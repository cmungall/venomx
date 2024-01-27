"""Conversion utils."""
import logging
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import yaml

import venomx as vx
from venomx.model.embeddings_pa import pyarrow_schema

logger = logging.getLogger(__name__)


class EmbeddingFormat(str, Enum):
    PARQUET = "parquet"
    YAML = "yaml"
    JSON = "json"


SUFFIX_MAP = {EmbeddingFormat.PARQUET: ".parquet"}


def embeddings_file_tuple(
    path: Union[str, Path],
    embedding_format: Optional[EmbeddingFormat] = EmbeddingFormat.PARQUET,
    allow_bundled=False,
    exists_check=True,
) -> Tuple[Path, Optional[Path], EmbeddingFormat]:
    """
    Given a path, return a tuple of the metadata file and embedded data file.

    :param path:
    :return:
    """
    path = str(path)
    suffix = SUFFIX_MAP.get(embedding_format)
    if path.endswith(".yaml"):
        metadata = Path(path)
        embeddings = Path(path.replace(".yaml", suffix))
    elif path.endswith(suffix):
        metadata = Path(path.replace(suffix, ".yaml"))
        embeddings = Path(path)
    else:
        raise ValueError(f"Invalid path: {path}")
    if exists_check:
        if not metadata.exists():
            raise ValueError(f"Metadata file does not exist: {metadata}")
        if not embeddings.exists():
            if allow_bundled:
                embeddings = None
            else:
                raise ValueError(f"Embeddings file does not exist: {embeddings}")
    return metadata, embeddings, embedding_format


def load_embeddings_as_pandas(
    self, source: Union[str, Path], format: EmbeddingFormat = EmbeddingFormat.PARQUET, **kwargs
) -> pd.DataFrame:
    if format == EmbeddingFormat.PARQUET:
        read_table = pq.read_table(str(source))
        df = read_table.to_pandas()
        df["values"] = df["values"].apply(lambda x: x.tolist() if isinstance(x, np.ndarray) else x)
        # df['values'] = df['values'].apply(lambda x: list(x) if isinstance(x, tuple) else x)
        return df
    else:
        raise ValueError(f"Unsupported format: {format}")


def _is_all_in_one(format: EmbeddingFormat) -> bool:
    """
    Check if a file is an all-in-one file.

    :param format:
    :param source:
    :return:
    """
    return format in [EmbeddingFormat.YAML, EmbeddingFormat.JSON]


def load_index(source: Union[str, Path], format: EmbeddingFormat = None, check=True, **kwargs) -> vx.Index:
    """
    Load an index from a file.

    :param source:
    :param kwargs:
    :return:
    """
    if format is None:
        format = EmbeddingFormat.PARQUET
    all_in_one = _is_all_in_one(format)
    if all_in_one:
        metadata = source
        embeddings = None
        ef = format
    else:
        metadata, embeddings, ef = embeddings_file_tuple(source, format, allow_bundled=all_in_one)
    metadata_obj = yaml.safe_load(open(metadata))
    ix = vx.Index(**metadata_obj)
    if embeddings:
        if format == EmbeddingFormat.PARQUET:
            ix.embeddings_frame = load_embeddings_as_pandas(ix, embeddings, ef, **kwargs)
        else:
            raise NotImplementedError(f"Unsupported format: {format}")
    if not ix.embeddings and ix.embeddings_frame is None:
        raise ValueError(f"Index has no embeddings: {source}")
    if ix.embeddings and not ix.embeddings_frame:
        ix.embeddings_frame = pd.DataFrame([row.model_dump() for row in ix.embeddings])
    if check:
        validate(ix)
    return ix


def validate(ix: vx.Index, **kwargs):
    """
    Validate an index.

    :param ix:
    :param kwargs:
    :return:
    """
    if ix.embeddings_frame is not None:
        vseries = ix.embeddings_frame["values"]
        lens = set(vseries.apply(len).tolist())
        if len(lens) != 1:
            raise ValueError(f"Index has inconsistent embeddings lengths: {lens}")
        vseries_len = list(lens)[0]
        if ix.embeddings_dimensions is None:
            ix.embeddings_dimensions = vseries_len
        if vseries_len != ix.embeddings_dimensions:
            raise ValueError(
                "Index has inconsistent embeddings dimensions: " f"{vseries_len} != {ix.embeddings_dimensions}"
            )


def save_index(ix: vx.Index, target: Union[str, Path], format: EmbeddingFormat = EmbeddingFormat.PARQUET, **kwargs):
    """
    Save an index to a file.

    >>> num_entities = 100
    >>> embedding_dim = 50
    >>> entities = [f"X:{i}" for i in range(num_entities)]
    >>> embeddings = np.random.rand(num_entities, embedding_dim).tolist()
    >>> df = pd.DataFrame({"id": entities, "values": embeddings})
    >>> ix = vx.Index()
    >>> ix.objects = [vx.NamedObject(id=x) for x in entities]
    >>> ix.embeddings_frame = df
    >>> len(ix.objects)
    100
    >>> save_index(ix, "tests/output/test.vx.yaml")
    >>> ix2 = load_index("tests/output/test.vx.yaml")
    >>> len(ix2.objects)
    100

    :param ix:
    :param target:
    :param kwargs:
    :return:
    """
    metadata_path, embeddings_path, ef = embeddings_file_tuple(target, exists_check=False)
    all_in_one = format in [EmbeddingFormat.YAML, EmbeddingFormat.JSON]
    metadata_obj = ix.model_dump(exclude_unset=True)
    if all_in_one:
        metadata_obj["embeddings"] = populate_embeddings_list(ix)
    else:
        metadata_obj["embeddings"] = None
    metadata_obj["embeddings_frame"] = None
    yaml.safe_dump(metadata_obj, open(metadata_path, "w", encoding="utf-8"), sort_keys=False)
    if ix.embeddings_frame is not None:
        if format == EmbeddingFormat.PARQUET:
            df = ix.embeddings_frame
            df["values"] = df["values"].apply(lambda x: pa.array(x, type=pa.float32()))
            schema = pyarrow_schema()
            table = pa.Table.from_pandas(df, schema=schema)
            pq.write_table(table, str(embeddings_path))
        elif all_in_one:
            pass
        else:
            raise ValueError(f"Unsupported format: {format}")


def populate_embeddings_list(ix: vx.Index) -> List[Dict[str, list[float]]]:
    """
    Populate the embeddings list.

    :param ix:
    :return:
    """
    if ix.embeddings_frame is not None:
        embeddings = []
        for _, row in ix.embeddings_frame.iterrows():
            e = vx.Embedding(
                id=row["id"],
                values=row["values"],
            )
            embeddings.append({"id": row["id"], "values": row["values"]})
    return embeddings
