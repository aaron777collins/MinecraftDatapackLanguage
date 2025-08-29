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
    IF = "IF"
    ELSE = "ELSE"
    ELSE_IF = "ELSE_IF"
    WHILE = "WHILE"

    IN = "IN"
    ON_TICK = "ON_TICK"
    ON_LOAD = "ON_LOAD"
    TAG = "TAG"
    ADD = "ADD"
    
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
    DOT = "DOT"
    
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
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
    
            'in': TokenType.IN,
            'on_tick': TokenType.ON_TICK,
            'on_load': TokenType.ON_LOAD,
            'tag': TokenType.TAG,
            'add': TokenType.ADD,
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
    
    def _scan_variable_substitution(self, source: str):
        """Scan a variable substitution ($variable$)."""
        self.current += 1  # consume $
        self.column += 1
        
        # Scan the variable name
        while (self.current < len(source) and 
               (source[self.current].isalnum() or source[self.current] == '_')):
            self.current += 1
            self.column += 1
        
        # Check for closing $
        if (self.current < len(source) and 
            source[self.current] == '$'):
            self.current += 1
            self.column += 1
            
            text = source[self.start:self.current]
            variable_name = text[1:-1]  # Remove $ symbols
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
            '<': TokenType.LESS,
            '>': TokenType.GREATER,
            ';': TokenType.SEMICOLON,
            ',': TokenType.COMMA,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '.': TokenType.DOT,
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
