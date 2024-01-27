from functools import lru_cache

import pyarrow as pa

ID = "id"
NAME = "name"
VALUES = "values"
METADATA = "metadata"


@lru_cache
def pyarrow_schema() -> pa.Schema:
    """
    Schema for the embeddings table.

    :return:
    """
    return pa.schema(
        [
            (ID, pa.string()),
            (VALUES, pa.list_(pa.float32())),
        ]
    )
