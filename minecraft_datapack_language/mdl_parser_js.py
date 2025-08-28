"""
MDL Parser - JavaScript-style syntax with curly braces and semicolons
Handles unlimited nesting with explicit block boundaries
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Union
from .mdl_lexer_js import Token, TokenType, lex_mdl_js

@dataclass
class ASTNode:
    """Base class for AST nodes."""
    pass

@dataclass
class ArrayLiteral(ASTNode):
    values: List[int]

@dataclass
class PackDeclaration(ASTNode):
    name: str
    description: str
    pack_format: int
    min_format: Optional[ArrayLiteral] = None
    max_format: Optional[ArrayLiteral] = None
    min_engine_version: Optional[str] = None

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
class ForInLoop(ASTNode):
    variable: str
    list_name: str
    body: List[ASTNode]

@dataclass
class WhileLoop(ASTNode):
    condition: str
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
class ImportStatement(ASTNode):
    module_name: str
    imports: List[str]  # List of function names to import

@dataclass
class ExportStatement(ASTNode):
    function_name: str

@dataclass
class VariableDeclaration(ASTNode):
    var_type: str  # 'var', 'let', 'const'
    data_type: str  # 'num', 'str'
    name: str
    value: Optional['Expression'] = None

@dataclass
class VariableAssignment(ASTNode):
    name: str
    value: 'Expression'

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
    type: str  # 'number', 'string', 'identifier'

@dataclass
class VariableExpression(Expression):
    name: str

@dataclass
class ListExpression(Expression):
    elements: List['Expression']

@dataclass
class ListAccessExpression(Expression):
    list_name: str
    index: 'Expression'

@dataclass
class ListAssignmentExpression(Expression):
    list_name: str
    index: 'Expression'
    value: 'Expression'

@dataclass
class BreakStatement(ASTNode):
    pass

@dataclass
class ContinueStatement(ASTNode):
    pass

@dataclass
class ReturnStatement(ASTNode):
    value: Optional[Expression]

@dataclass
class SwitchStatement(ASTNode):
    expression: 'Expression'
    cases: List['SwitchCase']
    default_case: Optional[List[ASTNode]]

@dataclass
class SwitchCase(ASTNode):
    value: 'Expression'
    body: List[ASTNode]

@dataclass
class TryCatchStatement(ASTNode):
    try_body: List[ASTNode]
    catch_body: List[ASTNode]
    error_variable: Optional[str]

@dataclass
class ThrowStatement(ASTNode):
    expression: 'Expression'

@dataclass
class ImportStatement(ASTNode):
    module: str
    alias: Optional[str]
    imports: List[str]

@dataclass
class ListAppendOperation(ASTNode):
    list_name: str
    value: 'Expression'

@dataclass
class ListRemoveOperation(ASTNode):
    list_name: str
    value: 'Expression'

@dataclass
class ListInsertOperation(ASTNode):
    list_name: str
    index: 'Expression'
    value: 'Expression'

@dataclass
class ListPopOperation(ASTNode):
    list_name: str
    index: Optional['Expression'] = None  # Optional index, if not provided pops last element

@dataclass
class ListClearOperation(ASTNode):
    list_name: str

@dataclass
class ListAccessExpression(Expression):
    list_name: str
    index: Expression

@dataclass
class ListLengthExpression(Expression):
    list_name: str

@dataclass
class UnaryExpression(Expression):
    operator: str
    operand: Expression

@dataclass
class BreakStatement(ASTNode):
    pass

@dataclass
class ContinueStatement(ASTNode):
    pass

class MDLParser:
    """Parser for JavaScript-style MDL language with curly braces."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        
    def parse(self) -> Dict[str, Any]:
        """Parse the tokens into a complete AST."""
        ast = {
            'pack': None,
            'namespaces': [],
            'functions': [],
            'hooks': [],
            'tags': []
        }
        
        current_namespace = None
        
        while self.current < len(self.tokens):
            token = self._peek()
            if not token:
                break
                
            if token.type == TokenType.PACK:
                ast['pack'] = self._parse_pack_declaration()
            elif token.type == TokenType.NAMESPACE:
                namespace_decl = self._parse_namespace_declaration()
                current_namespace = namespace_decl.name
                ast['namespaces'].append(namespace_decl)
            elif token.type == TokenType.FUNCTION:
                func_decl = self._parse_function_declaration()
                # Associate function with current namespace
                func_decl.namespace = current_namespace
                ast['functions'].append(func_decl)
            elif token.type in [TokenType.ON_TICK, TokenType.ON_LOAD]:
                ast['hooks'].append(self._parse_hook_declaration())
            elif token.type == TokenType.TAG:
                ast['tags'].append(self._parse_tag_declaration())
            elif token.type == TokenType.IMPORT:
                ast['imports'].append(self._parse_import_statement())
            elif token.type == TokenType.EXPORT:
                ast['exports'].append(self._parse_export_statement())
            elif token.type in [TokenType.VAR, TokenType.LET, TokenType.CONST]:
                # Handle variable declarations at top level (global variables)
                if ast['functions']:
                    ast['functions'][-1].body.append(self._parse_variable_declaration())
                else:
                    # Create a global function to hold top-level variables
                    global_func = FunctionDeclaration("_global_vars", [], [self._parse_variable_declaration()])
                    global_func.namespace = current_namespace
                    ast['functions'].append(global_func)
            else:
                self._advance()  # Skip unknown tokens
        
        return ast
    
    def _peek(self) -> Optional[Token]:
        """Look at the next token without consuming it."""
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None
    
    def _peek_next(self) -> Optional[Token]:
        """Look at the token after the next one without consuming it."""
        if self.current + 1 < len(self.tokens):
            return self.tokens[self.current + 1]
        return None
    
    def _peek_next_n(self, n: int) -> Optional[Token]:
        """Look at the token n positions ahead without consuming it."""
        if self.current + n < len(self.tokens):
            return self.tokens[self.current + n]
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
                min_format = self._parse_array_literal()
            elif field == "max_format":
                self._advance()
                max_format = self._parse_array_literal()
            elif field == "min_engine_version":
                self._advance()
                min_engine_version = self._match(TokenType.STRING).value
            else:
                break
        
        # Expect semicolon
        if self._peek() and self._peek().type == TokenType.SEMICOLON:
            self._advance()
        
        # Skip any newlines after semicolon
        while self._peek() and self._peek().type == TokenType.NEWLINE:
            self._advance()
        
        return PackDeclaration(name, description, pack_format, min_format, max_format, min_engine_version)
    
    def _parse_array_literal(self) -> ArrayLiteral:
        """Parse array literal like [82, 0]."""
        self._match(TokenType.LBRACKET)
        
        values = []
        while self._peek() and self._peek().type != TokenType.RBRACKET:
            if values:  # Not the first element
                self._match(TokenType.COMMA)
            
            # Parse number
            token = self._match(TokenType.NUMBER)
            values.append(int(token.value))
        
        self._match(TokenType.RBRACKET)
        return ArrayLiteral(values)
    
    def _parse_namespace_declaration(self) -> NamespaceDeclaration:
        """Parse namespace declaration."""
        self._match(TokenType.NAMESPACE)
        name = self._match(TokenType.STRING).value
        
        # Expect semicolon
        if self._peek() and self._peek().type == TokenType.SEMICOLON:
            self._advance()
        
        # Skip any newlines after semicolon
        while self._peek() and self._peek().type == TokenType.NEWLINE:
            self._advance()
        
        return NamespaceDeclaration(name)
    
    def _parse_function_declaration(self) -> FunctionDeclaration:
        """Parse function declaration with curly braces."""
        self._match(TokenType.FUNCTION)
        name = self._match(TokenType.STRING).value
        
        # Parse parameters if present
        parameters = []
        if self._peek() and self._peek().type == TokenType.LPAREN:
            self._match(TokenType.LPAREN)
            if self._peek() and self._peek().type != TokenType.RPAREN:
                parameters.append(self._match(TokenType.IDENTIFIER).value)
                while self._peek() and self._peek().type == TokenType.COMMA:
                    self._advance()  # consume comma
                    parameters.append(self._match(TokenType.IDENTIFIER).value)
            self._match(TokenType.RPAREN)
        
        # Expect opening brace
        if self._peek() and self._peek().type == TokenType.LBRACE:
            self._match(TokenType.LBRACE)
            
            # Parse function body
            body = self._parse_block()
            
            self._match(TokenType.RBRACE)
        else:
            # No body, just empty function
            body = []
        
        return FunctionDeclaration(name, parameters, body)
    
    def _parse_block(self) -> List[ASTNode]:
        """Parse a block of statements enclosed in curly braces."""
        statements = []
        
        while self.current < len(self.tokens):
            token = self._peek()
            if not token:
                break
            
            # Skip newlines and comments
            if token.type in [TokenType.NEWLINE, TokenType.COMMENT]:
                self._advance()
                continue
            
            # Check for end of block
            if token.type == TokenType.RBRACE:
                break
            
            # Parse statements
            if token.type == TokenType.IF:
                statements.append(self._parse_if_statement())
            elif token.type == TokenType.FOR:
                statements.append(self._parse_for_loop())
            elif token.type == TokenType.WHILE:
                statements.append(self._parse_while_loop())
            elif token.type == TokenType.SWITCH:
                statements.append(self._parse_switch_statement())
            elif token.type == TokenType.TRY:
                # Try-catch statements need special handling as they span multiple blocks
                # We'll handle this by parsing the entire try-catch structure here
                statements.append(self._parse_try_catch_statement())
            elif token.type == TokenType.BREAK:
                statements.append(self._parse_break_statement())
            elif token.type == TokenType.CONTINUE:
                statements.append(self._parse_continue_statement())
            elif token.type == TokenType.RETURN:
                statements.append(self._parse_return_statement())
            elif token.type == TokenType.THROW:
                statements.append(self._parse_throw_statement())
            elif token.type == TokenType.FUNCTION:
                statements.append(self._parse_function_call())
            elif token.type == TokenType.COMMAND:
                statements.append(self._parse_command())
            elif token.type in [TokenType.VAR, TokenType.LET, TokenType.CONST]:
                statements.append(self._parse_variable_declaration())
            elif token.type == TokenType.IDENTIFIER:
                # Check if this is a variable assignment, function call, or list operation
                next_token = self._peek_next()
                if next_token and next_token.type == TokenType.ASSIGN:
                    statements.append(self._parse_variable_assignment())
                elif next_token and next_token.type == TokenType.DOT:
                    # This might be a list operation like items.append("value")
                    statements.append(self._parse_list_operation())
                elif next_token and next_token.type == TokenType.LPAREN:
                    statements.append(self._parse_function_call_from_identifier())
                else:
                    self._advance()  # Skip unknown tokens
            elif token.type == TokenType.BREAK:
                self._advance()  # consume 'break'
                # Expect semicolon
                if self._peek() and self._peek().type == TokenType.SEMICOLON:
                    self._advance()
                statements.append(BreakStatement())
            elif token.type == TokenType.CONTINUE:
                self._advance()  # consume 'continue'
                # Expect semicolon
                if self._peek() and self._peek().type == TokenType.SEMICOLON:
                    self._advance()
                statements.append(ContinueStatement())
            else:
                self._advance()  # Skip unknown tokens
        
        return statements
    
    def _parse_if_statement(self) -> IfStatement:
        """Parse if statement with curly braces."""
        self._match(TokenType.IF)
        condition = self._match(TokenType.STRING).value
        self._match(TokenType.LBRACE)
        
        # Parse if body
        body = self._parse_block()
        self._match(TokenType.RBRACE)
        
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
        self._match(TokenType.LBRACE)
        body = self._parse_block()
        self._match(TokenType.RBRACE)
        return ElifBranch(condition, body)
    
    def _parse_else_branch(self) -> List[ASTNode]:
        """Parse else branch."""
        self._match(TokenType.ELSE)
        self._match(TokenType.LBRACE)
        body = self._parse_block()
        self._match(TokenType.RBRACE)
        return body
    
    def _parse_for_loop(self) -> Union[ForLoop, ForInLoop]:
        """Parse for loop with curly braces."""
        self._match(TokenType.FOR)
        
        # Check if this is a for-in loop: for (var item in list)
        if self._peek().type == TokenType.LPAREN:
            self._match(TokenType.LPAREN)
            self._match(TokenType.VAR)
            variable = self._match(TokenType.IDENTIFIER).value
            self._match(TokenType.IN)
            list_name = self._match(TokenType.IDENTIFIER).value
            self._match(TokenType.RPAREN)
            
            self._match(TokenType.LBRACE)
            body = self._parse_block()
            self._match(TokenType.RBRACE)
            
            return ForInLoop(variable, list_name, body)
        else:
            # Regular for loop: for variable in selector
            variable = self._match(TokenType.IDENTIFIER).value
            self._match(TokenType.IN)
            
            # Check if the next token is a string (selector) or identifier (list variable)
            token = self._peek()
            if token.type == TokenType.STRING:
                selector = self._match(TokenType.STRING).value
            elif token.type == TokenType.IDENTIFIER:
                # This is a list variable, we'll need to handle it specially
                selector = self._match(TokenType.IDENTIFIER).value
            else:
                raise ValueError(f"Expected STRING or IDENTIFIER after 'in', got {token.type}")
            
            self._match(TokenType.LBRACE)
            
            body = self._parse_block()
            self._match(TokenType.RBRACE)
            
            return ForLoop(variable, selector, body)
    
    def _parse_while_loop(self) -> WhileLoop:
        """Parse while loop with curly braces."""
        self._match(TokenType.WHILE)
        condition = self._match(TokenType.STRING).value
        self._match(TokenType.LBRACE)
        
        body = self._parse_block()
        self._match(TokenType.RBRACE)
        
        return WhileLoop(condition, body)
    
    def _parse_function_call(self) -> FunctionCall:
        """Parse function call."""
        self._match(TokenType.FUNCTION)
        
        # Function names can be either STRING or IDENTIFIER
        token = self._peek()
        if token.type == TokenType.STRING:
            function_name = self._match(TokenType.STRING).value
        elif token.type == TokenType.IDENTIFIER:
            function_name = self._match(TokenType.IDENTIFIER).value
        else:
            raise ValueError(f"Expected STRING or IDENTIFIER for function name, got {token.type}")
        
        # Parse arguments if present
        arguments = []
        if self._peek() and self._peek().type == TokenType.LPAREN:
            self._match(TokenType.LPAREN)
            if self._peek() and self._peek().type != TokenType.RPAREN:
                arguments.append(self._parse_expression())
                while self._peek() and self._peek().type == TokenType.COMMA:
                    self._advance()  # consume comma
                    arguments.append(self._parse_expression())
            self._match(TokenType.RPAREN)
        
        # Expect semicolon
        if self._peek() and self._peek().type == TokenType.SEMICOLON:
            self._advance()
        
        return FunctionCall(function_name, arguments)
    
    def _parse_command(self) -> Command:
        """Parse command."""
        command = self._match(TokenType.COMMAND).value
        
        # Expect semicolon
        if self._peek() and self._peek().type == TokenType.SEMICOLON:
            self._advance()
        
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
        
        # Expect semicolon
        if self._peek() and self._peek().type == TokenType.SEMICOLON:
            self._advance()
        
        return HookDeclaration(hook_type, function_name)
    
    def _parse_tag_declaration(self) -> TagDeclaration:
        """Parse tag declaration."""
        self._match(TokenType.TAG)
        tag_type = self._match(TokenType.IDENTIFIER).value
        # Handle both quoted and unquoted tag names
        if self._peek().type == TokenType.STRING:
            name = self._match(TokenType.STRING).value
        else:
            name = self._match(TokenType.IDENTIFIER).value
        self._match(TokenType.LBRACE)
        
        values = []
        while True:
            # Skip any newlines before checking for ADD
            while self._peek() and self._peek().type == TokenType.NEWLINE:
                self._advance()
            
            # Check if we have an ADD token
            if not self._peek() or self._peek().type != TokenType.ADD:
                break
            
            self._match(TokenType.ADD)
            # Handle both quoted and unquoted values
            if self._peek().type == TokenType.STRING:
                values.append(self._match(TokenType.STRING).value)
            else:
                values.append(self._match(TokenType.IDENTIFIER).value)
            
            # Expect semicolon
            if self._peek() and self._peek().type == TokenType.SEMICOLON:
                self._advance()
            
            # Skip any newlines after semicolon
            while self._peek() and self._peek().type == TokenType.NEWLINE:
                self._advance()
        
        # Skip any newlines before the closing brace
        while self._peek() and self._peek().type == TokenType.NEWLINE:
            self._advance()
        
        self._match(TokenType.RBRACE)
        
        return TagDeclaration(tag_type, name, values)
    
    def _parse_import_statement(self) -> ImportStatement:
        """Parse import statement."""
        self._match(TokenType.IMPORT)
        
        # Parse module name
        module_name = self._match(TokenType.STRING).value
        
        # Parse imports list
        imports = []
        if self._peek() and self._peek().type == TokenType.LBRACE:
            self._match(TokenType.LBRACE)
            if self._peek() and self._peek().type != TokenType.RBRACE:
                imports.append(self._match(TokenType.IDENTIFIER).value)
                while self._peek() and self._peek().type == TokenType.COMMA:
                    self._advance()  # consume comma
                    imports.append(self._match(TokenType.IDENTIFIER).value)
            self._match(TokenType.RBRACE)
        
        # Expect semicolon
        if self._peek() and self._peek().type == TokenType.SEMICOLON:
            self._advance()
        
        return ImportStatement(module_name, imports)
    
    def _parse_export_statement(self) -> ExportStatement:
        """Parse export statement."""
        self._match(TokenType.EXPORT)
        function_name = self._match(TokenType.IDENTIFIER).value
        
        # Expect semicolon
        if self._peek() and self._peek().type == TokenType.SEMICOLON:
            self._advance()
        
        return ExportStatement(function_name)
    
    def _parse_variable_declaration(self) -> VariableDeclaration:
        """Parse variable declaration."""
        var_type = self._advance().value  # var, let, or const
        
        # Parse data type
        if self._peek().type in [TokenType.NUM, TokenType.STR, TokenType.LIST]:
            data_type = self._advance().value
        else:
            data_type = "num"  # Default to number
        
        # Parse variable name
        name = self._match(TokenType.IDENTIFIER).value
        
        # Parse optional assignment
        value = None
        if self._peek() and self._peek().type == TokenType.ASSIGN:
            self._advance()  # consume =
            value = self._parse_expression()
        
        # Expect semicolon
        if self._peek() and self._peek().type == TokenType.SEMICOLON:
            self._advance()
        
        return VariableDeclaration(var_type, data_type, name, value)
    
    def _parse_variable_assignment(self) -> VariableAssignment:
        """Parse variable assignment."""
        name = self._match(TokenType.IDENTIFIER).value
        self._match(TokenType.ASSIGN)  # consume =
        value = self._parse_expression()
        
        # Expect semicolon
        if self._peek() and self._peek().type == TokenType.SEMICOLON:
            self._advance()
        
        return VariableAssignment(name, value)
    
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
        """Parse primary expressions (literals, variables, parenthesized, lists)."""
        token = self._peek()
        
        if token.type == TokenType.NUMBER:
            self._advance()
            return LiteralExpression(token.value, "number")
        elif token.type == TokenType.STRING:
            self._advance()
            return LiteralExpression(token.value, "string")
        elif token.type == TokenType.IDENTIFIER:
            self._advance()
            # Check if this is a function call (identifier followed by ()
            if self._peek() and self._peek().type == TokenType.LPAREN:
                # Parse function call
                arguments = []
                self._advance()  # consume (
                if self._peek() and self._peek().type != TokenType.RPAREN:
                    arguments.append(self._parse_expression())
                    while self._peek() and self._peek().type == TokenType.COMMA:
                        self._advance()  # consume comma
                        arguments.append(self._parse_expression())
                self._match(TokenType.RPAREN)
                return FunctionCall(token.value, arguments)
            # Check if this is a list access (identifier followed by [)
            elif self._peek() and self._peek().type == TokenType.LBRACKET:
                self._advance()  # consume [
                index = self._parse_expression()
                self._match(TokenType.RBRACKET)
                return ListAccessExpression(token.value, index)
            # Check if this is a list length (identifier.length)
            elif self._peek() and self._peek().type == TokenType.DOT:
                self._advance()  # consume .
                if self._peek() and self._peek().type == TokenType.LENGTH:
                    self._advance()  # consume length
                    return ListLengthExpression(token.value)
            return VariableExpression(token.value)
        elif token.type == TokenType.LPAREN:
            self._advance()  # consume (
            expr = self._parse_expression()
            self._match(TokenType.RPAREN)
            return expr
        elif token.type == TokenType.LBRACE:
            # List literal
            return self._parse_list_literal()
        elif token.type == TokenType.LBRACKET:
            # List literal (square brackets)
            return self._parse_list_literal()
        elif token.type == TokenType.MINUS:
            # Handle unary minus (negative numbers)
            self._advance()
            expr = self._parse_primary_expression()
            if isinstance(expr, LiteralExpression) and expr.type == "number":
                return LiteralExpression(-float(expr.value), "number")
            else:
                # For non-number expressions, create a unary expression
                return UnaryExpression("-", expr)
        else:
            raise ValueError(f"Unexpected token in expression: {token.type}")
    
    def _parse_list_literal(self) -> ListExpression:
        """Parse list literal [expr1, expr2, ...]."""
        # Handle both LBRACE and LBRACKET for list literals
        if self._peek().type == TokenType.LBRACE:
            self._match(TokenType.LBRACE)
            closing_token = TokenType.RBRACE
        else:
            self._match(TokenType.LBRACKET)
            closing_token = TokenType.RBRACKET
            
        elements = []
        
        # Parse first element
        if self._peek() and self._peek().type != closing_token:
            elements.append(self._parse_expression())
            
            # Parse remaining elements
            while self._peek() and self._peek().type == TokenType.COMMA:
                self._advance()  # consume comma
                elements.append(self._parse_expression())
        
        # Match the closing bracket/brace
        if closing_token == TokenType.RBRACE:
            self._match(TokenType.RBRACE)
        else:
            self._match(TokenType.RBRACKET)
            
        return ListExpression(elements)
    
    def _parse_break_statement(self) -> BreakStatement:
        """Parse break statement."""
        self._match(TokenType.BREAK)
        if self._peek() and self._peek().type == TokenType.SEMICOLON:
            self._advance()
        return BreakStatement()
    
    def _parse_continue_statement(self) -> ContinueStatement:
        """Parse continue statement."""
        self._match(TokenType.CONTINUE)
        if self._peek() and self._peek().type == TokenType.SEMICOLON:
            self._advance()
        return ContinueStatement()
    
    def _parse_return_statement(self) -> ReturnStatement:
        """Parse return statement."""
        self._match(TokenType.RETURN)
        value = None
        if self._peek() and self._peek().type != TokenType.SEMICOLON:
            value = self._parse_expression()
        if self._peek() and self._peek().type == TokenType.SEMICOLON:
            self._advance()
        return ReturnStatement(value)
    
    def _parse_throw_statement(self) -> ThrowStatement:
        """Parse throw statement."""
        self._match(TokenType.THROW)
        expression = self._parse_expression()
        if self._peek() and self._peek().type == TokenType.SEMICOLON:
            self._advance()
        return ThrowStatement(expression)
    
    def _parse_switch_statement(self) -> SwitchStatement:
        """Parse switch statement."""
        self._match(TokenType.SWITCH)
        self._match(TokenType.LPAREN)
        expression = self._parse_expression()
        self._match(TokenType.RPAREN)
        self._match(TokenType.LBRACE)
        
        cases = []
        default_case = None
        
        while self._peek() and self._peek().type != TokenType.RBRACE:
            if self._peek().type == TokenType.CASE:
                cases.append(self._parse_switch_case())
            elif self._peek().type == TokenType.DEFAULT:
                self._match(TokenType.DEFAULT)
                self._match(TokenType.LBRACE)
                default_case = self._parse_block()
                self._match(TokenType.RBRACE)
            else:
                self._advance()  # Skip unknown tokens
        
        self._match(TokenType.RBRACE)
        return SwitchStatement(expression, cases, default_case)
    
    def _parse_switch_case(self) -> SwitchCase:
        """Parse switch case."""
        self._match(TokenType.CASE)
        value = self._parse_expression()
        self._match(TokenType.LBRACE)
        body = self._parse_block()
        self._match(TokenType.RBRACE)
        return SwitchCase(value, body)
    
    def _parse_try_catch_statement(self) -> TryCatchStatement:
        """Parse try-catch statement."""
        self._match(TokenType.TRY)
        self._match(TokenType.LBRACE)
        
        # Parse try body using the standard block parser
        try_body = self._parse_block()
        self._match(TokenType.RBRACE)
        
        # Skip any newlines before catch
        while self._peek() and self._peek().type == TokenType.NEWLINE:
            self._advance()
        
        self._match(TokenType.CATCH)
        error_variable = None
        if self._peek() and self._peek().type == TokenType.LPAREN:
            self._match(TokenType.LPAREN)
            error_variable = self._match(TokenType.IDENTIFIER).value
            self._match(TokenType.RPAREN)
        
        self._match(TokenType.LBRACE)
        
        # Parse catch body using the standard block parser
        catch_body = self._parse_block()
        self._match(TokenType.RBRACE)
        
        return TryCatchStatement(try_body, catch_body, error_variable)
    
    def _parse_function_call_from_identifier(self) -> FunctionCall:
        """Parse function call that starts with an identifier."""
        function_name = self._match(TokenType.IDENTIFIER).value
        
        # Parse arguments
        arguments = []
        if self._peek() and self._peek().type == TokenType.LPAREN:
            self._match(TokenType.LPAREN)
            if self._peek() and self._peek().type != TokenType.RPAREN:
                arguments.append(self._parse_expression())
                while self._peek() and self._peek().type == TokenType.COMMA:
                    self._advance()  # consume comma
                    arguments.append(self._parse_expression())
            self._match(TokenType.RPAREN)
        
        # Expect semicolon
        if self._peek() and self._peek().type == TokenType.SEMICOLON:
            self._advance()
        
        return FunctionCall(function_name, arguments)

    def _parse_list_operation(self) -> Union[ListAppendOperation, ListRemoveOperation, ListInsertOperation, ListPopOperation, ListClearOperation]:
        """Parse list operation like items.append("value"), items.remove("value"), items.insert(0, "value"), items.pop(), items.clear()."""
        list_name = self._match(TokenType.IDENTIFIER).value
        self._match(TokenType.DOT)  # consume .
        
        # Parse the operation type
        operation_token = self._peek()
        if operation_token.type == TokenType.APPEND:
            self._match(TokenType.APPEND)
        elif operation_token.type == TokenType.REMOVE:
            self._match(TokenType.REMOVE)
        elif operation_token.type == TokenType.INSERT:
            self._match(TokenType.INSERT)
        elif operation_token.type == TokenType.POP:
            self._match(TokenType.POP)
        elif operation_token.type == TokenType.CLEAR:
            self._match(TokenType.CLEAR)
        else:
            raise ValueError(f"Expected 'append', 'remove', 'insert', 'pop', or 'clear', got {operation_token.type}")
        
        # Parse arguments based on operation type
        if operation_token.type == TokenType.CLEAR:
            # clear() takes no arguments
            self._match(TokenType.LPAREN)
            self._match(TokenType.RPAREN)
            if self._peek() and self._peek().type == TokenType.SEMICOLON:
                self._advance()
            return ListClearOperation(list_name)
        
        elif operation_token.type == TokenType.POP:
            # pop() or pop(index)
            self._match(TokenType.LPAREN)
            if self._peek() and self._peek().type != TokenType.RPAREN:
                index = self._parse_expression()
                self._match(TokenType.RPAREN)
                if self._peek() and self._peek().type == TokenType.SEMICOLON:
                    self._advance()
                return ListPopOperation(list_name, index)
            else:
                self._match(TokenType.RPAREN)
                if self._peek() and self._peek().type == TokenType.SEMICOLON:
                    self._advance()
                return ListPopOperation(list_name)
        
        elif operation_token.type == TokenType.INSERT:
            # insert(index, value)
            self._match(TokenType.LPAREN)
            index = self._parse_expression()
            self._match(TokenType.COMMA)
            value = self._parse_expression()
            self._match(TokenType.RPAREN)
            if self._peek() and self._peek().type == TokenType.SEMICOLON:
                self._advance()
            return ListInsertOperation(list_name, index, value)
        
        else:
            # append(value) or remove(value)
            self._match(TokenType.LPAREN)
            value = self._parse_expression()
            self._match(TokenType.RPAREN)
            if self._peek() and self._peek().type == TokenType.SEMICOLON:
                self._advance()
            
            # Return appropriate operation
            if operation_token.type == TokenType.APPEND:
                return ListAppendOperation(list_name, value)
            else:
                return ListRemoveOperation(list_name, value)

def parse_mdl_js(source: str) -> Dict[str, Any]:
    """Parse JavaScript-style MDL source code."""
    tokens = lex_mdl_js(source)
    parser = MDLParser(tokens)
    return parser.parse()
