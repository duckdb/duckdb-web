---
layout: default
title: History
body_class: history blog_typography
toc: true
permalink: /history/
---

<div class="wrap pagetitle">
  <div class="pagetitle-heading" role="heading" aria-level="1">DuckDB and Its Ecosystem</div>
</div>

<p class="lead">The DuckDB story now extends beyond the original database. Here is how the projects and organizations around it developed, and how they fit together today.</p>

<div class="timeline">

  <div class="timeline-entry">
    <div class="timeline-marker"><span class="timeline-year">2018</span></div>
    <div class="timeline-body">
      <h2 id="hello-world">Hello World</h2>
      <p>Mark Raasveldt and Hannes Mühleisen began developing DuckDB in 2018 while working as database researchers at Centrum Wiskunde &amp; Informatica (CWI) in Amsterdam. Their work grew from database systems research, later documented in <a href="{% link library/index.html %}?category=core&amp;format=paper">papers on DuckDB's design and architecture</a>, including its embedded analytical model.</p>
      <p>DuckDB was open source from day one. In 2019, Mark and Hannes announced <a href="/library/duckdb-sigmod-demo/">DuckDB v0.1</a> at the SIGMOD conference in Amsterdam. DuckDB could run as a single binary or inside Python, R, or another host process, giving users an analytical SQL engine without requiring them to deploy and maintain a separate database server.</p>
      <p>This in-process architecture removed a familiar source of friction. Developers could query files and data where they were already working. Data scientists could bring SQL into a notebook without first deploying database infrastructure. Product teams could embed analytical processing directly in their applications.</p>
      <p>As more people began using DuckDB, the project needed a permanent engineering home and a structure that could support long-term development.</p>
    </div>
  </div>

  <div class="timeline-entry">
    <div class="timeline-marker"><span class="timeline-year">2021</span></div>
    <div class="timeline-body">
      <h2 id="the-ecosystem-begins-to-take-shape">The Ecosystem Begins to Take Shape</h2>
      <p>On July 14, 2021, Mark and Hannes announced <a href="https://ducklabs.com/news/2021/07/14/spin-off-company-DuckDB-Labs">DuckDB Labs as a CWI spin-off</a>. The company brought the core engineering team together and created a commercial route for organizations that needed support or development work.</p>
      <p>The independent DuckDB Foundation was incorporated later that year. It holds most of DuckDB's intellectual property and safeguards the project's continuity under the permissive MIT license.</p>
      <p>The company and Foundation were designed for different responsibilities. DuckDB Labs became the engineering and commercial home of the core team. The Foundation provided the legal structure around intellectual property, trademarks, and long-term open-source continuity. Day-to-day development remained with the engineers and contributors working on the project.</p>
    </div>
  </div>

  <div class="timeline-entry">
    <div class="timeline-marker"><span class="timeline-year">2022</span></div>
    <div class="timeline-body">
      <h2 id="motherduck-adds-a-managed-cloud-path">MotherDuck Adds a Managed Cloud Path</h2>
      <p>DuckDB's local and embedded model covered a wide range of analytical work. Some teams also wanted centralized storage, sharing, collaboration, access control, and managed operations. MotherDuck was formed to build that cloud experience on DuckDB. In November 2022, DuckDB Labs announced <a href="https://ducklabs.com/news/2022/11/15/motherduck-partnership">a long-term partnership with MotherDuck</a>.</p>
      <p>MotherDuck contracts with DuckLabs for engineering work, supports the DuckDB Foundation, and contributes technology to the wider project. DuckLabs gives MotherDuck direct access to the people developing and maintaining the database.</p>
      <p>The partnership works through clearly defined roles. MotherDuck operates the managed cloud service, the Foundation holds DuckDB's intellectual property, and DuckLabs leads core engineering and commercial support around the open-source projects. The companies collaborate where their technical work overlaps.</p>
    </div>
  </div>

  <div class="timeline-entry">
    <div class="timeline-marker"><span class="timeline-year">2024</span></div>
    <div class="timeline-body">
      <h2 id="duckdb-reaches-10">DuckDB Reaches v1.0</h2>
      <p>On June 3, 2024, the team <a href="{% post_url 2024-06-03-announcing-duckdb-100 %}">released DuckDB v1.0.0</a>.</p>
      <p>The release emphasized stability rather than a long list of new features. DuckDB had gained backward compatibility for its storage format, extensive testing across the engine, and a more cautious approach to changes in the SQL dialect and C API. Version 1.0 expressed the team's confidence that developers could build applications on DuckDB with clearer expectations about compatibility over time.</p>
      <p>It was also a marker of adoption. Six years after the first code was written, DuckDB had moved from a research project into production systems, data workflows, and embedded products across a growing community.</p>
      <p>Later that year, MotherDuck made significant contributions to the <a href="{% post_url 2024-12-18-duckdb-node-neo-client %}">new DuckDB Node.js client</a>, another example of technical work shared across the ecosystem.</p>
    </div>
  </div>

  <div class="timeline-entry">
    <div class="timeline-marker"><span class="timeline-year">2025</span></div>
    <div class="timeline-body">
      <h2 id="the-work-expands-beyond-the-original-database">The Work Expands beyond the Original Database</h2>
      <p>In March 2025, DuckLabs and MotherDuck introduced the <a href="{% post_url 2025-03-12-duckdb-ui %}">DuckDB Local UI</a>, a browser-based interface delivered through the DuckDB <strong>ui</strong> extension. It runs queries against a local DuckDB instance and provides an explicit path to connect to MotherDuck when users want cloud capabilities. The project showed how the two companies could combine local and managed experiences in one workflow.</p>
      <p>Two months later, the DuckLabs team introduced <a href="https://ducklake.select/2025/05/27/ducklake-01/">DuckLake</a>, an open lakehouse format that keeps catalog metadata in a SQL database while storing data in the open Parquet format.</p>
      <p>DuckLake applied the team's database engineering experience to a different layer of the data stack. The work now covered the analytical engine and the organization of shared lakehouse data. The name DuckDB Labs was beginning to describe only part of what the company maintained.</p>
    </div>
  </div>

  <div class="timeline-entry">
    <div class="timeline-marker"><span class="timeline-year">2026, Q2</span></div>
    <div class="timeline-body">
      <h2 id="the-broader-direction-becomes-explicit">Broader Horizons</h2>
      <p>DuckLake reached <a href="https://ducklake.select/2026/04/13/ducklake-10/">version 1.0 on April 13, 2026</a>, establishing a production-ready specification and reference implementation.</p>
      <p>The Quack technical preview followed in May. Quack is the DuckDB client-server protocol, designed for workloads that need remote connections or multiple clients. It is available as a beta release while the team develops it toward stable status as <a href="{% post_url 2026-08-17-duckdb-20-highlights %}">DuckDB v2.0</a>.</p>
      <p>The change from <a href="https://ducklabs.com/news/2026/05/27/duckdb-labs-becomes-ducklabs">DuckDB Labs to DuckLabs</a> came later that month. By then, the company employed more than 30 people working across DuckDB, DuckLake, Quack, extensions, language bindings, and related systems engineering.</p>
    </div>
  </div>

  <div class="timeline-entry">
    <div class="timeline-marker"><span class="timeline-year">2026, Q3</span></div>
    <div class="timeline-body">
      <h2 id="ducklabs-to-join-aws">DuckLabs Is Joining AWS</h2>
      <p>On August 26, 2026, DuckLabs announced that <a href="https://ducklabs.com/news/2026/08/26/ducklabs-to-join-aws">it is joining Amazon Web Services</a>. The DuckLabs team stays in Amsterdam and remain focused on the development of the core projects – DuckDB, DuckLake and Quack.</p>
      <p>These projects will remain the intellectual property of the <a href="https://duckdb.foundation/">DuckDB Foundation</a> and open source under the MIT license. The scope of the <a href="{% link community_support.md %}">community support</a> is extended to accept larger volumes of issues and pull requests, and will cover more components.</p>
    </div>
  </div>

</div>
