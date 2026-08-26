---
layout: post
title: "How DuckDB Runs Recursive CTEs Faster"
author: "Denis Hirn"
excerpt: "DuckDB's recursive CTE engine now treats recursion as one long-lived computation: it retains eligible epoch-invariant state, chooses execution modes from exact frontier cardinalities and physical work, probes keyed state directly and gives `USING KEY ... UNION` changed-key semantics."
tags: ["deep dive"]
thumb: "/images/blog/thumbs/recursive-queries.svg"
image: "/images/blog/thumbs/recursive-queries.jpg"
---

When I implemented [DuckDB's first recursive CTE operator](https://github.com/duckdb/duckdb/pull/404) in 2020, correctness determined the design: evaluate the non-recursive term once, then evaluate the recursive term until the next working table is empty. That established the right semantic contract, but reusable runtime state was scoped too narrowly. Across iterations, the recursive input changes while most of the machinery that evaluates it remains reusable. The implementation nevertheless treated every iteration almost like a new query and repeatedly paid for pipeline scheduling, operator setup, execution and teardown. I have wanted to remove that mismatch ever since.

In the upcoming DuckDB v2.0, we assign those scopes explicitly. The query plan owns the physical operator tree, precomputed pipeline schedules and a pool of reusable pipeline executors. Each recursive invocation borrows executors from that pool and owns the accumulated recursive state and retained materializations whose lifetime spans the complete fixed-point computation, while each iteration owns only frontier-dependent state. This separation enables retained hash builds, per-iteration selection between inline and scheduled execution and direct probes into keyed state. The physical execution changes are accompanied by one semantic change: for `USING KEY`, `UNION` now makes new keys and keys whose finalized payload changed visible to the next iteration.

To illustrate the performance impact, we compare the original and new engines on a small reachability query. The table contains one million edges over 100,000 nodes. Ten identical edges leave each source node, and following them from node 0 visits 20,000 nodes:

```sql
CREATE TABLE edges AS
    SELECT (range % 100_000)::INTEGER AS src,
           ((range * 13 + 7) % 100_000)::INTEGER AS dst
    FROM range(1_000_000);

WITH RECURSIVE reachable(node) AS (
    SELECT 0
    UNION
    SELECT dst
    FROM edges, reachable
    WHERE src = node
)
SELECT count(*)
FROM reachable;
```

With the optimizations described below, median runtime falls from 4.051 seconds with DuckDB v1.5.5 to 0.095 seconds with the DuckDB v2.0 preview, a 42.6× speedup without changing the SQL.

## Reusable Execution State Outlives the Frontier

Recursive CTE execution sits inside the query-plan lifetime. The physical operator tree belongs to that plan, and immutable schedule projections are built during physical pipeline construction. Within the plan, an invocation spans one complete fixed-point computation, while an epoch spans one evaluation of the recursive term. The original query plan already retained the recursive physical operator, but its runtime treated each epoch as a fresh execution: it recreated events and executors, reconstructed operator state and repeated scheduling work.

During pipeline construction, DuckDB derives immutable views of the pipeline dependency schedule, including the form that omits invocation-retained build pipelines after their first execution. We refer to these views as **schedule projections**. The runtime can therefore select the required dependency schedule without deriving it again for every epoch.

### The Frontier Bounds Recursive Input

Every recursive **epoch** replaces the working table, often called the **frontier**, while the query remains fixed. The anchor term produces the first frontier. The recursive term reads it and produces candidates for the next one. With regular `UNION`, DuckDB rejects rows already seen; the survivors form the next frontier and also contribute to the logical **union table**. Evaluation stops when no rows survive.

The union table belongs to the semantics. DuckDB need not materialize it: result chunks can stream downstream while the engine retains the current frontier and, for regular `UNION`, the hash state required for duplicate elimination. It accumulates a complete copy only when the recursive term accesses `recurring.⟨cte_name⟩`{:.language-sql .highlight}.

For a monotone, linear recursive term, this frontier discipline is the operational core of **semi-naive evaluation**: an epoch reads only the preceding delta instead of reevaluating the recursive term from every row seen so far. The original operator already preserved this semantic invariant; the remaining mismatch concerned the lifetime of the physical machinery evaluating that frontier.

### Epoch-Invariant State Belongs to the Invocation

The frontier scan, shown as `REC_CTE_SCAN` in an `EXPLAIN` plan, must read new input after an epoch boundary, and the runtime state of every operator that depends on that input must be reset. The query-plan-owned schedule projections remain valid. Executors checked out for the invocation and invocation-owned buffers can be reset for reuse, while a build exclusively over recursion-independent base tables can retain its materialized state if repeating the build would produce the same observable result. The old runtime failed to distinguish invocation-scoped materialized state from frontier-dependent state: materialized state whose validity spans the recursive invocation cannot be owned by one epoch.

An operation is **epoch-invariant** when its inputs do not depend on the current frontier and reevaluating it would reproduce the same observable result. Scanning a stable base table and building a hash table from it is the canonical example. The recursive runtime follows the same ownership distinction as **loop-invariant code motion**: the invariant build belongs outside the epoch loop, while probing it with the changing frontier remains inside.

The ownership invariant first failed in the recursive runtime. DuckDB executes a query as a graph of pipelines. Although the old physical operator retained its recursive meta-pipeline, every epoch recreated events and executors, scheduled the pipelines and reconstructed their state. Epoch-invariant pipelines consequently reread the same static input and rebuilt the same state.

A large epoch can amortize fixed scheduling and setup costs across many frontier rows. Rebuilding invariant state remains proportional to the static input size and can cost far more than probing it with the changing frontier.

![The old engine builds a hash table from each REC_CTE_SCAN frontier and probes it by scanning edges; the new engine scans edges and builds a retained hash table once, then probes it with each frontier.]({% link images/blog/recursive-cte-engine/execution-reuse-light.svg %}){: .lightmode-img }
![The old engine builds a hash table from each REC_CTE_SCAN frontier and probes it by scanning edges; the new engine scans edges and builds a retained hash table once, then probes it with each frontier.]({% link images/blog/recursive-cte-engine/execution-reuse-dark.svg %}){: .darkmode-img }

*DuckDB v1.5.5 rebuilds a hash table from each frontier and revisits `edges` as the probe input. The new engine reverses the join, builds the edge hash table once and probes it with each frontier.*{: .caption }

The resulting ownership boundary is:

| State | Owning scope | Epoch-boundary action |
| --- | --- | --- |
| Physical operator tree and immutable schedule projections | Query plan | Retain |
| Reusable pipeline-executor pool | Query plan | Retain |
| Executor checkout, chunks and collection capacity | Recursive invocation | Reset contents for reuse |
| Accumulated duplicate-elimination or keyed state | Recursive invocation | Retain |
| Repeatable, recursion-independent builds | Recursive invocation | Retain materialized state |
| Volatile, side-effecting or unknown builds | Epoch | Rebuild |
| Recursive scans | Epoch | Rebind to current recursive state |
| Candidate output | Epoch | Clear or combine |

The hash join in the opening query requires both a join reorientation and retained state. DuckDB v1.5.5 builds a hash table from the current `reachable` frontier and scans `edges` as the probe input in every epoch. The new planner places the recursion-independent `edges` relation on the build side where valid. The first epoch scans `edges` and builds the hash table; later epochs rebind `reachable` as the probe and reuse that table.

`EXPLAIN (ANALYZE, FORMAT JSON)` makes the avoided input work concrete. Both versions return the expected 20,000 nodes. DuckDB v1.5.5 reports `operator_rows_scanned: 19,718,328,320` on the `edges` scan, equivalent in row volume to about 19,718 complete scans, while the DuckDB v2.0 preview reports the table's one million rows once. Dynamic filtering skips parts of some v1.5.5 edge scans, but it cannot prevent the base relation from being revisited in every epoch.

### Retention Requires a Repeatability Proof

We retain a build only when its observable result is repeatable. Recursion independence establishes one requirement. Repeatability adds another: a seeded sample may be retained; an unseeded sample, a volatile expression such as `nextval()`, DML, a side-effecting operator or an unknown extension operator must be rebuilt. The repeatability classifier owns that decision and rejects retention when it cannot prove safety. This conservative choice may forgo reuse while preserving query semantics.

Fully materialized CTE producers follow the same ownership rule: a recursion-independent result may survive while each consumer scan is reset. We do not retain streaming or hybrid producers because their consumption state does not have the same lifetime. Early source termination is another boundary case. A retained pipeline must not withhold partial output merely to fill a vector, because doing so could prevent a downstream `LIMIT` from stopping recursive execution early. Reuse therefore preserves that termination contract.

## Exact Cardinalities Make Execution Adaptive

The epoch boundary provides information unavailable during ordinary query planning. By the time an epoch ends, DuckDB has produced the next frontier in full and therefore knows its row and chunk counts exactly. These observed cardinalities govern how the recursive runtime executes the next epoch; optimizer estimates no longer have to stand in for them.

### Each Epoch Chooses Its Own Mode

Once the opening query has built and retained its edge hash table, an epoch carries one reachable node into one probe. Sending that work through a parallel scheduler would create more coordination than useful work. A traversal whose frontier expands to many chunks has the opposite shape: executing it on one thread would leave independent pipeline work idle. A static mode chosen for the complete query cannot serve both cases, and a single query may move between them as its frontier grows and contracts.

When the exact frontier and physical work shape do not justify task scheduling, an epoch runs **inline**. One thread walks the selected immutable schedule projection and drives its operators directly, without creating tasks or entering the general scheduler. When the work classifier finds enough independent work, **scheduled execution** instantiates the corresponding recursive event graph and distributes work across a bounded number of workers. Both modes use the same query-plan-owned schedule projections. Executors checked out for the invocation and invocation-owned buffers are reset for reuse; only the epoch-level execution policy changes.

Rows alone do not determine useful parallelism. The policy also considers frontier chunks, the number of recursive references, independent source tasks, configured threads and the pipelines that would actually execute. The same frontier can feed several pipelines, while an independent source can expose work not represented by frontier rows. Conversely, worker-local output and boundary combination introduce costs of their own. We therefore bound workers by both recursive input and physical work units, using private output only for broad regular `UNION ALL` and duplicate-eliminating `UNION` epochs where its combine cost can amortize.

## Frozen Keyed State Enables Direct Probes

Torsten Grust and Björn Bamberg explain the original `USING KEY` feature and its applications in their [“`USING KEY` in Recursive CTEs” blog post]({% post_url 2025-05-23-using-key %}). Semantically, `USING KEY` operates the union table as keyed state: the declared key columns identify a row, while the remaining payload columns are maintained by declared aggregates or the default `last` aggregate. DuckDB physically represents this state in an aggregate hash table. The recursive term can therefore probe selected keys directly instead of scanning the complete recurring state.

### Each Epoch Reads a Frozen Keyed State

Direct access must preserve one semantic invariant: every access through `recurring.⟨cte_name⟩`{:.language-sql .highlight} during epoch `i` observes the same keyed state `Sᵢ`. The epoch has three ordered phases: read `Sᵢ`, buffer its candidate bag and commit those candidates to obtain `Sᵢ₊₁`. Making a candidate visible during the read phase would let another candidate from the same epoch observe it and make the result depend on worker arrival order. The three phases preserve an epoch-at-a-time state transition while probes execute concurrently.

The original implementation preserved the invariant by materializing keyed state into a collection for recurring-state reads. That representation gave every access a broad physical path: an epoch touching a few keys could still copy or scan a state containing millions of keys.

The keyed-state owner now enforces those phases. While recursive pipelines execute, `recurring.⟨cte_name⟩`{:.language-sql .highlight} reads the frozen aggregate hash table and candidates accumulate separately. The owner commits them only at the epoch boundary. A probe cannot observe a half-applied update, and hash-table growth cannot invalidate an address held by a concurrent reader. After recursion ends, the source drains the final keyed state once.

### Probe Eligibility Follows Join Shape

The frozen representation supports specialized physical lookups while preserving the semantic view. An inner join that compares every declared key with `=` or `IS NOT DISTINCT FROM` can use a **recursive key join**, shown as `RECURSIVE_KEY_JOIN` in `EXPLAIN`, and probe the aggregate hash table directly. Such comparisons on a proper subset of a composite key can use an epoch-stable secondary hash index through `RECURSIVE_PARTIAL_KEY_JOIN`. New complete keys extend an index only after their addresses are stable; payload-only updates do not require index maintenance.

We select the complete-key specialization only for an inner join against a direct recurring-state scan (`REC_REC_CTE_SCAN`) with a direct, exactly typed scalar `=` or `IS NOT DISTINCT FROM` comparison for every declared key. Residual predicates, wrapped scans, mismatched types, nested keys and other join types use the general path. An ordinary recursive reference is also ineligible because it denotes the frontier; the accumulated keyed state is available through the recurring reference. Treating those two identities as interchangeable would change the query.

### Sparse Work Should Avoid Full-State Scans

The workload below retains one million keys and advances 1,000 of them through 20 epochs:

```sql
WITH RECURSIVE state(key, value) USING KEY (key) AS (
    SELECT key, CASE WHEN key < 1_000 THEN 0 ELSE 100 END
    FROM range(1_000_000) keys(key)
    UNION ALL
    SELECT frontier.key, recurring_state.value + 1
    FROM state AS frontier
    JOIN recurring.state AS recurring_state USING (key)
    WHERE frontier.value < 20
)
SELECT count(*) AS keys, sum(value)::BIGINT AS value_sum
FROM state;
```

Before direct probes, the join repeatedly scanned `recurring.state`. The runtime metrics counted roughly 20 million full-state scan rows for 20,000 useful matches. The specialized plan replaces them with 20,000 direct probes, a 1,000× reduction in recurring-state rows examined. In a comparison of builds immediately before and after the direct-probe work, median runtime fell from 0.401 to 0.040 seconds. The new path also removes the per-epoch collection previously used to materialize the complete keyed state.

## Candidates Can Leave Keyed State Unchanged

The candidate bag can be nonempty even when keyed state does not change. If candidates automatically become the next frontier, recursion may continue after the state visible to the query has converged. Retaining execution state and probing it efficiently cannot repair that semantic mismatch.

`USING KEY ... UNION` now gives this distinction SQL-level semantics. Both our [“A Fix for the Fixation on Fixpoints” CIDR paper](https://db.cs.uni-tuebingen.de/publications/2023/a-fix-for-the-fixation-on-fixpoints/a-fix-for-the-fixation-on-fixpoints.pdf) and [“How DuckDB is `USING KEY` to Unlock Recursive Query Performance” SIGMOD paper]({% link _library/2025-06-22-bamberg-using-key-sigmod.md %}) describe the original candidate-frontier design, in which the candidate bag becomes the next working table regardless of whether keyed state changes. Neither defines a changed-key delta. To our knowledge, DuckDB is the first and currently the only database system to distinguish changed-key recursion under `UNION` from candidate-frontier recursion under `UNION ALL`.

### Finalized State Belongs to the Commit Layer

Before this change, DuckDB followed the original design and treated `USING KEY ... UNION` and `USING KEY ... UNION ALL` alike. Every candidate produced by the recursive term became input to the next epoch, even if applying it left the recurring table unchanged. Because plain `UNION` had the same candidate-frontier behavior as `UNION ALL`, DuckDB v1.5 deprecated it for `USING KEY`. The changed-key semantics introduced here give the two keywords distinct meanings, so the upcoming v2.0 retains both. The observable aggregate result for a key is determined only after every candidate for the epoch has been applied. Consequently, the epoch-commit layer owns the decision whether a key changed.

A shortest-path epoch demonstrates why candidates cannot decide this themselves. Several routes may reach the same node, and every route must participate in `min(distance)`. Only the finalized minimum is observable in keyed state. Forwarding every inferior route multiplies the work of the next epoch; forwarding an unchanged minimum can keep candidate production alive after state convergence.

Consider keyed state `{A:8, B:7}` with a `min` payload and candidates `[A:9, A:5, B:7]`. Applying the complete candidate bag produces `{A:5, B:7}`. The `A:9` candidate does not affect the finalized minimum, and `B:7` reproduces an existing value. `UNION ALL` nevertheless forwards all three candidates. `UNION` forwards only the finalized row `A:5` because it is the only observable state change.

### `UNION` and `UNION ALL` Expose Different Frontiers

Let `Cᵢ` be the candidate bag produced in epoch `i`, `Sᵢ` the keyed state visible during that epoch and `Wᵢ₊₁` the next working table. Let `update(Sᵢ, Cᵢ)` apply all candidates in the bag and finalize every affected payload aggregate, and let `keys(Sᵢ)` denote the keys present before the update. We define the two forms as follows:

```text
USING KEY ... UNION ALL
Sᵢ₊₁ = update(Sᵢ, Cᵢ)
Wᵢ₊₁ = Cᵢ

USING KEY ... UNION
Sᵢ₊₁ = update(Sᵢ, Cᵢ)
Wᵢ₊₁ = { Sᵢ₊₁[k] | k ∉ keys(Sᵢ) OR Sᵢ₊₁[k] IS DISTINCT FROM Sᵢ[k] }
```

For the same input state and candidate bag, both forms compute the same next keyed state. They differ in what becomes recursively visible: `UNION ALL` forwards the bag unchanged, while `UNION` forwards one finalized row for each new or observably changed key. Recursion under `USING KEY ... UNION` therefore stops when keyed state stops changing.

The epoch-commit layer implements the rule by recording prior key existence and snapshotting the pre-epoch finalized payload of an existing key when that key is first touched. It then applies every candidate before finalizing and comparing each touched key once. Duplicate candidates and losing `min` or `max` inputs still participate in aggregate evaluation, but they do not become recursive work on their own.

![USING KEY UNION ALL forwards every candidate, while UNION applies all candidates and forwards only finalized keys whose values changed.]({% link images/blog/recursive-cte-engine/keyed-delta-light.svg %}){: .lightmode-img }
![USING KEY UNION ALL forwards every candidate, while UNION applies all candidates and forwards only finalized keys whose values changed.]({% link images/blog/recursive-cte-engine/keyed-delta-dark.svg %}){: .darkmode-img }

*For the same keyed state and candidate bag, both forms compute the same state update; the next frontier is either that bag or the changed-key delta.*{: .caption }

We compare finalized values with SQL semantics, including `NULL` and collations. Key identity uses the same normalization as `GROUP BY`, and collated scalar keys remain eligible for direct and partial-key probes. The implementation also covers multi-column and nested payloads, `NaN` and signed zero.

The two frontiers also have different types. A `UNION ALL` frontier contains raw candidate rows, so its payload columns use aggregate input types. A `UNION` frontier contains finalized keyed rows, so its payload columns use aggregate result types. This distinction is visible through the SQL contract and constrains the internal representation. Because the keyword selects the frontier's contents, types and termination condition, we never infer one form from the other as an optimization.

## Changed-Key Deltas Still Pay for Candidate Work

A changed-key delta reduces the next frontier only after all candidates have been applied. Millions of duplicate candidates can therefore still make the recurring hash-table update expensive even when few keys ultimately change. For eligible duplicate-heavy epochs, we first combine candidates in a temporary keyed hash table, then combine those aggregate states into recurring state.

### Preaggregation Requires Combinable Aggregate State

Early combination must be observationally equivalent to applying candidates directly. We enable preaggregation only when every payload aggregate provides a state-combine operation and none is order-dependent. The default `last` aggregate and extension aggregates without a combine callback therefore remain on the direct update path. Without a combine operation, preaggregation lacks a valid state transition. For an order-dependent aggregate, it could change the observed input order and therefore change the result.

### Cardinality Evidence Governs Preaggregation

Eligibility establishes correctness; observed cardinality determines whether the valid transformation is worthwhile. Epochs smaller than one standard vector bypass classification, as do non-expanding epochs whose candidate count does not exceed the preceding frontier. Larger eligible epochs build a HyperLogLog sketch over candidate keys. We preaggregate only when the sketch's error-inflated cardinality estimate is below one quarter of the candidate count, and stop sketching early once distinct-key evidence is sufficient to reject the additional hash table. The decision therefore adapts to the duplication observed in each epoch.

The cost of proving an unchanged value constrains this policy. For a wide workload with 102,400 unique existing-key updates, median runtime increases by 0.913 milliseconds, or 6%, under the new `UNION` semantics. The executor must compare finalized values where the previous implementation forwarded candidates without proving a change. Aggregate-specific shortcuts for `min` and `max` would place aggregate semantics in the recursive executor, so we do not use them. An aggregate-level change-reporting contract could put that responsibility in the aggregate interface. The current interface provides no such contract.

The large motivating workload was an [LDBC](https://ldbcouncil.org) SF100 pathfinding query. It generated about 21 million aggregate candidates, but epoch-level aggregation produced only 3.7 million observable keyed results. The adaptive path preaggregated 17 million candidates. On matched Release builds immediately before and after the changed-key work, query time fell from a median of 19.319 to 2.948 seconds, a 6.55× speedup, while peak resident memory fell from 3.918 to 2.663 GB.

The wider regression suite bounds that result. In the same build comparison, the geometric mean across 63 recursive benchmarks improved by 5.5%, and 60 were within ±2%. Duplicate fan-in and duplicate-heavy preaggregation improved substantially; the wide unique-key case above is the one stable loss. For this reason, we classify work per epoch instead of applying the strategy that wins the motivating query to every workload.

## Recursive CTEs Now Execute as One Adaptive Computation

The new engine resolves the lifetime mismatch I wanted to remove after implementing DuckDB's original recursive operator. The query plan owns the physical operator tree, schedule projections and reusable executor pool. Within each invocation, the runtime checks out executors and retains proven repeatable, recursion-independent state across epochs, while each epoch rebinds and resets frontier-dependent state. This separation makes retained invariant work and per-epoch execution policy compatible. Keyed recursion uses the epoch boundary to freeze recurring state for direct probes, then commits the candidates and exposes only observable changes as the next frontier under `UNION`. The implementation landed across [#22211](https://github.com/duckdb/duckdb/pull/22211), [#24031](https://github.com/duckdb/duckdb/pull/24031), [#24565](https://github.com/duckdb/duckdb/pull/24565) and [#24647](https://github.com/duckdb/duckdb/pull/24647).

That matters because recursion multiplies every physical cost placed inside the epoch loop. A scan, hash build or trip through the general scheduler that seems modest in isolation may run tens of thousands of times. The new engine pays eligible invariant costs once per invocation, avoids scheduler overhead when the observed work cannot amortize it and distributes epochs that expose sufficient independent work. Eligible keyed joins can access the required state directly, while `USING KEY ... UNION` recursion terminates when that state converges. This makes recursive SQL a more practical execution model for graph traversals, pathfinding and state machines, especially when the frontier remains small while the static input is large or when many candidates update the same keys.

The next step is to extend this foundation to more recursive plans. Future work can extend invocation-scoped reuse to more eligible operator states and use cardinalities observed at epoch boundaries for further execution decisions. Each extension must retain the same frontier and state-transition semantics. I intend to keep working along that boundary: reduce the physical cost of iteration while keeping recursive SQL predictable.
