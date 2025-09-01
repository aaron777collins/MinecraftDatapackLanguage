"""
MDL Parser - Simplified JavaScript-style syntax with curly braces and semicolons
Handles basic control structures and number variables only
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Union
from .mdl_lexer_js import Token, TokenType, lex_mdl_js
from .mdl_errors import MDLParserError, create_parser_error, MDLLexerError

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
    data: Dict[str, Any]

@dataclass
class LootTableDeclaration(ASTNode):
    name: str
    data: Dict[str, Any]

@dataclass
class AdvancementDeclaration(ASTNode):
    name: str
    data: Dict[str, Any]

@dataclass
class PredicateDeclaration(ASTNode):
    name: str
    data: Dict[str, Any]

@dataclass
class ItemModifierDeclaration(ASTNode):
    name: str
    data: Dict[str, Any]

@dataclass
class StructureDeclaration(ASTNode):
    name: str
    data: Dict[str, Any]


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
                    ast['namespace'] = namespace_decl
                    self.current_namespace = namespace_decl['name']  # Update current namespace
                    print(f"DEBUG: Parser updated current_namespace to: {self.current_namespace}")
                elif self._peek().type == TokenType.FUNCTION:
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
        
        return {"name": name, "body": body}
    
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
            return self._parse_execute_statement()
        elif self._peek().type == TokenType.RAW_START:
            return self._parse_raw_text()
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
        
        # Check for scope selector
        scope = None
        if '<' in name and name.endswith('>'):
            # Extract scope from name
            parts = name.split('<', 1)
            if len(parts) == 2:
                name = parts[0]
                scope = parts[1][:-1]  # Remove the closing >
        
        self._match(TokenType.ASSIGN)
        
        # Parse the value (could be a number or expression)
        value = self._parse_expression()
        
        self._match(TokenType.SEMICOLON)
        
        return {"name": name, "scope": scope, "value": value}
    
    def _parse_variable_assignment(self) -> VariableAssignment:
        """Parse variable assignment."""
        name_token = self._match(TokenType.IDENTIFIER)
        name = name_token.value
        
        self._match(TokenType.ASSIGN)
        
        # Parse the value (could be a number or expression)
        value = self._parse_expression()
        
        self._match(TokenType.SEMICOLON)
        
        return {"name": name, "value": value}
    
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
        
        # Check for else
        else_body = None
        if not self._is_at_end() and self._peek().type == TokenType.ELSE:
            self._match(TokenType.ELSE)
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
        
        return {"condition": condition, "then_body": then_body, "else_body": else_body}
    
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
        
        return {"condition": condition, "method": method, "body": body}
    
    def _parse_function_call(self) -> FunctionCall:
        """Parse function call."""
        self._match(TokenType.FUNCTION)
        
        name_token = self._match(TokenType.STRING)
        name = name_token.value.strip('"').strip("'")
        
        self._match(TokenType.SEMICOLON)
        
        return {"name": name}
    
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
        return {"command": command}
    
    def _parse_raw_text(self) -> RawText:
        """Parse raw text block."""
        self._match(TokenType.RAW_START)
        
        # Parse the raw content
        content_parts = []
        while not self._is_at_end() and self._peek().type != TokenType.RAW_END:
            content_parts.append(self._peek().value)
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
        return {"content": content}
    
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
        return {"command": command}
    
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
        
        return {"hook_type": hook_type, "function_name": function_name}
    
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
        
        return {"tag_type": tag_type, "name": name, "values": values}
    
    def _parse_expression(self) -> Any:
        """Parse an expression."""
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
            return VariableSubstitutionExpression(variable_name)
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
