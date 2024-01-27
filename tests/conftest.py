import pytest
from click.testing import CliRunner
from venomx.tools.file_io import save_index

from tests import OUTPUT_DIR, TEMP_TEST_YAML


@pytest.fixture
def runner() -> CliRunner:
    runner = CliRunner()
    return runner


@pytest.fixture
def create_test_index_files() -> str:
    """
    Create a test index.

    :return:
    """
    import numpy as np
    import pandas as pd
    import venomx as vx

    num_entities = 10
    embedding_dim = 20
    entities = [f"X:{i}" for i in range(num_entities)]
    embeddings = np.random.rand(num_entities, embedding_dim).tolist()
    df = pd.DataFrame({"id": entities, "values": embeddings})
    ix = vx.Index()
    ix.objects = [vx.NamedObject(id=x) for x in entities]
    ix.embeddings_frame = df
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    save_index(ix, TEMP_TEST_YAML)
    return TEMP_TEST_YAML
