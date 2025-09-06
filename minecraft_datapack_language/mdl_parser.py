"""
MDL Parser - Parses MDL source code into an Abstract Syntax Tree
Implements the complete language specification from language-reference.md
"""

from typing import List, Optional, Dict, Any, Union
from .mdl_lexer import Token, TokenType, MDLLexer
from .mdl_errors import MDLParserError
from .ast_nodes import (
    ASTNode, Program, PackDeclaration, NamespaceDeclaration, TagDeclaration,
    VariableDeclaration, VariableAssignment, VariableSubstitution, FunctionDeclaration,
    FunctionCall, IfStatement, WhileLoop, HookDeclaration, RawBlock,
    SayCommand, TellrawCommand, ExecuteCommand, ScoreboardCommand,
    BinaryExpression, UnaryExpression, ParenthesizedExpression, LiteralExpression,
    ScopeSelector, MacroLine, VerbatimLine
)


class MDLParser:
    """
    Parser for the MDL language.
    
    Features:
    - Full support for all language constructs from the specification
    - Proper scope handling for variables
    - Tag declarations for datapack resources
    - Say command auto-conversion to tellraw
    - Comprehensive error handling with context
    """
    
    def __init__(self, source_file: str = None):
        self.source_file = source_file
        self.tokens: List[Token] = []
        self.current = 0
        self.current_namespace = "mdl"
    
    def parse(self, source: str) -> Program:
        """
        Parse MDL source code into an AST.
        
        Args:
            source: The MDL source code string
            
        Returns:
            Program AST node representing the complete program
            
        Raises:
            MDLParserError: If there's a parsing error
        """
        # Lex the source into tokens
        lexer = MDLLexer(self.source_file)
        self.tokens = lexer.lex(source)
        self.current = 0
        
        # Parse the program
        return self._parse_program()
    
    def _parse_program(self) -> Program:
        """Parse the complete program."""
        pack = None
        namespace = None
        tags = []
        variables = []
        functions = []
        hooks = []
        statements = []
        
        while not self._is_at_end():
            try:
                if self._peek().type == TokenType.PACK:
                    pack = self._parse_pack_declaration()
                elif self._peek().type == TokenType.NAMESPACE:
                    namespace = self._parse_namespace_declaration()
                elif self._peek().type == TokenType.TAG:
                    tags.append(self._parse_tag_declaration())
                elif self._peek().type == TokenType.VAR:
                    variables.append(self._parse_variable_declaration())
                elif self._peek().type == TokenType.FUNCTION:
                    functions.append(self._parse_function_declaration())
                elif self._peek().type == TokenType.ON_LOAD:
                    hooks.append(self._parse_hook_declaration())
                elif self._peek().type == TokenType.ON_TICK:
                    hooks.append(self._parse_hook_declaration())
                elif self._peek().type == TokenType.EXEC:
                    statements.append(self._parse_function_call())
                elif self._peek().type == TokenType.IF:
                    statements.append(self._parse_if_statement())
                elif self._peek().type == TokenType.WHILE:
                    statements.append(self._parse_while_loop())
                elif self._peek().type == TokenType.DOLLAR and self._peek(1).type == TokenType.EXCLAMATION:
                    statements.append(self._parse_raw_block())
                elif self._peek().type == TokenType.MACRO_LINE:
                    # Function macro raw line (beginning with $)
                    statements.append(self._parse_macro_line())
                elif self._peek().type == TokenType.IDENTIFIER:
                    # Could be a variable assignment or say command
                    if self._peek().value == "say":
                        statements.append(self._parse_say_command())
                    else:
                        statements.append(self._parse_variable_assignment())
                else:
                    # Skip unknown tokens (comments, whitespace, etc.)
                    self._advance()
            except Exception as e:
                if isinstance(e, MDLParserError):
                    raise e
                else:
                    self._error(f"Unexpected error during parsing: {str(e)}", "Check the syntax")
        
        return Program(
            pack=pack,
            namespace=namespace,
            tags=tags,
            variables=variables,
            functions=functions,
            hooks=hooks,
            statements=statements
        )
    
    def _parse_pack_declaration(self) -> PackDeclaration:
        """Parse pack declaration: pack "name" "description" format;"""
        self._expect(TokenType.PACK, "Expected 'pack' keyword")
        
        self._expect(TokenType.QUOTE, "Expected opening quote for pack name")
        name = self._expect_identifier("Expected pack name")
        self._expect(TokenType.QUOTE, "Expected closing quote for pack name")
        
        self._expect(TokenType.QUOTE, "Expected opening quote for pack description")
        description = self._expect_identifier("Expected pack description")
        self._expect(TokenType.QUOTE, "Expected closing quote for pack description")
        
        self._expect(TokenType.NUMBER, "Expected pack format number")
        pack_format = int(self._previous().value)
        
        self._expect(TokenType.SEMICOLON, "Expected semicolon after pack declaration")
        
        return PackDeclaration(name=name, description=description, pack_format=pack_format)
    
    def _parse_namespace_declaration(self) -> NamespaceDeclaration:
        """Parse namespace declaration: namespace "name";"""
        self._expect(TokenType.NAMESPACE, "Expected 'namespace' keyword")
        
        self._expect(TokenType.QUOTE, "Expected opening quote for namespace name")
        name = self._expect_identifier("Expected namespace name")
        self._expect(TokenType.QUOTE, "Expected closing quote for namespace name")
        
        self._expect(TokenType.SEMICOLON, "Expected semicolon after namespace declaration")
        
        # Update current namespace
        self.current_namespace = name
        
        return NamespaceDeclaration(name=name)
    
    def _parse_tag_declaration(self) -> TagDeclaration:
        """Parse tag declaration: tag type "name" "path";"""
        self._expect(TokenType.TAG, "Expected 'tag' keyword")
        
        # Parse tag type
        tag_type = self._parse_tag_type()
        
        self._expect(TokenType.QUOTE, "Expected opening quote for tag name")
        name = self._expect_identifier("Expected tag name")
        self._expect(TokenType.QUOTE, "Expected closing quote for tag name")
        
        self._expect(TokenType.QUOTE, "Expected opening quote for file path")
        file_path = self._expect_identifier("Expected file path")
        self._expect(TokenType.QUOTE, "Expected closing quote for file path")
        
        self._expect(TokenType.SEMICOLON, "Expected semicolon after tag declaration")
        
        return TagDeclaration(tag_type=tag_type, name=name, file_path=file_path)
    
    def _parse_tag_type(self) -> str:
        """Parse tag type (recipe, loot_table, etc.)."""
        token = self._peek()
        if token.type in [TokenType.RECIPE, TokenType.LOOT_TABLE, TokenType.ADVANCEMENT,
                         TokenType.ITEM_MODIFIER, TokenType.PREDICATE, TokenType.STRUCTURE]:
            self._advance()
            return token.value
        else:
            self._error(f"Expected tag type, got {token.value}", 
                       "Use: recipe, loot_table, advancement, item_modifier, predicate, or structure")
    
    def _parse_variable_declaration(self) -> VariableDeclaration:
        """Parse variable declaration: var num name<scope> = value;"""
        self._expect(TokenType.VAR, "Expected 'var' keyword")
        
        self._expect(TokenType.NUM, "Expected 'num' keyword")
        
        name = self._expect_identifier("Expected variable name")
        
        scope = self._parse_scope_selector()
        
        self._expect(TokenType.ASSIGN, "Expected '=' after variable declaration")
        
        initial_value = self._parse_expression()
        
        self._expect(TokenType.SEMICOLON, "Expected semicolon after variable declaration")
        
        return VariableDeclaration(
            var_type="num",
            name=name,
            scope=scope,
            initial_value=initial_value
        )
    
    def _parse_variable_assignment(self) -> VariableAssignment:
        """Parse variable assignment: name<scope> = value;"""
        name = self._expect_identifier("Expected variable name")
        
        scope = self._parse_scope_selector()
        
        self._expect(TokenType.ASSIGN, "Expected '=' after variable name")
        
        value = self._parse_expression()
        
        self._expect(TokenType.SEMICOLON, "Expected semicolon after variable assignment")
        
        return VariableAssignment(name=name, scope=scope, value=value)
    
    def _parse_scope_selector(self) -> str:
        """Parse scope selector: <@s>, <@a[team=red]>, etc."""
        self._expect(TokenType.LANGLE, "Expected '<' for scope selector")
        
        # Parse the selector content
        selector_content = ""
        while not self._is_at_end() and self._peek().type != TokenType.RANGLE:
            selector_content += self._peek().value
            self._advance()
        
        self._expect(TokenType.RANGLE, "Expected '>' to close scope selector")
        
        return f"<{selector_content}>"
    
    def _parse_function_declaration(self) -> FunctionDeclaration:
        """Parse function declaration: function namespace:name<scope> { body }"""
        self._expect(TokenType.FUNCTION, "Expected 'function' keyword")
        
        # Parse namespace:name
        namespace = self._expect_identifier("Expected namespace")
        self._expect(TokenType.COLON, "Expected ':' after namespace")
        name = self._expect_identifier("Expected function name")
        
        # Parse optional scope
        scope = None
        if self._peek().type == TokenType.LANGLE:
            scope = self._parse_scope_selector()
        
        self._expect(TokenType.LBRACE, "Expected '{' to start function body")
        
        body = self._parse_block()
        
        self._expect(TokenType.RBRACE, "Expected '}' to end function body")
        
        return FunctionDeclaration(
            namespace=namespace,
            name=name,
            scope=scope,
            body=body
        )
    
    def _parse_function_call(self) -> FunctionCall:
        """Parse function call: exec namespace:name<scope> [compound_string | with clause];"""
        self._expect(TokenType.EXEC, "Expected 'exec' keyword")
        
        # Parse namespace:name
        namespace = self._expect_identifier("Expected namespace")
        self._expect(TokenType.COLON, "Expected ':' after namespace")
        name = self._expect_identifier("Expected function name")
        
        # Parse optional scope
        scope = None
        if self._peek().type == TokenType.LANGLE:
            scope = self._parse_scope_selector()
        
        # Optional compound string or with clause
        compound = None
        with_clause = None
        
        # exec ns:name<scope> "{...json...}";
        if self._peek().type == TokenType.QUOTE and self._peek(1).type == TokenType.IDENTIFIER and self._peek(2).type == TokenType.QUOTE:
            self._advance()  # opening quote
            compound = self._expect_identifier("Expected compound JSON string content")
            self._expect(TokenType.QUOTE, "Expected closing quote for compound JSON")
        # exec ns:name<scope> with <data source/path tokens...>;
        elif self._peek().type == TokenType.WITH:
            self._advance()  # consume 'with'
            # Accumulate raw token values until ';'
            parts = []
            while not self._is_at_end() and self._peek().type != TokenType.SEMICOLON:
                parts.append(self._peek().value)
                self._advance()
            with_clause = " ".join(parts).strip()
        
        self._expect(TokenType.SEMICOLON, "Expected semicolon after function call")
        
        return FunctionCall(
            namespace=namespace,
            name=name,
            scope=scope,
            compound=compound,
            with_clause=with_clause
        )
    
    def _parse_if_statement(self) -> IfStatement:
        """Parse if statement: if condition { then_body } else { else_body } or else if { ... }"""
        self._expect(TokenType.IF, "Expected 'if' keyword")
        
        condition = self._parse_expression()
        
        self._expect(TokenType.LBRACE, "Expected '{' to start if body")
        then_body = self._parse_block()
        self._expect(TokenType.RBRACE, "Expected '}' to end if body")
        
        # Parse optional else clause
        else_body = None
        if self._peek().type == TokenType.ELSE:
            self._advance()  # consume 'else'
            
            # Check if this is an else if
            if self._peek().type == TokenType.IF:
                # This is an else if - parse it as a nested if statement
                else_body = [self._parse_if_statement()]
            else:
                # This is a regular else
                self._expect(TokenType.LBRACE, "Expected '{' to start else body")
                else_body = self._parse_block()
                self._expect(TokenType.RBRACE, "Expected '}' to end else body")
        
        return IfStatement(
            condition=condition,
            then_body=then_body,
            else_body=else_body
        )
    
    def _parse_while_loop(self) -> WhileLoop:
        """Parse while loop: while condition { body }"""
        self._expect(TokenType.WHILE, "Expected 'while' keyword")
        
        condition = self._parse_expression()
        
        self._expect(TokenType.LBRACE, "Expected '{' to start while body")
        body = self._parse_block()
        self._expect(TokenType.RBRACE, "Expected '}' to end while body")
        
        return WhileLoop(condition=condition, body=body)
    
    def _parse_hook_declaration(self) -> HookDeclaration:
        """Parse hook declaration: on_load/on_tick namespace:name<scope>;"""
        hook_type = self._peek().value
        self._advance()  # consume on_load or on_tick
        
        # Parse namespace:name
        namespace = self._expect_identifier("Expected namespace")
        self._expect(TokenType.COLON, "Expected ':' after namespace")
        name = self._expect_identifier("Expected function name")
        
        # Parse optional scope
        scope = None
        if self._peek().type == TokenType.LANGLE:
            scope = self._parse_scope_selector()
        
        self._expect(TokenType.SEMICOLON, "Expected semicolon after hook declaration")
        
        return HookDeclaration(
            hook_type=hook_type,
            namespace=namespace,
            name=name,
            scope=scope
        )
    
    def _parse_raw_block(self) -> RawBlock:
        """Parse raw block: $!raw ... raw!$"""
        # Consume $!raw
        self._expect(TokenType.DOLLAR, "Expected '$' to start raw block")
        self._expect(TokenType.EXCLAMATION, "Expected '!' after '$' in raw block")
        self._expect(TokenType.IDENTIFIER, "Expected 'raw' keyword")
        
        # Look for RAW_CONTENT token
        if self._peek().type == TokenType.RAW_CONTENT:
            content = self._peek().value
            self._advance()
        else:
            content = ""
        
        # Consume raw!$ end marker
        self._expect(TokenType.IDENTIFIER, "Expected 'raw' to end raw block")
        self._expect(TokenType.EXCLAMATION, "Expected '!' to end raw block")
        self._expect(TokenType.DOLLAR, "Expected '$' to end raw block")
        
        return RawBlock(content=content)
    
    def _parse_say_command(self) -> SayCommand:
        """Parse say command: say "message with $variable<scope>$";"""
        self._expect(TokenType.IDENTIFIER, "Expected 'say' keyword")
        
        self._expect(TokenType.QUOTE, "Expected opening quote for say message")
        
        # Get the string content (which includes variable substitutions)
        if self._peek().type == TokenType.IDENTIFIER:
            message = self._peek().value
            self._advance()
        else:
            message = ""
        
        # Extract variables from the message content
        variables = []
        # Simple regex-like extraction of $variable<scope>$ patterns
        import re
        var_pattern = r'\$([a-zA-Z_][a-zA-Z0-9_]*<[^>]+>)\$'
        matches = re.findall(var_pattern, message)
        
        for match in matches:
            # Parse the variable name and scope from the match
            if '<' in match and '>' in match:
                name = match[:match.index('<')]
                scope = match[match.index('<'):match.index('>')+1]
                variables.append(VariableSubstitution(name=name, scope=scope))
        
        self._expect(TokenType.QUOTE, "Expected closing quote for say message")
        self._expect(TokenType.SEMICOLON, "Expected semicolon after say command")
        
        return SayCommand(message=message, variables=variables)
    
    def _parse_variable_substitution(self) -> VariableSubstitution:
        """Parse variable substitution: $variable<scope>$"""
        self._expect(TokenType.DOLLAR, "Expected '$' to start variable substitution")
        
        name = self._expect_identifier("Expected variable name")
        
        # For variable substitutions, use LANGLE/RANGLE
        self._expect(TokenType.LANGLE, "Expected '<' for scope selector")
        
        # Parse the selector content
        selector_content = ""
        while not self._is_at_end() and self._peek().type != TokenType.RANGLE:
            selector_content += self._peek().value
            self._advance()
        
        self._expect(TokenType.RANGLE, "Expected '>' to close scope selector")
        
        scope = f"<{selector_content}>"
        
        self._expect(TokenType.DOLLAR, "Expected '$' to end variable substitution")
        
        return VariableSubstitution(name=name, scope=scope)
    
    def _parse_expression(self) -> Any:
        """Parse an expression with operator precedence."""
        return self._parse_comparison()
    
    def _parse_comparison(self) -> Any:
        """Parse comparison expressions (>, <, >=, <=, ==, !=)."""
        expr = self._parse_term()
        
        while not self._is_at_end() and self._peek().type in [
            TokenType.GREATER, TokenType.LESS, TokenType.GREATER_EQUAL, 
            TokenType.LESS_EQUAL, TokenType.EQUAL, TokenType.NOT_EQUAL
        ]:
            operator = self._peek().type
            self._advance()
            right = self._parse_term()
            expr = BinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_term(self) -> Any:
        """Parse addition and subtraction terms."""
        expr = self._parse_factor()
        
        while not self._is_at_end() and self._peek().type in [TokenType.PLUS, TokenType.MINUS]:
            operator = self._peek().type
            self._advance()
            right = self._parse_factor()
            expr = BinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_factor(self) -> Any:
        """Parse multiplication and division factors."""
        expr = self._parse_primary()
        
        while not self._is_at_end() and self._peek().type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            operator = self._peek().type
            self._advance()
            right = self._parse_primary()
            expr = BinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_primary(self) -> Any:
        """Parse primary expressions (literals, variables, parenthesized expressions)."""
        if self._peek().type == TokenType.DOLLAR:
            return self._parse_variable_substitution()
        elif self._peek().type == TokenType.NUMBER:
            value = float(self._peek().value)
            self._advance()
            return LiteralExpression(value=value, type="number")
        elif self._peek().type == TokenType.QUOTE:
            self._advance()  # consume opening quote
            value = self._expect_identifier("Expected string content")
            self._expect(TokenType.QUOTE, "Expected closing quote")
            return LiteralExpression(value=value, type="string")
        elif self._peek().type == TokenType.LPAREN:
            self._advance()  # consume opening parenthesis
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN, "Expected closing parenthesis")
            return ParenthesizedExpression(expression=expr)
        else:
            # Simple identifier
            value = self._expect_identifier("Expected expression")
            return LiteralExpression(value=value, type="identifier")
    
    def _parse_block(self) -> List[ASTNode]:
        """Parse a block of statements."""
        statements = []
        
        while not self._is_at_end() and self._peek().type != TokenType.RBRACE:
            if self._peek().type == TokenType.IF:
                statements.append(self._parse_if_statement())
            elif self._peek().type == TokenType.WHILE:
                statements.append(self._parse_while_loop())
            elif self._peek().type == TokenType.EXEC:
                statements.append(self._parse_function_call())
            elif self._peek().type == TokenType.DOLLAR and self._peek(1).type == TokenType.EXCLAMATION:
                statements.append(self._parse_raw_block())
            elif self._peek().type == TokenType.MACRO_LINE:
                statements.append(self._parse_macro_line())
            elif self._peek().type == TokenType.IDENTIFIER:
                if self._peek().value == "say":
                    statements.append(self._parse_say_command())
                else:
                    # Fallback: parse as assignment; if it fails later in compiler,
                    # compiler will treat lines containing $(...) specially.
                    statements.append(self._parse_variable_assignment())
            else:
                # Skip unknown tokens
                self._advance()
        
        return statements

    def _parse_macro_line(self) -> MacroLine:
        """Parse a function macro raw line token into an AST node."""
        token = self._expect(TokenType.MACRO_LINE, "Expected macro line starting with '$'")
        return MacroLine(content=token.value)
    
    # Helper methods
    def _advance(self) -> Token:
        """Advance to next token and return the previous one."""
        if not self._is_at_end():
            self.current += 1
        return self._previous()
    
    def _peek(self, offset: int = 0) -> Token:
        """Peek ahead by offset tokens."""
        if self.current + offset >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.current + offset]
    
    def _previous(self) -> Token:
        """Get the previous token."""
        return self.tokens[self.current - 1]
    
    def _is_at_end(self) -> bool:
        """Check if we're at the end of tokens."""
        return self.current >= len(self.tokens) or self._peek().type == TokenType.EOF
    
    def _expect(self, token_type: str, message: str) -> Token:
        """Expect a specific token type and return it."""
        if self._is_at_end():
            self._error(f"Unexpected end of file, {message}", "Add the missing token")
        
        if self._peek().type == token_type:
            return self._advance()
        else:
            self._error(f"Expected {token_type}, got {self._peek().type}", message)
    
    def _expect_identifier(self, message: str) -> str:
        """Expect an identifier token and return its value."""
        token = self._peek()
        if token.type == TokenType.IDENTIFIER:
            self._advance()
            return token.value
        else:
            self._error(f"Expected identifier, got {token.type}", message)
    
    def _error(self, message: str, suggestion: str):
        """Raise a parser error with context."""
        if self._is_at_end():
            line = 1
            column = 1
            line_content = "end of file"
        else:
            token = self._peek()
            line = token.line
            column = token.column
            line_content = token.value
        
        raise MDLParserError(
            message=message,
            file_path=self.source_file,
            line=line,
            column=column,
            line_content=line_content,
            suggestion=suggestion
        )
