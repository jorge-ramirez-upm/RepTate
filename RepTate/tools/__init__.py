from . import polymer_data as polymer_data
import sys as _sys

_LEGACY_POLYMER_DATA_MODULE: str = "polymer_data"
_sys.modules.setdefault(_LEGACY_POLYMER_DATA_MODULE, polymer_data)
