---
layout: post
title: "Lightweight Text Analytics Workflows with DuckDB"
author: Petrica Leuca
thumb: "/images/blog/thumbs/text-analytics.svg"
image: "/images/blog/thumbs/text-analytics.png"
excerpt: "In this post, we demonstrate how to use DuckDB for keyword, full-text, and semantic similarity search with embeddings."
tags: ["using DuckDB"]
---

## Introduction

Text analytics is a central component of many modern data workflows, covering tasks such as keyword matching, full-text search, and semantic comparison. Conventional tools frequently require complex pipelines and substantial infrastructure, which can pose significant challenges. DuckDB offers a high-performance SQL engine that simplifies and streamlines text analytics. In this post, we will demonstrate how to leverage DuckDB to efficiently perform advanced text analytics in Python.

> The following implementation is executed in a [marimo Python notebook](https://marimo.io/), which is available on GitHub, in our [examples repository](https://github.com/duckdb/duckdb-blog-examples/tree/main/text_analytics_with_duckdb).

## Data Preparation

We will be working with a public dataset, available on [Hugging Face](https://huggingface.co/datasets/dair-ai/emotion), which contains English Twitter messages and their classification to one of the following emotions: anger, fear, joy, love, sadness, and surprise.

With DuckDB we are able to access Hugging Face datasets via the `hf://` prefix:

```python
from_hf_rel = conn.read_parquet(
        "hf://datasets/dair-ai/emotion/unsplit/train-00000-of-00001.parquet",
        file_row_number=True
    )
from_hf_rel = from_hf_rel.select("""
    text,
    label as emotion_id,
    file_row_number as text_id
""")
from_hf_rel.to_table("text_emotions")
```

> How to access Hugging Face datasets with DuckDB is detailed in the post [“Access 150k+ Datasets from Hugging Face with DuckDB”]({% post_url 2024-05-29-access-150k-plus-datasets-from-hugging-face-with-duckdb %}).

In the above data we have available only the identifier of an emotion (`emotion_id`), without its descriptive information. Therefore, from the list provided in the dataset description, we create a reference table by unnesting the Python list and retrieving the index for each value with the [`generate_subscripts`]({% link docs/stable/sql/query_syntax/unnest.md %}#keeping-track-of-list-entry-positions) function:
```python
emotion_labels = ["sadness", "joy", "love", "anger", "fear", "surprise"]

from_labels_rel = conn.values([emotion_labels])
from_labels_rel = from_labels_rel.select("""
    unnest(col0) as emotion,
    generate_subscripts(col0, 1) - 1 as emotion_id
""")
from_labels_rel.to_table("emotion_ref")
```

Last we define a relation, by joining the two tables:
```python
text_emotions_rel = conn.table("text_emotions").join(
    conn.table("emotion_ref"), condition="emotion_id"
)
```

> By executing `text_emotions_rel.to_view("text_emotions_v", replace=True)` a view with the name `text_emotions_v` will be created, which can be used in SQL cells.

We plot on a bar chart the emotion distribution to have an initial understanding of our data:
<div align="center" style="margin:10px">
    <a href="/images/blog/text-analytics/emotions_in_dataset.png">
        <img
          src="{% link images/blog/text-analytics/emotions_in_dataset.png %}"
          alt="Emotion distribution in the data"
          width="700"
        />
    </a>
</div>

## Keyword Search

*Keyword search* is the most basic form of text retrieval, matching exact words or phrases in text fields using SQL conditions such as `CONTAINS`, `ILIKE`, or other DuckDB [text functions]({% link docs/stable/sql/functions/text.md %}).
It is fast, requires no preprocessing, and works well for structured queries like filtering logs, matching tags, or finding product names.

For example, getting the texts and their emotion label containing the phrase `excited to learn` is a matter of applying `filter` on the relation defined above:

```python
text_emotions_rel.filter("text ilike '%excited to learn%'").select("""
    emotion,
    substring(
        text,
        position('excited to learn' in text),
        len('excited to learn')
    ) as substring_text 
""")
```

```text
┌─────────┬──────────────────┐
│ emotion │  substring_text  │
│ varchar │     varchar      │
├─────────┼──────────────────┤
│ sadness │ excited to learn │
│ joy     │ excited to learn │
│ joy     │ excited to learn │
│ fear    │ excited to learn │
│ fear    │ excited to learn │
│ joy     │ excited to learn │
│ joy     │ excited to learn │
│ sadness │ excited to learn │
└─────────┴──────────────────┘
```

One common step in text processing is to split text into tokens (keywords), where raw text is broken down into smaller units (typically words), that can be analyzed or indexed. This process, known as *tokenization*, helps convert unstructured text into a structured form suitable for keyword search. In DuckDB this process can be implemented with the [`regexp_split_to_table` function]({% link docs/stable/sql/functions/text.md %}#regexp_split_to_tablestring-regex), which will split the text based on the provided regex and return each keyword on a row.

> This step is case sensitive, therefore it is important to convert all text to a consistent case (by applying [`lcase`]({% link docs/stable/sql/functions/text.md %}#lcasestring) or [`ucase`]({% link docs/stable/sql/functions/text.md %}#ucasestring)) before processing.

In the below code snippet we select all the keywords by splitting the text on one or more non-word characters (anything except `[a-zA-Z0-9_]`):

```python
text_emotions_tokenized_rel = text_emotions_rel.select("""
    text_id,
    emotion,
    regexp_split_to_table(text, '\\W+') as token
""")
```

In the tokenization step, we usually exclude common words (such as `and`, `the`), called *stopwords*. In DuckDB we implement the exclusion by applying an [`ANTI JOIN`]({% link docs/stable/sql/query_syntax/from.md %}#semi-and-anti-joins) on a curated CSV file hosted on GitHub:

```python
english_stopwords_rel = duckdb_conn.read_csv(
    "https://raw.githubusercontent.com/stopwords-iso/stopwords-en/refs/heads/master/stopwords-en.txt",
    header=False,
).select("column0 as token")

text_emotions_tokenized_rel.join(
    english_stopwords_rel,
    condition="token",
    how="anti",
).to_table("text_emotion_tokens")

```

Now that we have tokenized and cleaned the text, we can implement keyword search by ranking the match with [similarity functions]({%link docs/stable/sql/functions/text.md %}#text-similarity-functions), such as [Jaccard](https://en.wikipedia.org/wiki/Jaccard_index):

```python
text_token_rel = conn.table(
    "text_emotion_tokens"
).select("token, emotion, jaccard(token, 'learn') as jaccard_score")

text_token_rel = text_token_rel.max(
    "jaccard_score",
    groups="emotion, token",
    projected_columns="emotion, token"
)

text_token_rel.order("3 desc").limit(10)
```

```text
┌──────────┬─────────┬────────────────────┐
│ emotion  │  token  │ max(jaccard_score) │
│ varchar  │ varchar │       double       │
├──────────┼─────────┼────────────────────┤
│ fear     │ learn   │                1.0 │
│ surprise │ learn   │                1.0 │
│ love     │ learn   │                1.0 │
│ joy      │ lerna   │                1.0 │
│ sadness  │ learn   │                1.0 │
│ fear     │ learner │                1.0 │
│ anger    │ learn   │                1.0 │
│ joy      │ leaner  │                1.0 │
│ fear     │ allaner │                1.0 │
│ anger    │ learner │                1.0 │
├──────────┴─────────┴────────────────────┤
│ 10 rows                       3 columns │
└─────────────────────────────────────────┘
```

We can also visualize the data to gain insights. One simple and effective approach is to plot the most frequently used words. By counting token occurrences across the dataset and displaying them in bubble plots, we can quickly identify dominant themes, repeated keywords, or unusual patterns in the text. For example, we plot the data by using a [scatter facet plot](https://plotly.com/python/facet-plots/) per emotion:

<div align="center" style="margin:10px">
    <a href="/images/blog/text-analytics/most_used_word.png">
        <img
          src="{% link images/blog/text-analytics/most_used_word.png %}"
          alt="Most used word"
          width="700"
        />
    </a>
</div>

From the above plot, we observe repeated keywords, such as `feel - feeling`, `love - loved - loving`. In order to de-duplicate such data, we need to look at the [word stem](https://en.wikipedia.org/wiki/Word_stem) rather than at the word itself. This brings us to full-text search.

## Full-Text Search

The [Full-Text Search (FTS) DuckDB extension]({%link docs/stable/core_extensions/full_text_search.md %}) is an experimental extension, which implements two main [full-text search](https://cloud.google.com/discover/what-is-full-text-search) functionalities:
- the `stem` function, to retrieve the word stem;
- the `match_bm25` function, to calculate the [Best Match score](https://en.wikipedia.org/wiki/Okapi_BM25).

By applying `stem` to the token column, we can now visualize the most frequently used word stem in our data:
<div align="center" style="margin:10px">
    <a href="/images/blog/text-analytics/most_used_stem.png">
        <img
          src="{% link images/blog/text-analytics/most_used_stem.png %}"
          alt="Most used stem"
          width="700"
        />
    </a>
</div>

We observe that `feel` and `love` appear only once and new word stems are plotted, such as `support`, `surpris`.

While the `stem` function can be used standalone, the `match_bm25` one requires the build of a FTS index, a special index that allows fast and efficient searching of text by indexing the words (tokens) in a column:
```python
conn.sql("""
    PRAGMA create_fts_index(
        "text_emotions", 
        text_id, 
        "text", 
        stemmer = 'english',
        stopwords = 'english_stopwords',
        ignore = '(\\.|[^a-z])+',
        strip_accents = 1, 
        lower = 1, 
        overwrite = 1
    )
""")
```

In the FTS index creation we are using the same list of English stopwords as in the tokenization process, by saving it into a table, named `english_stopwords`. The index is case insensitive due to the `lower` parameter, which will lowercase the text automatically.

> Warning The index can be created only on tables and it requires a unique identifier of the text. It also needs to be rebuild when the underlying data has been modified.

Once the index has been created, we can rank the match between the `text` column and the phrase `excited to learn`:

```python
text_emotions_rel
.select("""
    emotion,
    text,
    emotion_color,
    fts_main_text_emotions.match_bm25(
        text_id,
        'excited to learn'
    )::decimal(3, 2) as bm25_score
""")
.order("bm25_score desc")
.limit(10)
```

<div align="center" style="margin:10px">
    <a href="/images/blog/text-analytics/fts.png">
        <img
          src="{% link images/blog/text-analytics/fts.png %}"
          alt="FTS results"
          width="700"
        />
    </a>
</div>

Out of the 10 returned texts, displayed above in a [table plot](https://plotly.com/python/table/), 2 are poor matches to our search input; likely due to BM25 scoring being skewed by common terms or differences in document length.

## Semantic Search

Compared to keyword and full-text search, *semantic search* takes into account the meaning and context of the text. Instead of just looking for exact words, it uses techniques like [vector embeddings](https://github.com/veekaybee/what_are_embeddings) to capture the underlying concepts. Semantic search, which is case insensitive, can be implemented in DuckDB, by making use of the (also experimental) [Vector Similarity Search extension]({% link docs/stable/core_extensions/vss.md %}).

The vector embeddings of a (list of) text can be calculated with the [`sentence-transformers` library](https://sbert.net/) and the [pre-trained model `all-MiniLM-L6-v2`](https://sbert.net/docs/sentence_transformer/pretrained_models.html):
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_text_embedding_list(list_text: list[str]):
    """
    Return the list of normalized vector embeddings for list_text.
    """
    return model.encode(list_text, normalize_embeddings=True)
```

For example, `get_text_embedding_list(['excited to learn'])` will return:
```text
array([[ 3.14795598e-02, -6.66208193e-02,  1.05058309e-02,
         4.12571728e-02, -8.67664907e-03, -1.79746319e-02,
        ...
        -2.50727013e-02, -3.00881546e-03,  1.55055271e-02]], dtype=float32)
```

We register the model inference function as a [Python User Defined Function]({% link docs/stable/clients/python/function.md %}) and create a table with a column of type `FLOAT[384]` to load the embeddings into:

```python
conn.create_function(
    "get_text_embedding_list",
    get_text_embedding_list,
    return_type='FLOAT[384][]'
)

conn.sql("""
    create table text_emotion_embeddings (
        text_id integer,
        text_embedding FLOAT[384]
    )
""")
```

With the Python UDF, we save, in batches, the model output in `text_emotion_embeddings`:
```python
for i in range(num_batches):
    selection_query = (
        duckdb_conn.table("text_emotions")
        .order("text_id")
        .limit(batch_size, offset=batch_size*i)
        .select("*")
    )

    (
        selection_query.aggregate("""
            array_agg(text) as text_list,
            array_agg(text_id) as id_list,
            get_text_embedding_list(text_list) as text_emb_list
        """).select("""
            unnest(id_list) as text_id,
            unnest(text_emb_list) as text_embedding
        """)
    ).insert_into("text_emotion_embeddings")
```

> We wrote about model inference in DuckDB in the post [Machine Learning Prototyping with DuckDB and scikit-learn]({% post_url 2025-05-16-scikit-learn-duckdb %}).

We can now perform semantic search by using the [cosine distance](https://en.wikipedia.org/wiki/Cosine_similarity#Cosine_distance) between the vector embedding of our search text, `excited to learn`, and the embedding of the `text` field:
```python
input_text_emb_rel = conn.sql("""
    select get_text_embedding_list(['excited to learn'])[1] as input_text_embedding
""")

text_emotions_rel
.join(conn.table("text_emotion_embeddings"), condition="text_id")
.join(input_text_emb_rel, condition="1=1")
.select("""
        text, 
        emotion,
        emotion_color,
        array_cosine_distance(
            text_embedding,
            input_text_embedding
        )::decimal(3, 2) as cosine_distance_score
    """)
.order("cosine_distance_score asc")
.limit(10)
```

<div align="center" style="margin:10px">
    <a href="/images/blog/text-analytics/vss.png">
        <img
          src="{% link images/blog/text-analytics/vss.png %}"
          alt="VSS results"
          width="700"
        />
    </a>
</div>

Interesting to observe that the phrase `i am excited to learn and feel privileged to be here` didn't make it in the top 10 results in our semantic search!

### Similarity Joins

Vector embeddings are most known for their usability in search engines, but they can be used in a variety of text analytics use cases, such as topic grouping, classification or semantic matching between documents. The VSS extension provides [vector similarity joins]({% link docs/stable/core_extensions/vss.md %}#bonus-vector-similarity-search-joins), which can be used to conduct these types of analytics.

For example, we show in the below [heatmap chart](https://plotly.com/python/heatmaps/) the number of texts for each combination of emotion labels, where the x-axis corresponds to the semantic matching between the text and the emotion, the y-axis to the classified emotion, and the color indicates the count of texts assigned to each pair: 

<div align="center" style="margin:10px">
    <a href="/images/blog/text-analytics/best_matched_emotion.png">
        <img
          src="{% link images/blog/text-analytics/best_matched_emotion.png %}"
          alt="Best matched emotion versus classified emotion"
          width="700"
        />
    </a>
</div>

It is particularly noticeable that from the 6 emotions, only `sadness` has a strong semantic match with the text classified with the same label. As with full-text search, semantic search is affected by differences in document length (in this case the emotion keyword versus a text).

## Hybrid Search

While each type of search has its own applicability, we observed that some results are not as expected:
- keyword search and full-text search do not take word meaning into account;
- semantic search scored synonyms higher than the search text.

In practice, the three search methods are combined and used to perform a “hybrid search”, in order to improve the search relevance and accuracy. We start by calculating the score for each type of search, by implementing custom logic, such as a check on the emotion:

```python
if(
    emotion = 'joy' and contains(text, 'excited to learn'),
    1,
    0
) exact_match_score,

fts_main_text_emotions.match_bm25(
        text_id,
        'excited to learn'
)::decimal(3, 2) as bm25_score,

array_cosine_similarity(
    text_embedding,
    input_text_embedding
)::decimal(3, 2) as cosine_similarity_score
```

The BM25 score is ranked in descending order and the cosine  distance in ascending order. In hybrid search, we use the `array_cosine_similarity` score to ensure the same sort order (in this case descending).

> cosine similarity = 1 - cosine distance

Because the BM25 score can be, in theory, unbounded, we need [to scale the score](https://en.wikipedia.org/wiki/Feature_scaling) to the interval `[0, 1]` by implementing the min-max normalization:

```python
max(bm25_score) over () as max_bm25_score,
min(bm25_score) over () as min_bm25_score,
(bm25_score - min_bm25_score) / nullif((max_bm25_score - min_bm25_score), 0) as norm_bm25_score
```


The hybrid search score is calculated by applying a weight to the BM25 and cosine similarity scores:
```python
if(
    exact_match_score = 1,
    exact_match_score,
    cast(
        0.3 * coalesce(norm_bm25_score, 0) +
        0.7 * coalesce(cosine_similarity_score, 0)
        as
        decimal(3, 2)
    )
) as hybrid_score
```

And here are the results! Much better, don't you think?
<div align="center" style="margin:10px">
    <a href="/images/blog/text-analytics/hybrid.png">
        <img
          src="{% link images/blog/text-analytics/hybrid.png %}"
          alt="Hybrid search results"
          width="700"
        />
    </a>
</div>

## Conclusion

In this post, we showed how DuckDB can be used for text analytics by combining keyword, full-text, and semantic search techniques. Using the experimental `fts` and `vss` extensions with the `sentence-transformers` library, we demonstrated how DuckDB can support both traditional and modern text analytics workflows.
