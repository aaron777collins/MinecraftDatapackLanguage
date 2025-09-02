"""
MDL Parser - Simplified JavaScript-style syntax with curly braces and semicolons
Handles basic control structures and number variables only
"""

from typing import List, Optional, Dict, Any, Union
from .mdl_lexer_js import Token, TokenType, lex_mdl_js
from .mdl_errors import MDLParserError, create_parser_error, MDLLexerError
from .ast_nodes import (
    ASTNode, PackDeclaration, NamespaceDeclaration, FunctionDeclaration,
    VariableDeclaration, VariableAssignment, IfStatement, WhileLoop,
    FunctionCall, ExecuteStatement, RawText, Command, VariableExpression,
    VariableSubstitutionExpression, LiteralExpression, BinaryExpression,
    HookDeclaration, TagDeclaration, RecipeDeclaration, LootTableDeclaration,
    AdvancementDeclaration, PredicateDeclaration, ItemModifierDeclaration,
    StructureDeclaration
)


class MDLParser:
    """Parser for simplified MDL language."""
    
    def __init__(self, tokens: List[Token], source_file: str = None):
        self.tokens = tokens
        self.current = 0
        self.current_namespace = "mdl"  # Track current namespace
        self.source_file = source_file
    
    def parse(self) -> Dict[str, Any]:
        """Parse tokens into AST."""
        ast = {
            'pack': None,
            'namespace': None,
            'functions': [],
            'hooks': [],
            'tags': [],
            'imports': [],
            'exports': [],
            'variables': [],  # Add support for top-level variable declarations
            'recipes': [],
            'loot_tables': [],
            'advancements': [],
            'predicates': [],
            'item_modifiers': [],
            'structures': []
        }
        
        while not self._is_at_end():
            try:
                if self._peek().type == TokenType.PACK:
                    ast['pack'] = self._parse_pack_declaration()
                elif self._peek().type == TokenType.NAMESPACE:
                    namespace_decl = self._parse_namespace_declaration()
                    # Store namespace in both places for compatibility
                    ast['namespace'] = namespace_decl
                    # Also collect all namespaces in a list
                    if 'namespaces' not in ast:
                        ast['namespaces'] = []
                    ast['namespaces'].append(namespace_decl)
                    self.current_namespace = namespace_decl['name']  # Update current namespace
                    print(f"DEBUG: Parser updated current_namespace to: {self.current_namespace}")
                elif self._peek().type == TokenType.FUNCTION:
                    # Check if this is a function call or declaration
                    # Look ahead to see if there's a semicolon or brace
                    function_token = self._peek()
                    self._advance()  # Consume 'function'
                    
                    # Look ahead to see what comes after the function name
                    name_token = self._peek()
                    if name_token.type != TokenType.STRING:
                        raise create_parser_error(
                            message="Expected function name after 'function'",
                            file_path=self.source_file,
                            line=name_token.line,
                            column=name_token.column,
                            line_content=name_token.value,
                            suggestion="Provide a function name in quotes"
                        )
                    
                    # Look ahead to see if there's a semicolon (function call) or brace (function declaration)
                    self._advance()  # Consume function name
                    next_token = self._peek()
                    
                    if next_token.type == TokenType.SEMICOLON:
                        # This is a function call
                        self._advance()  # Consume semicolon
                        name = name_token.value.strip('"').strip("'")
                        ast['functions'].append({"type": "function_call", "name": name})
                    else:
                        # This is a function declaration - reset and parse properly
                        self.current -= 2  # Go back to 'function' token
                        ast['functions'].append(self._parse_function_declaration())
                elif self._peek().type == TokenType.ON_LOAD:
                    ast['hooks'].append(self._parse_hook_declaration())
                elif self._peek().type == TokenType.ON_TICK:
                    ast['hooks'].append(self._parse_hook_declaration())
                elif self._peek().type == TokenType.TAG:
                    ast['tags'].append(self._parse_tag_declaration())
                elif self._peek().type == TokenType.VAR:
                    # Handle top-level variable declarations
                    ast['variables'].append(self._parse_variable_declaration())
                elif self._peek().type == TokenType.RECIPE:
                    print(f"DEBUG: Found RECIPE token, current_namespace: {self.current_namespace}")
                    ast['recipes'].append(self._parse_recipe_declaration())
                elif self._peek().type == TokenType.LOOT_TABLE:
                    ast['loot_tables'].append(self._parse_loot_table_declaration())
                elif self._peek().type == TokenType.ADVANCEMENT:
                    ast['advancements'].append(self._parse_advancement_declaration())
                elif self._peek().type == TokenType.PREDICATE:
                    ast['predicates'].append(self._parse_predicate_declaration())
                elif self._peek().type == TokenType.ITEM_MODIFIER:
                    ast['item_modifiers'].append(self._parse_item_modifier_declaration())
                elif self._peek().type == TokenType.STRUCTURE:
                    ast['structures'].append(self._parse_structure_declaration())
                else:
                    # Skip unknown tokens
                    self._advance()
            except MDLLexerError:
                # Re-raise lexer errors as they already have proper formatting
                raise
            except Exception as e:
                # Convert other exceptions to parser errors
                current_token = self._peek()
                raise create_parser_error(
                    message=str(e),
                    file_path=self.source_file,
                    line=current_token.line,
                    column=current_token.column,
                    line_content=current_token.value,
                    suggestion="Check the syntax and ensure all required tokens are present"
                )
        
        # Check for missing closing braces by looking for unmatched opening braces
        self._check_for_missing_braces()
        
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
        
        return {"type": "pack_declaration", "name": name, "description": description, "pack_format": pack_format}
    
    def _parse_namespace_declaration(self) -> NamespaceDeclaration:
        """Parse namespace declaration."""
        self._match(TokenType.NAMESPACE)
        
        name_token = self._match(TokenType.STRING)
        name = name_token.value.strip('"').strip("'")
        
        self._match(TokenType.SEMICOLON)
        
        return {"type": "namespace_declaration", "name": name}
    
    def _parse_function_declaration(self) -> FunctionDeclaration:
        """Parse function declaration."""
        self._match(TokenType.FUNCTION)
        
        name_token = self._match(TokenType.STRING)
        name = name_token.value.strip('"').strip("'")
        
        self._match(TokenType.LBRACE)
        
        body = []
        while not self._is_at_end() and self._peek().type != TokenType.RBRACE:
            body.append(self._parse_statement())
        
        if self._is_at_end():
            raise create_parser_error(
                message="Missing closing brace for function",
                file_path=self.source_file,
                line=self._peek().line,
                column=self._peek().column,
                line_content=self._peek().value,
                suggestion="Add a closing brace (}) to match the opening brace"
            )
        
        self._match(TokenType.RBRACE)
        
        return {"type": "function_declaration", "name": name, "body": body}
    
    def _parse_recipe_declaration(self) -> RecipeDeclaration:
        """Parse recipe declaration."""
        self._match(TokenType.RECIPE)
        
        name_token = self._match(TokenType.STRING)
        name = name_token.value.strip('"').strip("'")
        
        # Expect a JSON file path
        json_file_token = self._match(TokenType.STRING)
        json_file = json_file_token.value.strip('"').strip("'")
        
        self._match(TokenType.SEMICOLON)
        
        # Store reference to JSON file and current namespace
        data = {"json_file": json_file}
        
        result = {"name": name, "data": data, "_source_namespace": self.current_namespace}
        print(f"DEBUG: Recipe '{name}' declared with namespace: {self.current_namespace}")
        return result
    
    def _parse_loot_table_declaration(self) -> LootTableDeclaration:
        """Parse loot table declaration."""
        self._match(TokenType.LOOT_TABLE)
        
        name_token = self._match(TokenType.STRING)
        name = name_token.value.strip('"').strip("'")
        
        json_file_token = self._match(TokenType.STRING)
        json_file = json_file_token.value.strip('"').strip("'")
        
        self._match(TokenType.SEMICOLON)
        
        data = {"json_file": json_file}
        return {"name": name, "data": data, "_source_namespace": self.current_namespace}
    
    def _parse_advancement_declaration(self) -> AdvancementDeclaration:
        """Parse advancement declaration."""
        self._match(TokenType.ADVANCEMENT)
        
        name_token = self._match(TokenType.STRING)
        name = name_token.value.strip('"').strip("'")
        
        json_file_token = self._match(TokenType.STRING)
        json_file = json_file_token.value.strip('"').strip("'")
        
        self._match(TokenType.SEMICOLON)
        
        data = {"json_file": json_file}
        return {"name": name, "data": data, "_source_namespace": self.current_namespace}
    
    def _parse_predicate_declaration(self) -> PredicateDeclaration:
        """Parse predicate declaration."""
        self._match(TokenType.PREDICATE)
        
        name_token = self._match(TokenType.STRING)
        name = name_token.value.strip('"').strip("'")
        
        json_file_token = self._match(TokenType.STRING)
        json_file = json_file_token.value.strip('"').strip("'")
        
        self._match(TokenType.SEMICOLON)
        
        data = {"json_file": json_file}
        return {"name": name, "data": data, "_source_namespace": self.current_namespace}
    
    def _parse_item_modifier_declaration(self) -> ItemModifierDeclaration:
        """Parse item modifier declaration."""
        self._match(TokenType.ITEM_MODIFIER)
        
        name_token = self._match(TokenType.STRING)
        name = name_token.value.strip('"').strip("'")
        
        json_file_token = self._match(TokenType.STRING)
        json_file = json_file_token.value.strip('"').strip("'")
        
        self._match(TokenType.SEMICOLON)
        
        data = {"json_file": json_file}
        return {"name": name, "data": data, "_source_namespace": self.current_namespace}
    
    def _parse_structure_declaration(self) -> StructureDeclaration:
        """Parse structure declaration."""
        self._match(TokenType.STRUCTURE)
        
        name_token = self._match(TokenType.STRING)
        name = name_token.value.strip('"').strip("'")
        
        json_file_token = self._match(TokenType.STRING)
        json_file = json_file_token.value.strip('"').strip("'")
        
        self._match(TokenType.SEMICOLON)
        
        data = {"json_file": json_file}
        return {"name": name, "data": data, "_source_namespace": self.current_namespace}
    
    def _parse_statement(self) -> ASTNode:
        """Parse a statement."""
        if self._peek().type == TokenType.VAR:
            return self._parse_variable_declaration()
        elif self._peek().type == TokenType.IF:
            return self._parse_if_statement()
        elif self._peek().type == TokenType.WHILE:
            return self._parse_while_loop()
        elif self._peek().type == TokenType.FUNCTION:
            return self._parse_function_call()
        elif self._peek().type == TokenType.EXECUTE:
            return self._parse_execute_command()
        elif self._peek().type == TokenType.RAW_START:
            return self._parse_raw_text()
        elif self._peek().type == TokenType.SAY:
            return self._parse_say_command()
        elif self._peek().type == TokenType.IDENTIFIER:
            # Check for for loops (which are no longer supported)
            if self._peek().value == "for":
                raise create_parser_error(
                    message="For loops are no longer supported in MDL. Use while loops instead.",
                    file_path=self.source_file,
                    line=self._peek().line,
                    column=self._peek().column,
                    line_content=self._peek().value,
                    suggestion="Replace 'for' with 'while' and adjust the loop structure"
                )
            
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
        self._match(TokenType.NUM)
        
        name_token = self._match(TokenType.IDENTIFIER)
        name = name_token.value
        
        # Check for scope selector after variable name
        scope = None
        if not self._is_at_end() and self._peek().type == TokenType.SCOPE:
            self._match(TokenType.SCOPE)  # consume 'scope'
            
            # Parse scope selector in angle brackets
            if not self._is_at_end() and self._peek().type == TokenType.LANGLE:
                self._match(TokenType.LANGLE)  # consume '<'
                
                # Parse scope selector content
                scope_parts = []
                while not self._is_at_end() and self._peek().type != TokenType.RANGLE:
                    scope_parts.append(self._peek().value)
                    self._advance()
                
                if self._is_at_end():
                    raise create_parser_error(
                        message="Unterminated scope selector",
                        file_path=self.source_file,
                        line=self._peek().line,
                        column=self._peek().column,
                        line_content=self._peek().value,
                        suggestion="Add a closing '>' to terminate the scope selector"
                    )
                
                self._match(TokenType.RANGLE)  # consume '>'
                scope = ''.join(scope_parts)
        
        self._match(TokenType.ASSIGN)
        
        # Parse the value (could be a number or expression)
        value = self._parse_expression()
        
        self._match(TokenType.SEMICOLON)
        
        return {"type": "variable_declaration", "name": name, "scope": scope, "value": value}
    
    def _parse_variable_assignment(self) -> VariableAssignment:
        """Parse variable assignment."""
        name_token = self._match(TokenType.IDENTIFIER)
        name = name_token.value
        
        self._match(TokenType.ASSIGN)
        
        # Parse the value (could be a number or expression)
        value = self._parse_expression()
        
        self._match(TokenType.SEMICOLON)
        
        return {"type": "variable_assignment", "name": name, "value": value}
    
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
        
        if self._is_at_end():
            raise create_parser_error(
                message="Missing closing brace for if statement",
                file_path=self.source_file,
                line=self._peek().line,
                column=self._peek().column,
                line_content=self._peek().value,
                suggestion="Add a closing brace (}) to match the opening brace"
            )
        
        self._match(TokenType.RBRACE)
        
        # Check for else or else if
        else_body = None
        if not self._is_at_end() and self._peek().type == TokenType.ELSE:
            self._match(TokenType.ELSE)
            
            # Check if this is an else if statement
            if not self._is_at_end() and self._peek().type == TokenType.IF:
                # This is an else if statement - parse it as a nested if
                self._match(TokenType.IF)
                
                # Parse the else if condition
                condition_token = self._match(TokenType.STRING)
                condition = condition_token.value.strip('"').strip("'")
                
                self._match(TokenType.LBRACE)
                
                # Parse the else if body
                else_body = []
                while not self._is_at_end() and self._peek().type != TokenType.RBRACE:
                    else_body.append(self._parse_statement())
                
                if self._is_at_end():
                    raise create_parser_error(
                        message="Missing closing brace for else if statement",
                        file_path=self.source_file,
                        line=self._peek().line,
                        column=self._peek().column,
                        line_content=self._peek().value,
                        suggestion="Add a closing brace (}) to match the opening brace"
                    )
                
                self._match(TokenType.RBRACE)
                
                # Recursively check for more else if or else statements
                if not self._is_at_end() and self._peek().type == TokenType.ELSE:
                    # Parse the remaining else/else if chain
                    remaining_else = self._parse_else_chain()
                    if remaining_else:
                        # Combine the else if body with the remaining else chain
                        else_body.extend(remaining_else)
            else:
                # This is a regular else statement
                self._match(TokenType.LBRACE)
                
                else_body = []
                while not self._is_at_end() and self._peek().type != TokenType.RBRACE:
                    else_body.append(self._parse_statement())
                
                if self._is_at_end():
                    raise create_parser_error(
                        message="Missing closing brace for else statement",
                        file_path=self.source_file,
                        line=self._peek().line,
                        column=self._peek().column,
                        line_content=self._peek().value,
                        suggestion="Add a closing brace (}) to match the opening brace"
                    )
                
                self._match(TokenType.RBRACE)
        
        return {"type": "if_statement", "condition": condition, "then_body": then_body, "else_body": else_body}
    
    def _parse_else_chain(self) -> List[Any]:
        """Parse a chain of else if statements and final else statement."""
        statements = []
        
        while not self._is_at_end() and self._peek().type == TokenType.ELSE:
            self._match(TokenType.ELSE)
            
            # Check if this is an else if statement
            if not self._is_at_end() and self._peek().type == TokenType.IF:
                # This is an else if statement
                self._match(TokenType.IF)
                
                # Parse the else if condition
                condition_token = self._match(TokenType.STRING)
                condition = condition_token.value.strip('"').strip("'")
                
                self._match(TokenType.LBRACE)
                
                # Parse the else if body
                else_if_body = []
                while not self._is_at_end() and self._peek().type != TokenType.RBRACE:
                    else_if_body.append(self._parse_statement())
                
                if self._is_at_end():
                    raise create_parser_error(
                        message="Missing closing brace for else if statement",
                        file_path=self.source_file,
                        line=self._peek().line,
                        column=self._peek().column,
                        line_content=self._peek().value,
                        suggestion="Add a closing brace (}) to match the opening brace"
                    )
                
                self._match(TokenType.RBRACE)
                
                # Add the else if statement to the chain
                statements.append({
                    "type": "else_if_statement",
                    "condition": condition,
                    "body": else_if_body
                })
            else:
                # This is a final else statement
                self._match(TokenType.LBRACE)
                
                else_body = []
                while not self._is_at_end() and self._peek().type != TokenType.RBRACE:
                    else_body.append(self._parse_statement())
                
                if self._is_at_end():
                    raise create_parser_error(
                        message="Missing closing brace for else statement",
                        file_path=self.source_file,
                        line=self._peek().line,
                        column=self._peek().column,
                        line_content=self._peek().value,
                        suggestion="Add a closing brace (}) to match the opening brace"
                    )
                
                self._match(TokenType.RBRACE)
                
                # Add the final else statement to the chain
                statements.append({
                    "type": "else_statement",
                    "body": else_body
                })
                break  # Final else statement ends the chain
        
        return statements
    
    def _parse_while_loop(self) -> WhileLoop:
        """Parse while loop."""
        self._match(TokenType.WHILE)
        
        # Parse condition
        condition_token = self._match(TokenType.STRING)
        condition = condition_token.value.strip('"').strip("'")
        
        # Check for method parameter
        method = None
        if not self._is_at_end() and self._peek().type == TokenType.IDENTIFIER and self._peek().value == "method":
            self._match(TokenType.IDENTIFIER)  # consume "method"
            self._match(TokenType.ASSIGN)
            method_token = self._match(TokenType.STRING)
            method = method_token.value.strip('"').strip("'")
        
        self._match(TokenType.LBRACE)
        
        # Parse body
        body = []
        while not self._is_at_end() and self._peek().type != TokenType.RBRACE:
            body.append(self._parse_statement())
        
        if self._is_at_end():
            raise create_parser_error(
                message="Missing closing brace for while loop",
                file_path=self.source_file,
                line=self._peek().line,
                column=self._peek().column,
                line_content=self._peek().value,
                suggestion="Add a closing brace (}) to match the opening brace"
            )
        
        self._match(TokenType.RBRACE)
        
        return {"type": "while_statement", "condition": condition, "method": method, "body": body}
    
    def _parse_function_call(self) -> FunctionCall:
        """Parse function call."""
        self._match(TokenType.FUNCTION)
        
        name_token = self._match(TokenType.STRING)
        name = name_token.value.strip('"').strip("'")
        
        # Check for scope selector after function name
        scope = None
        if '<' in name and name.endswith('>'):
            # Extract scope selector from function name
            parts = name.split('<', 1)
            if len(parts) == 2:
                function_name = parts[0]
                scope_selector = parts[1][:-1]  # Remove closing >
                scope = scope_selector
                name = function_name
            else:
                # Malformed scope selector
                raise create_parser_error(
                    message="Malformed scope selector in function call",
                    file_path=self.source_file,
                    line=self._peek().line,
                    column=self._peek().column,
                    line_content=name,
                    suggestion="Use format: function \"namespace:function_name<@selector>\""
                )
        
        # Extract function name from namespace:function_name format
        if ':' in name:
            namespace_parts = name.split(':', 1)
            if len(namespace_parts) == 2:
                namespace_name = namespace_parts[0]
                function_name = namespace_parts[1]
                # Store both namespace and function name
                return {"type": "function_call", "name": function_name, "scope": scope, "namespace": namespace_name}
        
        self._match(TokenType.SEMICOLON)
        
        return {"type": "function_call", "name": name, "scope": scope}
    
    def _parse_execute_statement(self) -> ExecuteStatement:
        """Parse execute statement."""
        self._match(TokenType.EXECUTE)
        
        # Parse the command
        command_parts = []
        while not self._is_at_end() and self._peek().type != TokenType.SEMICOLON:
            command_parts.append(self._peek().value)
            self._advance()
        
        if self._is_at_end():
            raise create_parser_error(
                message="Missing semicolon after execute statement",
                file_path=self.source_file,
                line=self._peek().line,
                column=self._peek().column,
                line_content=self._peek().value,
                suggestion="Add a semicolon (;) at the end of the execute statement"
            )
        
        self._match(TokenType.SEMICOLON)
        
        command = _smart_join_command_parts(command_parts)
        return {"type": "command", "command": command}
    
    def _parse_raw_text(self) -> RawText:
        """Parse raw text block."""
        self._match(TokenType.RAW_START)
        
        # Parse the raw content
        content_parts = []
        while not self._is_at_end() and self._peek().type != TokenType.RAW_END:
            if self._peek().type == TokenType.RAW:
                # Add raw content
                content_parts.append(self._peek().value)
                self._advance()
            else:
                # Skip other tokens (shouldn't happen in raw mode)
                self._advance()
        
        if self._is_at_end():
            raise create_parser_error(
                message="Missing closing 'raw!$' for raw text block",
                file_path=self.source_file,
                line=self._peek().line,
                column=self._peek().column,
                line_content=self._peek().value,
                suggestion="Add 'raw!$' to close the raw text block"
            )
        
        self._match(TokenType.RAW_END)
        
        content = "".join(content_parts)
        # Split content into individual commands by newlines
        # Raw blocks contain raw Minecraft commands, not MDL commands with semicolons
        commands = [cmd.strip() for cmd in content.split('\n') if cmd.strip()]
        return {"type": "raw_text", "commands": commands}
    
    def _parse_command(self) -> Command:
        """Parse a command."""
        command_parts = []
        while not self._is_at_end() and self._peek().type != TokenType.SEMICOLON:
            command_parts.append(self._peek().value)
            self._advance()
        
        if self._is_at_end():
            raise create_parser_error(
                message="Missing semicolon after command",
                file_path=self.source_file,
                line=self._peek().line,
                column=self._peek().column,
                line_content=self._peek().value,
                suggestion="Add a semicolon (;) at the end of the command"
            )
        
        self._match(TokenType.SEMICOLON)
        
        command = _smart_join_command_parts(command_parts)
        return {"type": "command", "command": command}
    
    def _parse_say_command(self) -> Command:
        """Parse a say command."""
        say_token = self._match(TokenType.SAY)
        content = say_token.value
        
        # The semicolon is already included in the token value from the lexer
        # No need to consume another semicolon
        
        return {"type": "command", "command": content}
    
    def _parse_execute_command(self) -> Command:
        """Parse an execute command."""
        execute_token = self._match(TokenType.EXECUTE)
        content = execute_token.value
        
        # The semicolon should already be consumed by the lexer
        # But let's make sure we have it
        if not self._is_at_end() and self._peek().type == TokenType.SEMICOLON:
            self._match(TokenType.SEMICOLON)
        
        return {"type": "command", "command": content}
    
    def _parse_hook_declaration(self) -> HookDeclaration:
        """Parse hook declaration."""
        if self._peek().type == TokenType.ON_TICK:
            self._match(TokenType.ON_TICK)
            hook_type = "tick"
        else:
            self._match(TokenType.ON_LOAD)
            hook_type = "load"
        
        function_name_token = self._match(TokenType.STRING)
        function_name = function_name_token.value.strip('"').strip("'")
        
        self._match(TokenType.SEMICOLON)
        
        return {"type": "hook_declaration", "hook_type": hook_type, "function_name": function_name}
    
    def _parse_tag_declaration(self) -> TagDeclaration:
        """Parse tag declaration."""
        self._match(TokenType.TAG)
        
        # Parse tag type
        tag_type_token = self._match(TokenType.IDENTIFIER)
        tag_type = tag_type_token.value
        
        # Parse tag name
        name_token = self._match(TokenType.STRING)
        name = name_token.value.strip('"').strip("'")
        
        self._match(TokenType.LBRACE)
        
        # Parse tag values
        values = []
        while not self._is_at_end() and self._peek().type != TokenType.RBRACE:
            if self._peek().type == TokenType.STRING:
                value_token = self._match(TokenType.STRING)
                values.append(value_token.value.strip('"').strip("'"))
            else:
                # Skip non-string tokens
                self._advance()
        
        if self._is_at_end():
            raise create_parser_error(
                message="Missing closing brace for tag declaration",
                file_path=self.source_file,
                line=self._peek().line,
                column=self._peek().column,
                line_content=self._peek().value,
                suggestion="Add a closing brace (}) to match the opening brace"
            )
        
        self._match(TokenType.RBRACE)
        
        return {"type": "tag_declaration", "tag_type": tag_type, "name": name, "values": values}
    
    def _parse_expression(self) -> Any:
        """Parse an expression with operator precedence."""
        return self._parse_addition()
    
    def _parse_addition(self) -> Any:
        """Parse addition and subtraction."""
        expr = self._parse_multiplication()
        
        while not self._is_at_end() and self._peek().type in [TokenType.PLUS, TokenType.MINUS]:
            operator = self._peek().type
            self._advance()  # consume operator
            right = self._parse_multiplication()
            expr = BinaryExpression(expr, operator, right)
        
        return expr
    
    def _parse_multiplication(self) -> Any:
        """Parse multiplication, division, and modulo."""
        expr = self._parse_primary()
        
        while not self._is_at_end() and self._peek().type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]:
            operator = self._peek().type
            self._advance()  # consume operator
            right = self._parse_primary()
            expr = BinaryExpression(expr, operator, right)
        
        return expr
    
    def _parse_primary(self) -> Any:
        """Parse primary expressions (numbers, strings, variables, parenthesized expressions)."""
        token = self._peek()
        
        if token.type == TokenType.NUMBER:
            self._advance()
            return LiteralExpression(token.value, "number")
        elif token.type == TokenType.STRING:
            self._advance()
            return LiteralExpression(token.value.strip('"').strip("'"), "string")
        elif token.type == TokenType.VARIABLE_SUB:
            self._advance()
            variable_name = token.value
            
            # Check if the variable contains a scope selector
            if '<' in variable_name and variable_name.endswith('>'):
                # Extract variable name and scope selector
                parts = variable_name.split('<', 1)
                if len(parts) == 2:
                    var_name = parts[0]
                    scope_selector = parts[1][:-1]  # Remove the closing >
                    return VariableSubstitutionExpression(var_name, scope_selector)
            
            # Regular variable substitution without scope
            return VariableSubstitutionExpression(variable_name, None)
        elif token.type == TokenType.IDENTIFIER:
            identifier_name = token.value
            self._advance()  # consume the identifier
            
            # Check if the identifier contains a scope selector
            if '<' in identifier_name and identifier_name.endswith('>'):
                # Extract variable name and scope selector
                parts = identifier_name.split('<', 1)
                if len(parts) == 2:
                    var_name = parts[0]
                    scope_selector = parts[1][:-1]  # Remove the closing >
                    # For variable expressions in assignments, keep the full scoped name
                    return VariableExpression(identifier_name)
            
            # Regular variable expression without scope
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
            raise create_parser_error(
                message=f"Unexpected end of input, expected {expected_type}",
                file_path=self.source_file,
                line=self._peek().line,
                column=self._peek().column,
                line_content=self._peek().value,
                suggestion="Check for missing tokens or incomplete statements"
            )
        
        token = self._peek()
        if token.type == expected_type:
            return self._advance()
        else:
            raise create_parser_error(
                message=f"Expected {expected_type}, got {token.type}",
                file_path=self.source_file,
                line=token.line,
                column=token.column,
                line_content=token.value,
                suggestion=f"Replace '{token.value}' with the expected {expected_type}"
            )
    
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
    
    def _check_for_missing_braces(self):
        """Check for missing closing braces in the source code."""
        # This is a simple check - in a more robust implementation,
        # we would track brace matching during parsing
        # For now, we'll rely on the existing error handling in the parser
        pass


def _smart_join_command_parts(parts: List[str]) -> str:
    """Smart join command parts with proper spacing."""
    if not parts:
        return ""
    
    result = parts[0]
    
    for i in range(1, len(parts)):
        prev_part = parts[i - 1]
        curr_part = parts[i]
        
        # Special case: don't add space when previous part ends with a namespace (like minecraft)
        # and current part starts with a colon (like :iron_ingot)
        if curr_part.startswith(':'):
            # Don't add space for namespace:item patterns
            result += curr_part
        else:
            # Add space if needed
            if (prev_part and curr_part and 
                not prev_part.endswith('[') and not prev_part.endswith('{') and
                not curr_part.startswith(']') and not curr_part.startswith('}') and
                not curr_part.startswith(',') and not curr_part.startswith(':') and
                not prev_part.endswith('"') and not curr_part.startswith('"')):
                result += " "
            
            # Special case: add space after 'say' before quoted string
            if prev_part == 'say' and curr_part.startswith('"'):
                result += " "
            
            result += curr_part
    
    return result


def parse_mdl_js(source: str, source_file: str = None) -> Dict[str, Any]:
    """Parse JavaScript-style MDL source code into AST."""
    tokens = lex_mdl_js(source, source_file)
    parser = MDLParser(tokens, source_file)
    return parser.parse()
