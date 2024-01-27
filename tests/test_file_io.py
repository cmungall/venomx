import pandas as pd
import numpy as np
import venomx as vx
from tests import OUTPUT_DIR
from venomx.tools.file_io import save_index, load_index

ID = "id"
NAME = "name"
EMBEDDING = "embedding"
METADATA = "metadata"


def test_save_load():
    # Generate mock data
    num_entities = 100
    embedding_dim = 50

    outpath = OUTPUT_DIR / "test.vx.yaml"
    entities = [f"X:{i}" for i in range(num_entities)]
    embeddings = np.random.rand(num_entities, embedding_dim).tolist()
    df = pd.DataFrame({"id": entities, "values": embeddings})
    ix = vx.Index()
    ix.objects = [vx.NamedObject(id=x) for x in entities]
    ix.embeddings_frame = df
    first_arr = ix.embeddings_frame["values"][0]
    assert isinstance(first_arr, list)
    assert isinstance(first_arr[0], float)
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    save_index(ix, outpath)
    ix2 = load_index(outpath)
    assert len(ix2.objects) == num_entities
    df2: pd.DataFrame = ix2.embeddings_frame
    first_arr2 = df2["values"][0]
    assert isinstance(first_arr2, list)
    assert df2["id"].equals(df["id"])
    assert np.isclose(first_arr[0], first_arr2[0])
    assert np.isclose(df2["values"].tolist(), df["values"].tolist()).all()

