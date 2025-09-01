"""
AST Node Definitions - Data classes for the MDL Abstract Syntax Tree
"""

from dataclasses import dataclass
from typing import List, Optional, Any


@dataclass
class ASTNode:
    """Base class for AST nodes."""
    pass


@dataclass
class PackDeclaration(ASTNode):
    name: str
    description: str
    pack_format: int


@dataclass
class NamespaceDeclaration(ASTNode):
    name: str


@dataclass
class FunctionDeclaration(ASTNode):
    name: str
    body: List[Any]


@dataclass
class VariableDeclaration(ASTNode):
    name: str
    scope: Optional[str]
    value: Any


@dataclass
class VariableAssignment(ASTNode):
    name: str
    value: Any


@dataclass
class IfStatement(ASTNode):
    condition: str
    then_body: List[Any]
    else_body: Optional[List[Any]]


@dataclass
class WhileLoop(ASTNode):
    condition: str
    method: Optional[str]
    body: List[Any]


@dataclass
class FunctionCall(ASTNode):
    name: str


@dataclass
class ExecuteStatement(ASTNode):
    command: str


@dataclass
class RawText(ASTNode):
    content: str


@dataclass
class Command(ASTNode):
    command: str


@dataclass
class VariableExpression(ASTNode):
    name: str


@dataclass
class VariableSubstitutionExpression(ASTNode):
    name: str
    scope: Optional[str]


@dataclass
class LiteralExpression(ASTNode):
    value: str
    type: str


@dataclass
class BinaryExpression(ASTNode):
    left: Any
    operator: str
    right: Any


@dataclass
class HookDeclaration(ASTNode):
    hook_type: str
    function_name: str


@dataclass
class TagDeclaration(ASTNode):
    tag_type: str
    name: str
    values: List[str]


@dataclass
class RecipeDeclaration(ASTNode):
    name: str
    file_path: str


@dataclass
class LootTableDeclaration(ASTNode):
    name: str
    file_path: str


@dataclass
class AdvancementDeclaration(ASTNode):
    name: str
    file_path: str


@dataclass
class PredicateDeclaration(ASTNode):
    name: str
    file_path: str


@dataclass
class ItemModifierDeclaration(ASTNode):
    name: str
    file_path: str


@dataclass
class StructureDeclaration(ASTNode):
    name: str
    file_path: str
