"""venomx package."""

import importlib_metadata

from venomx.model.venomx import Embedding, Index, NamedObject

try:
    __version__ = importlib_metadata.version(__name__)
except importlib_metadata.PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"  # pragma: no cover

__all__ = [
    "Index",
    "Embedding",
    "NamedObject",
]
