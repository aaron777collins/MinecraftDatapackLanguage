"""
AST Node Definitions - Data classes for the MDL Abstract Syntax Tree
Updated to match the new language specification
"""

from dataclasses import dataclass
from typing import List, Optional, Any, Union


@dataclass
class ASTNode:
    """Base class for AST nodes."""
    pass


@dataclass
class PackDeclaration(ASTNode):
    """Pack declaration with name, description, and pack format."""
    name: str
    description: str
    pack_format: int


@dataclass
class NamespaceDeclaration(ASTNode):
    """Namespace declaration."""
    name: str


@dataclass
class TagDeclaration(ASTNode):
    """Tag declaration for datapack resources."""
    tag_type: str  # recipe, loot_table, advancement, item_modifier, predicate, structure
    name: str
    file_path: str


@dataclass
class VariableDeclaration(ASTNode):
    """Variable declaration with explicit scope."""
    var_type: str  # num
    name: str
    scope: str  # <@s>, <@a>, <@e[type=armor_stand]>, etc.
    initial_value: Any


@dataclass
class VariableAssignment(ASTNode):
    """Variable assignment with explicit scope."""
    name: str
    scope: str  # <@s>, <@a>, etc.
    value: Any


@dataclass
class VariableSubstitution(ASTNode):
    """Variable substitution for reading values."""
    name: str
    scope: str  # <@s>, <@a>, etc.


@dataclass
class FunctionDeclaration(ASTNode):
    """Function declaration with optional scope."""
    namespace: str
    name: str
    scope: Optional[str]  # Optional scope for the function
    body: List[ASTNode]


@dataclass
class FunctionCall(ASTNode):
    """Function execution with exec keyword."""
    namespace: str
    name: str
    scope: Optional[str]  # Optional scope for the function call


@dataclass
class IfStatement(ASTNode):
    """If statement with condition and bodies."""
    condition: Any  # Expression
    then_body: List[ASTNode]
    else_body: Optional[List[ASTNode]]


@dataclass
class WhileLoop(ASTNode):
    """While loop with condition and body."""
    condition: Any  # Expression
    body: List[ASTNode]


@dataclass
class HookDeclaration(ASTNode):
    """Hook declaration (on_load, on_tick)."""
    hook_type: str  # on_load, on_tick
    namespace: str
    name: str
    scope: Optional[str]  # Optional scope for the hook


@dataclass
class RawBlock(ASTNode):
    """Raw block of Minecraft commands."""
    content: str


@dataclass
class SayCommand(ASTNode):
    """Say command that auto-converts to tellraw."""
    message: str
    variables: List[VariableSubstitution]  # Variables to substitute


@dataclass
class TellrawCommand(ASTNode):
    """Tellraw command with JSON structure."""
    target: str  # @s, @a, etc.
    json_content: str


@dataclass
class ExecuteCommand(ASTNode):
    """Execute command."""
    command: str


@dataclass
class ScoreboardCommand(ASTNode):
    """Scoreboard command."""
    command: str


# Expression nodes
@dataclass
class BinaryExpression(ASTNode):
    """Binary expression with operator."""
    left: Any
    operator: str  # +, -, *, /, ==, !=, >, <, >=, <=
    right: Any


@dataclass
class UnaryExpression(ASTNode):
    """Unary expression."""
    operator: str
    operand: Any


@dataclass
class ParenthesizedExpression(ASTNode):
    """Expression in parentheses."""
    expression: Any


@dataclass
class LiteralExpression(ASTNode):
    """Literal value."""
    value: Union[str, int, float]
    type: str  # string, number


@dataclass
class ScopeSelector(ASTNode):
    """Scope selector like <@s>, <@a[team=red]>."""
    selector: str  # @s, @a[team=red], etc.


@dataclass
class Program(ASTNode):
    """Complete MDL program."""
    pack: Optional[PackDeclaration]
    namespace: Optional[NamespaceDeclaration]
    tags: List[TagDeclaration]
    variables: List[VariableDeclaration]
    functions: List[FunctionDeclaration]
    hooks: List[HookDeclaration]
    statements: List[ASTNode]  # Top-level statements
