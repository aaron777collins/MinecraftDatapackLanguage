
from .mdl_lexer import MDLLexer, Token, TokenType
from .mdl_parser import MDLParser
from .ast_nodes import *
from .dir_map import DirMap

__all__ = [
    "MDLLexer", "Token", "TokenType",
    "MDLParser",
    "ASTNode", "Program", "PackDeclaration", "NamespaceDeclaration", "TagDeclaration",
    "VariableDeclaration", "VariableAssignment", "VariableSubstitution", "FunctionDeclaration",
    "FunctionCall", "IfStatement", "WhileLoop", "HookDeclaration", "RawBlock",
    "SayCommand", "TellrawCommand", "ExecuteCommand", "ScoreboardCommand",
    "BinaryExpression", "UnaryExpression", "ParenthesizedExpression", "LiteralExpression",
    "ScopeSelector",
    "DirMap"
]

try:
    from ._version import version as __version__   # written by setuptools-scm
except Exception:
    # Fallback for editable dev before _version.py exists
    try:
        from importlib.metadata import version as _pkg_version
        __version__ = _pkg_version("minecraft-datapack-language")
    except Exception:
        __version__ = "0.0.0"