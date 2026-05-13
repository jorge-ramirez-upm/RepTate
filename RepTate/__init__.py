__version__: str

try:
    from ._version import version as __version__
except Exception:
    __version__ = "0+unknown"

from .runtime import root_dir
