
from .pack import Pack, Namespace, Function, Tag, Recipe, Advancement, LootTable, Predicate, ItemModifier, Structure, DirMap
__all__ = ["Pack","Namespace","Function","Tag","Recipe","Advancement","LootTable","Predicate","ItemModifier","Structure","DirMap"]
try:
    from ._version import version as __version__   # written by setuptools-scm
except Exception:
    # Fallback for editable dev before _version.py exists
    try:
        from importlib.metadata import version as _pkg_version
        __version__ = _pkg_version("minecraft-datapack-language")
    except Exception:
        __version__ = "0.0.0"