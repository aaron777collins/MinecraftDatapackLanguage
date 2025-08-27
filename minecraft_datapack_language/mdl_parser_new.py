"""
MDL Parser - Proper parsing for MDL language with unlimited nesting support
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from .mdl_lexer import Token, TokenType, lex_mdl

@dataclass
class ASTNode:
    """Base class for AST nodes."""
    pass

@dataclass
class PackDeclaration(ASTNode):
    name: str
    description: str
    pack_format: int
    min_format: Optional[str] = None
    max_format: Optional[str] = None
    min_engine_version: Optional[str] = None

@dataclass
class NamespaceDeclaration(ASTNode):
    name: str

@dataclass
class FunctionDeclaration(ASTNode):
    name: str
    body: List[ASTNode]

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
    condition: str
    body: List[ASTNode]

@dataclass
class FunctionCall(ASTNode):
    function_name: str

@dataclass
class HookDeclaration(ASTNode):
    hook_type: str  # 'tick' or 'load'
    function_name: str

@dataclass
class TagDeclaration(ASTNode):
    tag_type: str
    name: str
    values: List[str]

class MDLParser:
    """Proper parser for MDL language with unlimited nesting support."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.indent_stack = [0]
        
    def parse(self) -> Dict[str, Any]:
        """Parse the tokens into a complete AST."""
        ast = {
            'pack': None,
            'namespaces': [],
            'functions': [],
            'hooks': [],
            'tags': []
        }
        
        while self.current < len(self.tokens):
            token = self._peek()
            if not token:
                break
                
            if token.type == TokenType.PACK:
                ast['pack'] = self._parse_pack_declaration()
            elif token.type == TokenType.NAMESPACE:
                ast['namespaces'].append(self._parse_namespace_declaration())
            elif token.type == TokenType.FUNCTION:
                ast['functions'].append(self._parse_function_declaration())
            elif token.type in [TokenType.ON_TICK, TokenType.ON_LOAD]:
                ast['hooks'].append(self._parse_hook_declaration())
            elif token.type == TokenType.TAG:
                ast['tags'].append(self._parse_tag_declaration())
            else:
                self._advance()  # Skip unknown tokens
        
        return ast
    
    def _peek(self) -> Optional[Token]:
        """Look at the next token without consuming it."""
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None
    
    def _advance(self) -> Token:
        """Consume and return the next token."""
        if self.current < len(self.tokens):
            token = self.tokens[self.current]
            self.current += 1
            return token
        raise ValueError("Unexpected end of tokens")
    
    def _match(self, expected_type: TokenType) -> Token:
        """Match and consume a token of the expected type."""
        token = self._peek()
        if token and token.type == expected_type:
            return self._advance()
        raise ValueError(f"Expected {expected_type}, got {token.type if token else 'EOF'}")
    
    def _parse_pack_declaration(self) -> PackDeclaration:
        """Parse pack declaration."""
        self._match(TokenType.PACK)
        name = self._match(TokenType.STRING).value
        
        # Look for description
        description = ""
        if self._peek() and self._peek().type == TokenType.IDENTIFIER and self._peek().value == "description":
            self._advance()  # consume "description"
            description = self._match(TokenType.STRING).value
        
        self._match(TokenType.IDENTIFIER)  # "pack_format"
        pack_format = int(self._match(TokenType.NUMBER).value)
        
        # Parse optional fields
        min_format = None
        max_format = None
        min_engine_version = None
        
        while self._peek() and self._peek().type == TokenType.IDENTIFIER:
            field = self._peek().value
            if field == "min_format":
                self._advance()
                min_format = self._match(TokenType.STRING).value
            elif field == "max_format":
                self._advance()
                max_format = self._match(TokenType.STRING).value
            elif field == "min_engine_version":
                self._advance()
                min_engine_version = self._match(TokenType.STRING).value
            else:
                break
        
        return PackDeclaration(name, description, pack_format, min_format, max_format, min_engine_version)
    
    def _parse_namespace_declaration(self) -> NamespaceDeclaration:
        """Parse namespace declaration."""
        self._match(TokenType.NAMESPACE)
        name = self._match(TokenType.STRING).value
        return NamespaceDeclaration(name)
    
    def _parse_function_declaration(self) -> FunctionDeclaration:
        """Parse function declaration with unlimited nesting support."""
        self._match(TokenType.FUNCTION)
        name = self._match(TokenType.STRING).value
        self._match(TokenType.COLON)
        
        # Parse function body with proper indentation handling
        body = self._parse_indented_block()
        
        return FunctionDeclaration(name, body)
    
    def _parse_indented_block(self) -> List[ASTNode]:
        """Parse an indented block of statements with unlimited nesting."""
        statements = []
        
        while self.current < len(self.tokens):
            token = self._peek()
            if not token:
                break
            
            # Handle indentation
            if token.type == TokenType.INDENT:
                self._advance()
                continue
            elif token.type == TokenType.DEDENT:
                self._advance()
                break
            elif token.type == TokenType.NEWLINE:
                self._advance()
                continue
            elif token.type == TokenType.EOF:
                break
            
            # Parse statements
            if token.type == TokenType.IF:
                statements.append(self._parse_if_statement())
            elif token.type == TokenType.FOR:
                statements.append(self._parse_for_loop())
            elif token.type == TokenType.WHILE:
                statements.append(self._parse_while_loop())
            elif token.type == TokenType.FUNCTION:
                statements.append(self._parse_function_call())
            elif token.type == TokenType.COMMAND:
                statements.append(self._parse_command())
            else:
                self._advance()  # Skip unknown tokens
        
        return statements
    
    def _parse_if_statement(self) -> IfStatement:
        """Parse if statement with unlimited nesting."""
        self._match(TokenType.IF)
        condition = self._match(TokenType.STRING).value
        self._match(TokenType.COLON)
        
        # Parse if body
        body = self._parse_indented_block()
        
        # Parse elif branches
        elif_branches = []
        while self._peek() and self._peek().type == TokenType.ELSE_IF:
            elif_branches.append(self._parse_elif_branch())
        
        # Parse else branch
        else_body = None
        if self._peek() and self._peek().type == TokenType.ELSE:
            else_body = self._parse_else_branch()
        
        return IfStatement(condition, body, elif_branches, else_body)
    
    def _parse_elif_branch(self) -> ElifBranch:
        """Parse elif branch."""
        self._match(TokenType.ELSE_IF)
        condition = self._match(TokenType.STRING).value
        self._match(TokenType.COLON)
        body = self._parse_indented_block()
        return ElifBranch(condition, body)
    
    def _parse_else_branch(self) -> List[ASTNode]:
        """Parse else branch."""
        self._match(TokenType.ELSE)
        self._match(TokenType.COLON)
        return self._parse_indented_block()
    
    def _parse_for_loop(self) -> ForLoop:
        """Parse for loop with unlimited nesting."""
        self._match(TokenType.FOR)
        variable = self._match(TokenType.IDENTIFIER).value
        self._match(TokenType.IN)
        selector = self._match(TokenType.STRING).value
        self._match(TokenType.COLON)
        
        body = self._parse_indented_block()
        return ForLoop(variable, selector, body)
    
    def _parse_while_loop(self) -> WhileLoop:
        """Parse while loop with unlimited nesting."""
        self._match(TokenType.WHILE)
        condition = self._match(TokenType.STRING).value
        self._match(TokenType.COLON)
        
        body = self._parse_indented_block()
        return WhileLoop(condition, body)
    
    def _parse_function_call(self) -> FunctionCall:
        """Parse function call."""
        self._match(TokenType.FUNCTION)
        function_name = self._match(TokenType.STRING).value
        return FunctionCall(function_name)
    
    def _parse_command(self) -> Command:
        """Parse command."""
        command = self._match(TokenType.COMMAND).value
        return Command(command)
    
    def _parse_hook_declaration(self) -> HookDeclaration:
        """Parse hook declaration."""
        token = self._peek()
        if token.type == TokenType.ON_TICK:
            self._match(TokenType.ON_TICK)
            hook_type = "tick"
        else:
            self._match(TokenType.ON_LOAD)
            hook_type = "load"
        
        function_name = self._match(TokenType.STRING).value
        return HookDeclaration(hook_type, function_name)
    
    def _parse_tag_declaration(self) -> TagDeclaration:
        """Parse tag declaration."""
        self._match(TokenType.TAG)
        tag_type = self._match(TokenType.IDENTIFIER).value
        name = self._match(TokenType.STRING).value
        self._match(TokenType.COLON)
        
        values = []
        while self._peek() and self._peek().type == TokenType.ADD:
            self._match(TokenType.ADD)
            values.append(self._match(TokenType.STRING).value)
        
        return TagDeclaration(tag_type, name, values)

def parse_mdl_new(source: str) -> Dict[str, Any]:
    """Parse MDL source code using the new parser."""
    tokens = lex_mdl(source)
    parser = MDLParser(tokens)
    return parser.parse()
