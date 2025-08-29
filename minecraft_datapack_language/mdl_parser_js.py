"""
MDL Parser - Simplified JavaScript-style syntax with curly braces and semicolons
Handles basic control structures and number variables only
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Union
from .mdl_lexer_js import Token, TokenType, lex_mdl_js

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
    parameters: List[str]
    body: List[ASTNode]
    return_type: Optional[str] = None

@dataclass
class Command(ASTNode):
    command: str

@dataclass
class IfStatement(ASTNode):
    condition: str
    body: List[ASTNode]
    elif_branches: List['ElifBranch']
    else_body: Optional[List[ASTNode]]

@dataclass
class ElifBranch(ASTNode):
    condition: str
    body: List[ASTNode]

@dataclass
class ForLoop(ASTNode):
    variable: str
    selector: str
    body: List[ASTNode]

@dataclass
class WhileLoop(ASTNode):
    condition: 'Expression'  # Changed from str to Expression
    body: List[ASTNode]

@dataclass
class FunctionCall(ASTNode):
    function_name: str
    arguments: List['Expression']

@dataclass
class HookDeclaration(ASTNode):
    hook_type: str  # 'tick' or 'load'
    function_name: str

@dataclass
class TagDeclaration(ASTNode):
    tag_type: str
    name: str
    values: List[str]

@dataclass
class VariableDeclaration(ASTNode):
    var_type: str  # 'var'
    data_type: str  # 'num'
    name: str
    value: Optional['Expression']

@dataclass
class VariableAssignment(ASTNode):
    name: str
    value: 'Expression'

# Expression Nodes
@dataclass
class Expression(ASTNode):
    pass

@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: str
    right: Expression

@dataclass
class LiteralExpression(Expression):
    value: str
    type: str  # 'number'

@dataclass
class VariableExpression(Expression):
    name: str

@dataclass
class VariableSubstitutionExpression(Expression):
    variable_name: str

@dataclass
class ConditionExpression(Expression):
    """Special expression for while loop conditions that contain Minecraft command syntax."""
    condition_string: str


class MDLParser:
    """Parser for simplified MDL language."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
    
    def parse(self) -> Dict[str, Any]:
        """Parse tokens into AST."""
        ast = {
            'pack': None,
            'namespace': None,
            'functions': [],
            'hooks': [],
            'tags': [],
            'imports': [],
            'exports': []
        }
        
        while not self._is_at_end():
            if self._peek().type == TokenType.PACK:
                ast['pack'] = self._parse_pack_declaration()
            elif self._peek().type == TokenType.NAMESPACE:
                ast['namespace'] = self._parse_namespace_declaration()
            elif self._peek().type == TokenType.FUNCTION:
                ast['functions'].append(self._parse_function_declaration())
            elif self._peek().type == TokenType.ON_LOAD:
                ast['hooks'].append(self._parse_hook_declaration())
            elif self._peek().type == TokenType.ON_TICK:
                ast['hooks'].append(self._parse_hook_declaration())
            elif self._peek().type == TokenType.TAG:
                ast['tags'].append(self._parse_tag_declaration())
            else:
                # Skip unknown tokens
                self._advance()
        
        return ast
    
    def _parse_pack_declaration(self) -> PackDeclaration:
        """Parse pack declaration."""
        self._match(TokenType.PACK)
        
        # Parse pack name
        name_token = self._match(TokenType.STRING)
        name = name_token.value.strip('"').strip("'")
        
        # Parse description
        description_token = self._match(TokenType.STRING)
        description = description_token.value.strip('"').strip("'")
        
        # Parse pack_format
        pack_format_token = self._match(TokenType.NUMBER)
        pack_format = int(pack_format_token.value)
        
        self._match(TokenType.SEMICOLON)
        
        return {"name": name, "description": description, "pack_format": pack_format}
    
    def _parse_namespace_declaration(self) -> NamespaceDeclaration:
        """Parse namespace declaration."""
        self._match(TokenType.NAMESPACE)
        
        name_token = self._match(TokenType.STRING)
        name = name_token.value.strip('"').strip("'")
        
        self._match(TokenType.SEMICOLON)
        
        return {"name": name}
    
    def _parse_function_declaration(self) -> FunctionDeclaration:
        """Parse function declaration."""
        self._match(TokenType.FUNCTION)
        
        name_token = self._match(TokenType.STRING)
        name = name_token.value.strip('"').strip("'")
        
        self._match(TokenType.LBRACE)
        
        body = []
        while not self._is_at_end() and self._peek().type != TokenType.RBRACE:
            body.append(self._parse_statement())
        
        self._match(TokenType.RBRACE)
        
        return {"name": name, "body": body}
    
    def _parse_statement(self) -> ASTNode:
        """Parse a statement."""
        if self._peek().type == TokenType.VAR:
            return self._parse_variable_declaration()
        elif self._peek().type == TokenType.IF:
            return self._parse_if_statement()
        elif self._peek().type == TokenType.WHILE:
            return self._parse_while_loop()
        elif self._peek().type == TokenType.FOR:
            return self._parse_for_loop()
        elif self._peek().type == TokenType.FUNCTION:
            return self._parse_function_call()
        elif self._peek().type == TokenType.IDENTIFIER:
            # Check if this is a variable assignment (identifier followed by =)
            if (self.current + 1 < len(self.tokens) and 
                self.tokens[self.current + 1].type == TokenType.ASSIGN):
                return self._parse_variable_assignment()
            else:
                # Assume it's a command
                return self._parse_command()
        else:
            # Assume it's a command
            return self._parse_command()
    
    def _parse_variable_declaration(self) -> VariableDeclaration:
        """Parse variable declaration."""
        self._match(TokenType.VAR)
        
        # Parse data type (only num supported)
        self._match(TokenType.NUM)
        
        # Parse variable name
        name_token = self._match(TokenType.IDENTIFIER)
        name = name_token.value
        
        # Parse assignment
        self._match(TokenType.ASSIGN)
        
        # Parse value
        value = self._parse_expression()
        
        self._match(TokenType.SEMICOLON)
        
        return VariableDeclaration("var", "num", name, value)
    
    def _parse_variable_assignment(self) -> VariableAssignment:
        """Parse variable assignment."""
        name_token = self._match(TokenType.IDENTIFIER)
        name = name_token.value
        
        self._match(TokenType.ASSIGN)
        value = self._parse_expression()
        
        self._match(TokenType.SEMICOLON)
        
        return VariableAssignment(name, value)
    
    def _parse_if_statement(self) -> IfStatement:
        """Parse if statement."""
        self._match(TokenType.IF)
        
        # Parse condition
        condition_token = self._match(TokenType.STRING)
        condition = condition_token.value.strip('"').strip("'")
        
        self._match(TokenType.LBRACE)
        
        # Parse then body
        then_body = []
        while not self._is_at_end() and self._peek().type != TokenType.RBRACE:
            then_body.append(self._parse_statement())
        
        self._match(TokenType.RBRACE)
        
        # Parse else if branches
        elif_branches = []
        while (self._peek().type == TokenType.ELSE and 
               self.current + 1 < len(self.tokens) and
               self.tokens[self.current + 1].type == TokenType.IF):
            elif_branches.append(self._parse_elif_branch())
        
        # Parse else body
        else_body = None
        if self._peek().type == TokenType.ELSE:
            self._match(TokenType.ELSE)
            self._match(TokenType.LBRACE)
            else_body = []
            while not self._is_at_end() and self._peek().type != TokenType.RBRACE:
                else_body.append(self._parse_statement())
            self._match(TokenType.RBRACE)
        
        return IfStatement(condition, then_body, elif_branches, else_body)
    
    def _parse_elif_branch(self) -> ElifBranch:
        """Parse else if branch."""
        self._match(TokenType.ELSE)
        self._match(TokenType.IF)
        
        condition_token = self._match(TokenType.STRING)
        condition = condition_token.value.strip('"').strip("'")
        
        self._match(TokenType.LBRACE)
        
        body = []
        while not self._is_at_end() and self._peek().type != TokenType.RBRACE:
            body.append(self._parse_statement())
        
        self._match(TokenType.RBRACE)
        
        return ElifBranch(condition, body)
    
    def _parse_while_loop(self) -> WhileLoop:
        """Parse while loop."""
        self._match(TokenType.WHILE)
        
        # Parse condition
        condition_token = self._match(TokenType.STRING)
        condition = ConditionExpression(condition_token.value.strip('"').strip("'"))
        
        self._match(TokenType.LBRACE)
        
        body = []
        while not self._is_at_end() and self._peek().type != TokenType.RBRACE:
            body.append(self._parse_statement())
        
        self._match(TokenType.RBRACE)
        
        return WhileLoop(condition, body)
    
    def _parse_for_loop(self) -> ForLoop:
        """Parse for loop."""
        self._match(TokenType.FOR)
        
        variable_token = self._match(TokenType.IDENTIFIER)
        variable = variable_token.value
        
        self._match(TokenType.IN)
        
        selector_token = self._match(TokenType.STRING)
        selector = selector_token.value.strip('"').strip("'")
        
        self._match(TokenType.LBRACE)
        
        body = []
        while not self._is_at_end() and self._peek().type != TokenType.RBRACE:
            body.append(self._parse_statement())
        
        self._match(TokenType.RBRACE)
        
        return ForLoop(variable, selector, body)
    
    def _parse_function_call(self) -> FunctionCall:
        """Parse function call."""
        self._match(TokenType.FUNCTION)
        
        name_token = self._match(TokenType.STRING)
        name = name_token.value.strip('"').strip("'")
        
        self._match(TokenType.SEMICOLON)
        
        return FunctionCall(name, [])
    
    def _parse_command(self) -> Command:
        """Parse a command."""
        command_parts = []
        
        while not self._is_at_end() and self._peek().type != TokenType.SEMICOLON:
            command_parts.append(self._advance().value)
        
        if not self._is_at_end():
            self._match(TokenType.SEMICOLON)
        
        command = " ".join(command_parts)
        return Command(command)
    
    def _parse_hook_declaration(self) -> Dict[str, str]:
        """Parse hook declaration."""
        if self._peek().type == TokenType.ON_LOAD:
            self._match(TokenType.ON_LOAD)
            hook_type = "load"
        else:
            self._match(TokenType.ON_TICK)
            hook_type = "tick"
        
        function_name_token = self._match(TokenType.STRING)
        function_name = function_name_token.value.strip('"').strip("'")
        
        self._match(TokenType.SEMICOLON)
        
        return {"hook_type": hook_type, "function_name": function_name}
    
    def _parse_tag_declaration(self) -> Dict[str, Any]:
        """Parse tag declaration."""
        self._match(TokenType.TAG)
        
        tag_type_token = self._match(TokenType.IDENTIFIER)
        tag_type = tag_type_token.value
        
        name_token = self._match(TokenType.IDENTIFIER)
        name = name_token.value
        
        self._match(TokenType.LBRACE)
        
        values = []
        while not self._is_at_end() and self._peek().type != TokenType.RBRACE:
            if self._peek().type == TokenType.ADD:
                self._match(TokenType.ADD)
                value_token = self._match(TokenType.STRING)
                values.append(value_token.value.strip('"').strip("'"))
                self._match(TokenType.SEMICOLON)
            else:
                self._advance()
        
        self._match(TokenType.RBRACE)
        
        return {"tag_type": tag_type, "name": name, "values": values}
    
    def _parse_expression(self) -> Expression:
        """Parse an expression."""
        return self._parse_assignment_expression()
    
    def _parse_assignment_expression(self) -> Expression:
        """Parse assignment expression."""
        left = self._parse_logical_expression()
        
        if self._peek() and self._peek().type == TokenType.ASSIGN:
            self._advance()  # consume =
            right = self._parse_assignment_expression()
            return BinaryExpression(left, "=", right)
        
        return left
    
    def _parse_additive_expression(self) -> Expression:
        """Parse additive expressions (+, -)."""
        left = self._parse_multiplicative_expression()
        
        while self._peek() and self._peek().type in [TokenType.PLUS, TokenType.MINUS]:
            operator = self._advance().value
            right = self._parse_multiplicative_expression()
            left = BinaryExpression(left, operator, right)
        
        return left
    
    def _parse_comparison_expression(self) -> Expression:
        """Parse comparison expressions (==, !=, <, <=, >, >=)."""
        left = self._parse_additive_expression()
        
        while self._peek() and self._peek().type in [
            TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS, 
            TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL
        ]:
            operator = self._advance().value
            right = self._parse_additive_expression()
            left = BinaryExpression(left, operator, right)
        
        return left
    
    def _parse_logical_expression(self) -> Expression:
        """Parse logical expressions (&&, ||)."""
        left = self._parse_comparison_expression()
        
        while self._peek() and self._peek().type in [TokenType.AND, TokenType.OR]:
            operator = self._advance().value
            right = self._parse_comparison_expression()
            left = BinaryExpression(left, operator, right)
        
        return left
    
    def _parse_multiplicative_expression(self) -> Expression:
        """Parse multiplicative expressions (*, /, %)."""
        left = self._parse_primary_expression()
        
        while self._peek() and self._peek().type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]:
            operator = self._advance().value
            right = self._parse_primary_expression()
            left = BinaryExpression(left, operator, right)
        
        return left
    
    def _parse_primary_expression(self) -> Expression:
        """Parse primary expressions (literals, variables, parenthesized)."""
        token = self._peek()
        
        if token.type == TokenType.NUMBER:
            self._advance()
            return LiteralExpression(token.value, "number")
        elif token.type == TokenType.STRING:
            self._advance()
            return LiteralExpression(token.value, "string")
        elif token.type == TokenType.VARIABLE_SUB:
            self._advance()
            return VariableSubstitutionExpression(token.value)
        elif token.type == TokenType.IDENTIFIER:
            identifier_name = token.value
            self._advance()  # consume the identifier
            return VariableExpression(identifier_name)
        elif token.type == TokenType.LPAREN:
            self._advance()  # consume (
            expr = self._parse_expression()
            self._match(TokenType.RPAREN)
            return expr
        else:
            # Unknown token - create a literal expression
            self._advance()
            return LiteralExpression(token.value, "unknown")
    
    def _match(self, expected_type: TokenType) -> Token:
        """Match and consume a token of the expected type."""
        if self._is_at_end():
            raise RuntimeError(f"Unexpected end of input, expected {expected_type}")
        
        token = self._peek()
        if token.type == expected_type:
            return self._advance()
        else:
            raise RuntimeError(f"Expected {expected_type}, got {token.type}")
    
    def _advance(self) -> Token:
        """Advance to the next token."""
        if not self._is_at_end():
            self.current += 1
        return self.tokens[self.current - 1]
    
    def _peek(self) -> Token:
        """Peek at the current token."""
        if self._is_at_end():
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.current]
    
    def _is_at_end(self) -> bool:
        """Check if we're at the end of the tokens."""
        return self.current >= len(self.tokens)


def parse_mdl_js(source: str) -> Dict[str, Any]:
    """Parse JavaScript-style MDL source code into AST."""
    tokens = lex_mdl_js(source)
    parser = MDLParser(tokens)
    return parser.parse()
