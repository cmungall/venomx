from __future__ import annotations

import sys
from typing import Any, List, Optional

from pydantic import BaseModel as BaseModel
from pydantic import ConfigDict, Field

if sys.version_info >= (3, 8):
    pass
else:
    pass


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra="forbid",
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )
    pass


class Index(ConfiguredBaseModel):

    """
    A collection of named objects
    """

    id: Optional[str] = Field(None, description="""The identifier for index""")
    prefixes: Optional[List[Prefix]] = Field(default_factory=list, description="""The prefix map for index""")
    dataset: Optional[Dataset] = Field(None, description="""The dataset for named objects""")
    embeddings: Optional[List[Embedding]] = Field(
        default_factory=list, description="""The embeddings for named objects"""
    )
    embeddings_frame: Optional[Any] = Field(None, description="""Can be a dataframe, pyarrow object...""")
    embeddings_dimensions: Optional[int] = Field(None, description="""The number of dimensions for the embeddings""")
    embedding_model: Optional[Model] = Field(None, description="""The embedding model for dataset""")
    embedding_input_method: Optional[ModelInputMethod] = Field(
        None, description="""The method used to generate the input for the embedding model"""
    )
    objects: Optional[List[NamedObject]] = Field(default_factory=list, description="""The named objects""")
    is_external: Optional[bool] = Field(None, description="""Whether the objects are external""")
    md5: Optional[str] = Field(None, description="""The md5 for the index""")


class Prefix(ConfiguredBaseModel):

    """
    A prefix
    """

    prefix: Optional[str] = Field(None, description="""The prefix for prefix""")
    namespace: Optional[str] = Field(None, description="""The expansion for prefix""")


class Dataset(ConfiguredBaseModel):

    """
    A description of the dataset that the index is over. Note that this is not intended to be a comprehensive description of the dataset (use other standards for this), but enough to give context to the index.
    """

    name: Optional[str] = Field(None, description="""The name for dataset""")
    identifiers: Optional[List[str]] = Field(default_factory=list, description="""Identifiers for the dataset""")
    filesystem_path: Optional[str] = Field(None, description="""The filesystem path for dataset""")
    url: Optional[str] = Field(None, description="""The url for dataset""")
    title: Optional[str] = Field(None, description="""The label for dataset""")
    source: Optional[str] = Field(None, description="""The source for dataset""")
    version: Optional[str] = Field(None, description="""The version for dataset""")
    metadata: Optional[List[str]] = Field(default_factory=list, description="""The metadata for dataset""")


class Model(ConfiguredBaseModel):

    """
    A model
    """

    name: Optional[str] = Field(None, description="""The name for model""")
    identifiers: Optional[List[str]] = Field(default_factory=list, description="""Identifiers for the model""")
    url: Optional[str] = Field(None, description="""The url for model""")
    title: Optional[str] = Field(None, description="""The label for model""")
    source: Optional[str] = Field(None, description="""The source for model""")
    version: Optional[str] = Field(None, description="""The version for model""")
    metadata: Optional[List[str]] = Field(default_factory=list, description="""The metadata for model""")


class ModelInputMethod(ConfiguredBaseModel):

    """
    A method for generating the input for an embedding model. This might be as simple as extracting the label (name) of the object, or it might be involve concatenation of multiple fields.
    """

    fields: Optional[List[str]] = Field(default_factory=list, description="""The fields for model input method""")


class NamedObject(ConfiguredBaseModel):

    """
    A named object
    """

    id: str = Field(..., description="""The identifier for named object""")
    label: Optional[str] = Field(None, description="""The label for named object""")
    metadata: Optional[List[str]] = Field(default_factory=list, description="""The metadata for named object""")


class Embedding(ConfiguredBaseModel):

    id: str = Field(..., description="""The identifier for named object""")
    text: Optional[str] = Field(None, description="""The text for named object""")
    values: Optional[List[float]] = Field(default_factory=list, description="""The embedding for named object""")


class MetadataObject(ConfiguredBaseModel):

    """
    A metadata object
    """

    key: str = Field(...)
    value: Optional[Any] = Field(None)


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Index.model_rebuild()
Prefix.model_rebuild()
Dataset.model_rebuild()
Model.model_rebuild()
ModelInputMethod.model_rebuild()
NamedObject.model_rebuild()
Embedding.model_rebuild()
MetadataObject.model_rebuild()
