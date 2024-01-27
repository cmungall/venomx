import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import venomx as vx

ID = "id"
NAME = "name"
EMBEDDING = "embedding"
METADATA = "metadata"


def test_foo():
    ix = vx.Index()
    # Generate mock data
    num_entities = 100
    embedding_dim = 50

    entities = [f"X:Entity_{i}" for i in range(num_entities)]
    embeddings = np.random.rand(num_entities, embedding_dim).tolist()

    # Create a DataFrame
    df = pd.DataFrame(
        {ID: range(num_entities), NAME: entities, EMBEDDING: embeddings, METADATA: [{"foo": "x"}] * num_entities}
    )

    # Convert Embedding column to a list of pyarrow arrays
    df[EMBEDDING] = df[EMBEDDING].apply(lambda x: pa.array(x, type=pa.float32()))

    # Define schema for Parquet file
    schema = pa.schema(
        [
            (ID, pa.int32()),
            (NAME, pa.string()),
            (EMBEDDING, pa.list_(pa.float32())),
            (METADATA, pa.map_(pa.string(), pa.string())),
        ]
    )

    # Convert DataFrame to PyArrow Table
    table = pa.Table.from_pandas(df, schema=schema)

    ix.embeddings_frame = table
    # print(ix.model_dump())

    # Write to a Parquet file
    parquet_file = "embeddings.parquet"
    pq.write_table(table, parquet_file)

    # Read from a Parquet file
    read_table = pq.read_table(parquet_file)
    read_df = read_table.to_pandas()

    # Display the DataFrame
    print(read_df.head())
