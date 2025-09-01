"""
MDL Lexer - Simplified JavaScript-style syntax with curly braces and semicolons
Handles basic control structures and number variables only
"""

import re
from dataclasses import dataclass
from typing import List, Optional
from .mdl_errors import MDLLexerError


@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int


class TokenType:
    # Keywords
    PACK = "PACK"
    NAMESPACE = "NAMESPACE"
    FUNCTION = "FUNCTION"
    VAR = "VAR"
    NUM = "NUM"
    SCOPE = "SCOPE"
    IF = "IF"
    ELSE = "ELSE"
    ELSE_IF = "ELSE_IF"
    WHILE = "WHILE"
    ON_TICK = "ON_TICK"
    ON_LOAD = "ON_LOAD"
    TAG = "TAG"
    ADD = "ADD"
    RAW = "RAW"
    RAW_START = "RAW_START"
    RAW_END = "RAW_END"
    EXECUTE = "EXECUTE"
    
    # Registry types
    RECIPE = "RECIPE"
    LOOT_TABLE = "LOOT_TABLE"
    ADVANCEMENT = "ADVANCEMENT"
    PREDICATE = "PREDICATE"
    ITEM_MODIFIER = "ITEM_MODIFIER"
    STRUCTURE = "STRUCTURE"
    
    # Operators
    ASSIGN = "ASSIGN"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    AND = "AND"
    OR = "OR"
    
    # Delimiters
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    LANGLE = "LANGLE"  # < for scope syntax
    RANGLE = "RANGLE"  # > for scope syntax
    DOT = "DOT"
    COLON = "COLON"
    
    # Literals
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    
    # Special
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    COMMENT = "COMMENT"
    COMMAND = "COMMAND"
    SAY = "SAY"  # Say command
    
    # Variable substitution
    VARIABLE_SUB = "VARIABLE_SUB"  # $variable$


class MDLLexer:
    """Lexer for simplified MDL language."""
    
    def __init__(self, source_file: str = None):
        self.tokens = []
        self.current = 0
        self.start = 0
        self.line = 1
        self.column = 1
        self.source_file = source_file
        self.in_raw_mode = False
    
    def lex(self, source: str) -> List[Token]:
        """Lex the source code into tokens."""
        self.tokens = []
        self.current = 0
        self.start = 0
        self.line = 1
        self.column = 1
        self.in_raw_mode = False
        
        while self.current < len(source):
            self.start = self.current
            self._scan_token(source)
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    def _scan_token(self, source: str):
        """Scan a single token."""
        char = source[self.current]
        
        # If in raw mode, scan raw text until we find raw!$
        if self.in_raw_mode:
            self._scan_raw_text(source)
            return
        
        # Handle whitespace and newlines
        if char.isspace():
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.current += 1
            return
        
        # Handle comments
        if char == '/' and self.current + 1 < len(source) and source[self.current + 1] == '/':
            self._scan_comment(source)
            return
        
        # Handle strings
        if char in ['"', "'"]:
            self._scan_string(source, char)
            return
        
        # Handle numbers
        if char.isdigit():
            self._scan_number(source)
            return
        
        # Handle raw block markers and variable substitutions
        if char == '$':
            # Check if this is a raw block start marker
            if (self.current + 4 < len(source) and 
                source[self.current:self.current + 5] == '$!raw'):
                self._scan_raw_start(source)
                return
            else:
                self._scan_variable_substitution(source)
                return
        
        # Handle raw block end marker
        if char == 'r':
            # Check if this is a raw block end marker
            if (self.current + 4 < len(source) and 
                source[self.current:self.current + 5] == 'raw!$'):
                self._scan_raw_end(source)
                return
        
        # Handle identifiers and keywords
        if char.isalpha() or char == '_':
            # Special handling for 'say' command - but be more careful about context
            if (char == 's' and 
                self.current + 2 < len(source) and 
                source[self.current:self.current + 3] == 'say' and
                not self._is_inside_control_structure(source)):
                self._scan_say_command(source)
                return
            else:
                self._scan_identifier(source)
                return
        
        # Handle operators and delimiters
        self._scan_operator_or_delimiter(source)
    
    def _scan_comment(self, source: str):
        """Scan a comment."""
        # Skip the //
        self.current += 2
        self.column += 2
        
        # Scan until end of line or end of source
        while (self.current < len(source) and 
               source[self.current] != '\n'):
            self.current += 1
            self.column += 1
        
        # Don't add comment tokens to the output
        # Comments are ignored during parsing
    
    def _scan_string(self, source: str, quote_char: str):
        """Scan a string literal."""
        self.current += 1  # Skip opening quote
        self.column += 1
        
        start_column = self.column
        start_line = self.line
        
        while (self.current < len(source) and 
               source[self.current] != quote_char):
            if source[self.current] == '\n':
                # Unterminated string - report error
                raise create_lexer_error(
                    message=f"Unterminated string literal",
                    file_path=self.source_file,
                    line=start_line,
                    column=start_column,
                    line_content=source[start_line-1:start_line] if start_line <= len(source.split('\n')) else "",
                    suggestion="Add a closing quote to terminate the string"
                )
            
            if source[self.current] == '\\' and self.current + 1 < len(source):
                # Handle escape sequences
                self.current += 2
                self.column += 2
            else:
                self.current += 1
                self.column += 1
        
        if self.current >= len(source):
            # Unterminated string at end of file
            raise create_lexer_error(
                message=f"Unterminated string literal at end of file",
                file_path=self.source_file,
                line=start_line,
                column=start_column,
                line_content=source[start_line-1:start_line] if start_line <= len(source.split('\n')) else "",
                suggestion="Add a closing quote to terminate the string"
            )
        
        # Include the closing quote
        self.current += 1
        self.column += 1
        
        text = source[self.start:self.current]
        self.tokens.append(Token(TokenType.STRING, text, start_line, start_column))
    
    def _scan_number(self, source: str):
        """Scan a number literal."""
        while (self.current < len(source) and 
               source[self.current].isdigit()):
            self.current += 1
            self.column += 1
        
        # Check for decimal point
        if (self.current < len(source) and 
            source[self.current] == '.' and
            self.current + 1 < len(source) and
            source[self.current + 1].isdigit()):
            self.current += 1  # consume the decimal point
            self.column += 1
            
            while (self.current < len(source) and 
                   source[self.current].isdigit()):
                self.current += 1
                self.column += 1
        
        text = source[self.start:self.current]
        self.tokens.append(Token(TokenType.NUMBER, text, self.line, self.column - len(text)))
    
    def _scan_identifier(self, source: str):
        """Scan an identifier or keyword."""
        while (self.current < len(source) and 
               (source[self.current].isalnum() or source[self.current] == '_')):
            self.current += 1
            self.column += 1
        
        text = source[self.start:self.current]
        
        # Check if it's a keyword
        keyword_map = {
            'pack': TokenType.PACK,
            'namespace': TokenType.NAMESPACE,
            'function': TokenType.FUNCTION,
            'var': TokenType.VAR,
            'num': TokenType.NUM,
            'scope': TokenType.SCOPE,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'on_tick': TokenType.ON_TICK,
            'on_load': TokenType.ON_LOAD,
            'tag': TokenType.TAG,
            'add': TokenType.ADD,
            'raw': TokenType.RAW,
            'execute': TokenType.EXECUTE,
            'recipe': TokenType.RECIPE,
            'loot_table': TokenType.LOOT_TABLE,
            'advancement': TokenType.ADVANCEMENT,
            'predicate': TokenType.PREDICATE,
            'item_modifier': TokenType.ITEM_MODIFIER,
            'structure': TokenType.STRUCTURE
        }
        
        token_type = keyword_map.get(text.lower(), TokenType.IDENTIFIER)
        
        # Note: Special handling for say and execute commands is done in _scan_token
        # to avoid duplicate processing
        self.tokens.append(Token(token_type, text, self.line, self.column - len(text)))
    
    def _scan_variable_substitution(self, source: str):
        """Scan variable substitution ($variable$)."""
        self.current += 1  # Skip the $
        self.column += 1
        
        scope_selector = None
        variable_name = ""
        
        # Scan the variable name
        while (self.current < len(source) and 
               (source[self.current].isalnum() or source[self.current] == '_')):
            variable_name += source[self.current]
            self.current += 1
            self.column += 1
        
        # Validate variable name starts with letter or underscore
        if variable_name and (variable_name[0].isdigit()):
            raise create_lexer_error(
                message=f"Invalid variable name '{variable_name}' - cannot start with a digit",
                file_path=self.source_file,
                line=self.line,
                column=self.column - len(variable_name),
                line_content=source[self.line-1:self.line] if self.line <= len(source.split('\n')) else "",
                suggestion="Variable names must start with a letter or underscore"
            )
        
        # Check for scope selector after variable name
        if (self.current < len(source) and 
            source[self.current] == '<'):
            self.current += 1  # consume <
            self.column += 1
            
            scope_start = self.current
            bracket_count = 1
            
            # Scan until we find the matching closing >
            while (self.current < len(source) and bracket_count > 0):
                if source[self.current] == '<':
                    bracket_count += 1
                elif source[self.current] == '>':
                    bracket_count -= 1
                self.current += 1
                self.column += 1
            
            if bracket_count == 0:
                # Successfully found closing >
                scope_selector = source[scope_start:self.current-1]  # Exclude the closing >
            else:
                # Unterminated scope selector - report error
                raise create_lexer_error(
                    message="Unterminated scope selector in variable substitution",
                    file_path=self.source_file,
                    line=self.line,
                    column=self.column - (self.current - self.start),
                    suggestion="Add a closing '>' to terminate the scope selector"
                )
        
        # Check for closing $
        if (self.current < len(source) and 
            source[self.current] == '$'):
            self.current += 1
            self.column += 1
            
            # If we have a scope selector, include it in the token
            if scope_selector:
                variable_name = f"{variable_name}<{scope_selector}>"
            
            self.tokens.append(Token(TokenType.VARIABLE_SUB, variable_name, self.line, self.column - len(variable_name) - 2))
        else:
            # Not a valid variable substitution - report error
            raise create_lexer_error(
                message="Invalid variable substitution - missing closing '$'",
                file_path=self.source_file,
                line=self.line,
                column=self.column - (self.current - self.start),
                suggestion="Add a closing '$' to complete the variable substitution"
            )
    
    def _scan_raw_start(self, source: str):
        """Scan raw block start marker ($!raw)."""
        # Check if we're already in raw mode (nested raw blocks are not allowed)
        if self.in_raw_mode:
            raise create_lexer_error(
                message="Nested raw blocks are not allowed",
                file_path=self.source_file,
                line=self.line,
                column=self.column,
                line_content=source[self.line-1:self.line] if self.line <= len(source.split('\n')) else "",
                suggestion="Close the current raw block with 'raw!$' before starting a new one"
            )
        
        # Consume the $!raw
        self.current += 5
        self.column += 5
        
        text = source[self.start:self.current]
        self.tokens.append(Token(TokenType.RAW_START, text, self.line, self.column - len(text)))
        
        # Enter raw mode
        self.in_raw_mode = True
    
    def _scan_raw_end(self, source: str):
        """Scan raw block end marker (raw!$)."""
        # Consume the raw!$
        self.current += 5
        self.column += 5
        
        text = source[self.start:self.current]
        self.tokens.append(Token(TokenType.RAW_END, text, self.line, self.column - len(text)))
        
        # Exit raw mode
        self.in_raw_mode = False
    
    def _scan_raw_text(self, source: str):
        """Scan raw text content between $!raw and raw!$."""
        content_parts = []
        raw_start_line = self.line
        raw_start_column = self.column
        
        while self.current < len(source):
            char = source[self.current]
            
            # Check if we've reached the end of the raw block
            if (char == 'r' and 
                self.current + 4 < len(source) and 
                source[self.current:self.current + 5] == 'raw!$'):
                # Exit raw mode and let the main scanner handle the end marker
                self.in_raw_mode = False
                break
            
            # Add character to content
            content_parts.append(char)
            
            # Update position
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.current += 1
        
        # Check if we reached the end of source without finding the end marker
        if self.current >= len(source):
            # Unterminated raw block - report error
            raise create_lexer_error(
                message="Unterminated raw block - missing 'raw!$' end marker",
                file_path=self.source_file,
                line=raw_start_line,
                column=raw_start_column,
                line_content=source[raw_start_line-1:raw_start_line] if raw_start_line <= len(source.split('\n')) else "",
                suggestion="Add 'raw!$' to terminate the raw block"
            )
        
        # Add the raw content as a single RAW token
        content = ''.join(content_parts)
        if content.strip():  # Only add non-empty content
            # Remove leading and trailing whitespace for cleaner content
            clean_content = content.strip()
            self.tokens.append(Token(TokenType.RAW, clean_content, raw_start_line, raw_start_column))
    
    def _scan_say_command(self, source: str):
        """Scan a say command and its content until semicolon."""
        # Consume 'say'
        self.current += 3
        self.column += 3
        
        say_start_line = self.line
        say_start_column = self.column
        
        # Skip whitespace after 'say'
        while (self.current < len(source) and 
               source[self.current].isspace()):
            if source[self.current] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.current += 1
        
        # Scan content until we find a semicolon
        content_parts = []
        while self.current < len(source):
            char = source[self.current]
            
            if char == ';':
                # Found the end of the say command
                break
            
            # Add character to content
            content_parts.append(char)
            
            # Update position
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.current += 1
        
        if self.current >= len(source):
            # Unterminated say command - report error
            raise create_lexer_error(
                message="Unterminated say command - missing semicolon",
                file_path=self.source_file,
                line=say_start_line,
                column=say_start_column,
                line_content=source[say_start_line-1:say_start_line] if say_start_line <= len(source.split('\n')) else "",
                suggestion="Add a semicolon (;) to terminate the say command"
            )
        
        # Consume the semicolon
        self.current += 1
        self.column += 1
        
        # Create the say command token with full content
        content = ''.join(content_parts).strip()
        full_command = f"say {content};"
        self.tokens.append(Token(TokenType.SAY, full_command, say_start_line, say_start_column))
    
    def _scan_execute_command(self, source: str):
        """Scan an execute command and its content until semicolon."""
        # Consume 'execute'
        self.current += 7
        self.column += 7
        
        execute_start_line = self.line
        execute_start_column = self.column
        
        # Skip whitespace after 'execute'
        while (self.current < len(source) and 
               source[self.current].isspace()):
            if source[self.current] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.current += 1
        
        # Scan content until we find a semicolon
        content_parts = []
        while self.current < len(source):
            char = source[self.current]
            
            if char == ';':
                # Found the end of the execute command
                break
            
            # Add character to content
            content_parts.append(char)
            
            # Update position
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.current += 1
        
        if self.current >= len(source):
            # Unterminated execute command - report error
            raise create_lexer_error(
                message="Unterminated execute command - missing semicolon",
                file_path=self.source_file,
                line=execute_start_line,
                column=execute_start_column,
                line_content=source[execute_start_line-1:execute_start_line] if execute_start_line <= len(source.split('\n')) else "",
                suggestion="Add a semicolon (;) to terminate the execute command"
            )
        
        # Consume the semicolon
        self.current += 1
        self.column += 1
        
        # Create the execute command token with full content
        content = ''.join(content_parts).strip()
        full_command = f"execute {content};"
        self.tokens.append(Token(TokenType.EXECUTE, full_command, execute_start_line, execute_start_column))
    
    def _is_inside_control_structure(self, source: str) -> bool:
        """Check if we're inside a control structure (if/while)."""
        # Look backwards to see if we're inside a control structure
        # This is a simplified check - in a more robust implementation,
        # we would track the parsing context more carefully
        
        # For now, let's be conservative and only apply special handling
        # when we're clearly at the top level
        brace_count = 0
        for i in range(self.current):
            if source[i] == '{':
                brace_count += 1
            elif source[i] == '}':
                brace_count -= 1
        
        # If we're inside braces, we're likely in a control structure
        return brace_count > 0
    
    def _scan_operator_or_delimiter(self, source: str):
        """Scan operators and delimiters."""
        char = source[self.current]
        next_char = source[self.current + 1] if self.current + 1 < len(source) else None
        
        # Two-character operators
        if next_char:
            two_char = char + next_char
            if two_char in ['==', '!=', '<=', '>=', '&&', '||']:
                self.current += 2
                self.column += 2
                
                operator_map = {
                    '==': TokenType.EQUAL,
                    '!=': TokenType.NOT_EQUAL,
                    '<=': TokenType.LESS_EQUAL,
                    '>=': TokenType.GREATER_EQUAL,
                    '&&': TokenType.AND,
                    '||': TokenType.OR,
                }
                
                self.tokens.append(Token(operator_map[two_char], two_char, self.line, self.column - 2))
                return
        
        # Single-character operators and delimiters
        self.current += 1
        self.column += 1
        
        operator_map = {
            '=': TokenType.ASSIGN,
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '%': TokenType.MODULO,
            '<': TokenType.LANGLE,  # Use LANGLE for scope syntax, handle LESS in context
            '>': TokenType.RANGLE,  # Use RANGLE for scope syntax, handle GREATER in context
            ';': TokenType.SEMICOLON,
            ',': TokenType.COMMA,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '.': TokenType.DOT,
            ':': TokenType.COLON,
            '!': TokenType.RAW,  # Allow exclamation marks in text
            '?': TokenType.RAW,  # Allow question marks in text
            '@': TokenType.RAW,  # Allow @ for player selectors
            '#': TokenType.RAW,  # Allow # for tags
            '~': TokenType.RAW,  # Allow ~ for relative coordinates
            '^': TokenType.RAW,  # Allow ^ for relative coordinates
        }
        
        if char in operator_map:
            self.tokens.append(Token(operator_map[char], char, self.line, self.column - 1))
        else:
            # Unknown character - report error
            raise create_lexer_error(
                message=f"Unexpected character '{char}'",
                file_path=self.source_file,
                line=self.line,
                column=self.column - 1,
                line_content=source[self.line-1:self.line] if self.line <= len(source.split('\n')) else "",
                suggestion=f"Remove or replace the unexpected character '{char}'"
            )


def create_lexer_error(message: str, file_path: Optional[str] = None,
                      line: Optional[int] = None, column: Optional[int] = None,
                      line_content: Optional[str] = None, suggestion: Optional[str] = None) -> MDLLexerError:
    """Create a lexer error with common suggestions."""
    if not suggestion:
        if "unterminated string" in message.lower():
            suggestion = "Add a closing quote to terminate the string"
        elif "unterminated scope selector" in message.lower():
            suggestion = "Add a closing '>' to terminate the scope selector"
        elif "missing closing" in message.lower():
            suggestion = "Add the missing closing character"
        elif "unexpected character" in message.lower():
            suggestion = "Remove or replace the unexpected character"
    
    return MDLLexerError(
        message=message,
        file_path=file_path,
        line=line,
        column=column,
        line_content=line_content,
        suggestion=suggestion
    )


def lex_mdl_js(source: str, source_file: str = None) -> List[Token]:
    """Lex JavaScript-style MDL source code into tokens."""
    lexer = MDLLexer(source_file)
    return lexer.lex(source)
