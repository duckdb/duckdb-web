---
layout: docu
title: Integration with PyTorch
---

[PyTorch](https://pytorch.org/) tensors can be built from DuckDB query results by exporting each result batch as [Apache Arrow](https://arrow.apache.org/docs/format/Columnar.html). This pattern is useful when training or serving models on Parquet data because DuckDB can filter and project the input before the batches are converted to tensors.

## Installation

```batch
pip install -U duckdb pyarrow torch
```

## DuckDB to PyTorch

This example queries a Parquet-backed Arrow dataset, streams the result as `RecordBatch` objects, and converts each batch into feature and label tensors.

```python
import pathlib
import tempfile

import duckdb
import numpy as np
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq
import torch

base_path = pathlib.Path(tempfile.mkdtemp())
parquet_dir = base_path / "train"

table = pa.table(
    {
        "feature_0": [0.1, 0.3, 0.5, 0.7],
        "feature_1": [1.0, 0.0, 1.0, 0.0],
        "label": [0, 1, 1, 0],
    }
)
pq.write_to_dataset(table, str(parquet_dir))

con = duckdb.connect()
train_dataset = ds.dataset(str(parquet_dir))

reader = con.execute("""
    SELECT feature_0, feature_1, label
    FROM train_dataset
    WHERE label = 1
""").to_arrow_reader(batch_size=2)

for batch in reader:
    features = torch.tensor(
        np.column_stack(
            [
                batch.column(0).to_numpy(),
                batch.column(1).to_numpy(),
            ]
        ),
        dtype=torch.float32,
    )
    labels = torch.tensor(batch.column(2).to_numpy(), dtype=torch.int64)

    print(features.shape, labels)
```

```text
torch.Size([2, 2]) tensor([1, 1])
```

DuckDB pushes the `WHERE label = 1` filter and the selected columns into the dataset scan, so only the requested rows and columns are converted to tensors. The `to_arrow_reader` method streams the result in batches instead of materializing the full result in memory at once.

To learn more about querying Arrow objects directly, see the [“SQL on Apache Arrow” guide]({% link docs/lts/guides/python/sql_on_arrow.md %}) and the [“Export to Apache Arrow” guide]({% link docs/lts/guides/python/export_arrow.md %}).
