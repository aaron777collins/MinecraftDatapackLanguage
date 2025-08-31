"""
MDL Lexer - Simplified JavaScript-style syntax with curly braces and semicolons
Handles basic control structures and number variables only
"""

import re
from dataclasses import dataclass
from typing import List


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
    
    # Variable substitution
    VARIABLE_SUB = "VARIABLE_SUB"  # $variable$


class MDLLexer:
    """Lexer for simplified MDL language."""
    
    def __init__(self):
        self.tokens = []
        self.current = 0
        self.start = 0
        self.line = 1
        self.column = 1
    
    def lex(self, source: str) -> List[Token]:
        """Lex the source code into tokens."""
        self.tokens = []
        self.current = 0
        self.start = 0
        self.line = 1
        self.column = 1
        
        while self.current < len(source):
            self.start = self.current
            self._scan_token(source)
        
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    def _scan_token(self, source: str):
        """Scan a single token."""
        char = source[self.current]
        
        # Skip whitespace
        if char.isspace():
            if char == '\n':
                self.line += 1
                self.column = 1
            elif char == '\r':
                # Handle Windows line endings (\r\n)
                if self.current + 1 < len(source) and source[self.current + 1] == '\n':
                    self.current += 1  # Skip the \r
                    self.line += 1
                    self.column = 1
                else:
                    # Just a \r without \n, treat as newline
                    self.line += 1
                    self.column = 1
            else:
                self.column += 1
            self.current += 1
            return
        
        # Skip comments
        if char == '/' and self.current + 1 < len(source) and source[self.current + 1] == '/':
            self._scan_comment(source)
            return
        
        # Handle raw text blocks
        if char == '$' and self.current + 4 < len(source) and source[self.current:self.current + 5] == '$!raw':
            self._scan_raw_text(source)
            return
        
        # Handle identifiers and keywords
        if char.isalpha() or char == '_' or char == '@':
            self._scan_identifier(source)
            return
        
        # Handle numbers
        if char.isdigit():
            self._scan_number(source)
            return
        
        # Handle strings
        if char in ['"', "'"]:
            self._scan_string(source)
            return
        
        # Handle variable substitutions
        if char == '$':
            self._scan_variable_substitution(source)
            return
        
        # Handle operators and delimiters
        self._scan_operator_or_delimiter(source)
    
    def _scan_comment(self, source: str):
        """Scan a comment."""
        while self.current < len(source) and source[self.current] != '\n':
            if source[self.current] == '\r':
                # Handle Windows line endings in comments
                if self.current + 1 < len(source) and source[self.current + 1] == '\n':
                    break  # End of comment at \r\n
                else:
                    break  # End of comment at \r
            self.current += 1
            self.column += 1
    
    def _scan_identifier(self, source: str):
        """Scan an identifier or keyword."""
        # Special handling for @ - it should be followed by alphanumeric characters
        if source[self.start] == '@':
            self.current += 1
            self.column += 1
            # Continue scanning for alphanumeric characters after @
            while (self.current < len(source) and 
                   (source[self.current].isalnum() or source[self.current] == '_')):
                self.current += 1
                self.column += 1
        else:
            # Regular identifier scanning
            while (self.current < len(source) and 
                   (source[self.current].isalnum() or source[self.current] == '_')):
                self.current += 1
                self.column += 1
        
        text = source[self.start:self.current]
        
        # Check for keywords
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
            
            # Registry types
            'recipe': TokenType.RECIPE,
            'loot_table': TokenType.LOOT_TABLE,
            'advancement': TokenType.ADVANCEMENT,
            'predicate': TokenType.PREDICATE,
            'item_modifier': TokenType.ITEM_MODIFIER,
            'structure': TokenType.STRUCTURE,
        }
        
        token_type = keyword_map.get(text, TokenType.IDENTIFIER)
        
        # Special handling for "else if" - look ahead for "if"
        if text == 'else' and self.current < len(source):
            # Skip whitespace
            temp_current = self.current
            while (temp_current < len(source) and 
                   source[temp_current].isspace()):
                temp_current += 1
            
            # Check if next token is "if"
            if (temp_current + 1 < len(source) and 
                source[temp_current:temp_current + 2] == 'if' and
                (temp_current + 2 >= len(source) or 
                 not source[temp_current + 2].isalnum())):
                # This is "else if", we'll handle it in the parser
                pass
        
        # Check for scope selector (<selector>) after identifier
        scope_selector = None
        if (self.current < len(source) and 
            source[self.current] == '<'):
            # Found scope selector, scan it
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
                # Unterminated scope selector, treat as regular identifier
                self.current = scope_start - 1  # Backtrack to before <
                self.column = self.column - (self.current - scope_start + 1)
        
        # If we have a scope selector, include it in the token
        if scope_selector:
            text = f"{text}<{scope_selector}>"
        
        self.tokens.append(Token(token_type, text, self.line, self.start - self.column + 1))
    
    def _scan_number(self, source: str):
        """Scan a number."""
        while (self.current < len(source) and 
               (source[self.current].isdigit() or source[self.current] == '.')):
            self.current += 1
            self.column += 1
        
        text = source[self.start:self.current]
        self.tokens.append(Token(TokenType.NUMBER, text, self.line, self.start - self.column + 1))
    
    def _scan_string(self, source: str):
        """Scan a string literal."""
        quote_char = source[self.current]
        self.current += 1
        self.column += 1
        
        while (self.current < len(source) and 
               source[self.current] != quote_char):
            if source[self.current] == '\n':
                self.line += 1
                self.column = 1
            elif source[self.current] == '\r':
                # Handle Windows line endings in strings
                if self.current + 1 < len(source) and source[self.current + 1] == '\n':
                    self.current += 1  # Skip the \r
                    self.line += 1
                    self.column = 1
                else:
                    # Just a \r without \n, treat as newline
                    self.line += 1
                    self.column = 1
            else:
                self.column += 1
            self.current += 1
        
        if self.current < len(source):
            self.current += 1
            self.column += 1
        
        text = source[self.start:self.current]
        self.tokens.append(Token(TokenType.STRING, text, self.line, self.start - self.column + 1))
    
    def _scan_raw_text(self, source: str):
        """Scan raw text block ($!raw ... raw!$)."""
        # Consume $!raw
        self.current += 5  # $!raw
        self.column += 5
        
        # Add RAW_START token
        self.tokens.append(Token(TokenType.RAW_START, "$!raw", self.line, self.start - self.column + 1))
        
        # Scan until we find raw!$
        raw_text = ""
        while self.current < len(source):
            # Check for raw!$ ending
            if (self.current + 4 < len(source) and 
                source[self.current:self.current + 5] == 'raw!$'):
                self.current += 5  # consume raw!$
                self.column += 5
                break
            
            char = source[self.current]
            if char == '\n':
                self.line += 1
                self.column = 1
            elif char == '\r':
                # Handle Windows line endings
                if self.current + 1 < len(source) and source[self.current + 1] == '\n':
                    self.current += 1  # Skip the \r
                    self.line += 1
                    self.column = 1
                else:
                    # Just a \r without \n, treat as newline
                    self.line += 1
                    self.column = 1
            else:
                self.column += 1
            
            raw_text += char
            self.current += 1
        else:
            # Reached end of source without finding raw!$
            raise RuntimeError(f"Unterminated raw text block starting at line {self.line}")
        
        # Add the raw text content
        self.tokens.append(Token(TokenType.RAW, raw_text, self.line, self.start - self.column + 1))
        
        # Add RAW_END token
        self.tokens.append(Token(TokenType.RAW_END, "raw!$", self.line, self.start - self.column + 1))
    
    def _scan_variable_substitution(self, source: str):
        """Scan a variable substitution ($variable$ or $variable<selector>$)."""
        self.current += 1  # consume $
        self.column += 1
        
        # Scan the variable name
        while (self.current < len(source) and 
               (source[self.current].isalnum() or source[self.current] == '_')):
            self.current += 1
            self.column += 1
        
        # Check for scope selector (<selector>)
        scope_selector = None
        if (self.current < len(source) and 
            source[self.current] == '<'):
            # Found scope selector, scan it
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
                # Unterminated scope selector, treat as regular variable
                self.current = scope_start - 1  # Backtrack to before <
                self.column = self.column - (self.current - scope_start + 1)
        
        # Check for closing $
        if (self.current < len(source) and 
            source[self.current] == '$'):
            self.current += 1
            self.column += 1
            
            text = source[self.start:self.current]
            variable_name = text[1:-1]  # Remove $ symbols
            
            # If we have a scope selector, include it in the token
            if scope_selector:
                variable_name = f"{variable_name}<{scope_selector}>"
            
            self.tokens.append(Token(TokenType.VARIABLE_SUB, variable_name, self.line, self.start - self.column + 1))
        else:
            # Not a valid variable substitution, treat as regular $
            self.tokens.append(Token(TokenType.IDENTIFIER, "$", self.line, self.start - self.column + 1))
    
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
                
                self.tokens.append(Token(operator_map[two_char], two_char, self.line, self.start - self.column + 1))
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
        }
        
        if char in operator_map:
            self.tokens.append(Token(operator_map[char], char, self.line, self.start - self.column + 1))
        else:
            # Unknown character - treat as identifier
            self.tokens.append(Token(TokenType.IDENTIFIER, char, self.line, self.start - self.column + 1))


def lex_mdl_js(source: str) -> List[Token]:
    """Lex JavaScript-style MDL source code into tokens."""
    lexer = MDLLexer()
    return lexer.lex(source)
