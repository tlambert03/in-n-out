"""plugable dependency injection and result processing."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("in-n-out")
except PackageNotFoundError:
    __version__ = "uninstalled"
__author__ = "Talley Lambert"
__email__ = "talley.lambert@gmail.com"

from ._inject import inject_dependencies
from ._processors import get_processor, set_processors
from ._providers import get_provider, provider, set_providers
from ._type_resolution import (
    resolve_single_type_hints,
    resolve_type_hints,
    type_resolved_signature,
)

__all__ = [
    "get_processor",
    "get_provider",
    "inject_dependencies",
    "provider",
    "resolve_single_type_hints",
    "resolve_type_hints",
    "set_processors",
    "set_providers",
    "type_resolved_signature",
]
