"""
MDL Lexer - Proper lexical analysis for MDL language
Handles unlimited nesting and all control structures
"""

import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Tuple

class TokenType(Enum):
    # Keywords
    PACK = "PACK"
    NAMESPACE = "NAMESPACE"
    FUNCTION = "FUNCTION"
    ON_TICK = "ON_TICK"
    ON_LOAD = "ON_LOAD"
    TAG = "TAG"
    ADD = "ADD"
    
    # Control flow
    IF = "IF"
    ELSE = "ELSE"
    ELSE_IF = "ELSE_IF"
    WHILE = "WHILE"
    FOR = "FOR"
    IN = "IN"
    
    # Literals
    STRING = "STRING"
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"
    
    # Punctuation
    COLON = "COLON"
    COMMA = "COMMA"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    
    # Special
    INDENT = "INDENT"
    DEDENT = "DEDENT"
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    COMMENT = "COMMENT"
    COMMAND = "COMMAND"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    indent_level: int = 0

class MDLLexer:
    """Proper lexer for MDL language with unlimited nesting support."""
    
    def __init__(self, source: str):
        self.source = source
        self.lines = source.splitlines()
        self.current_line = 0
        self.current_column = 0
        self.tokens: List[Token] = []
        self.indent_stack = [0]
        
    def tokenize(self) -> List[Token]:
        """Tokenize the MDL source code with proper indentation handling."""
        self.tokens = []
        
        for line_num, line in enumerate(self.lines):
            self.current_line = line_num + 1
            
            # Skip empty lines and comments
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                if stripped.startswith('#'):
                    self.tokens.append(Token(TokenType.COMMENT, stripped, line_num + 1, 0))
                continue
            
            # Calculate indentation
            indent = len(line) - len(line.lstrip())
            
            # Handle indentation changes
            self._handle_indentation(indent, line_num + 1)
            
            # Tokenize the line content
            self._tokenize_line(stripped, line_num + 1)
            
            # Add newline token
            self.tokens.append(Token(TokenType.NEWLINE, "\n", line_num + 1, len(line)))
        
        # Add final dedents and EOF
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, "", len(self.lines) + 1, 0, self.indent_stack[-1]))
        
        self.tokens.append(Token(TokenType.EOF, "", len(self.lines) + 1, 0))
        return self.tokens
    
    def _handle_indentation(self, indent: int, line: int):
        """Handle indentation changes."""
        current_indent = self.indent_stack[-1]
        
        if indent > current_indent:
            # Indent
            self.indent_stack.append(indent)
            self.tokens.append(Token(TokenType.INDENT, "    " * (indent // 4), line, 0, indent))
        elif indent < current_indent:
            # Dedent
            while len(self.indent_stack) > 1 and self.indent_stack[-1] > indent:
                self.indent_stack.pop()
                self.tokens.append(Token(TokenType.DEDENT, "", line, 0, self.indent_stack[-1]))
    
    def _tokenize_line(self, line: str, line_num: int):
        """Tokenize a single line of MDL code."""
        # Check for function declaration first (ends with colon)
        if line.startswith('function ') and line.endswith(':'):
            self.tokens.append(Token(TokenType.FUNCTION, "function", line_num, 0))
            func_name = line[9:-1].strip()  # Remove 'function ' and ':'
            # Handle quoted function names
            if func_name.startswith('"') and func_name.endswith('"'):
                self.tokens.append(Token(TokenType.STRING, func_name[1:-1], line_num, 10))
            else:
                # Handle unquoted function names
                self.tokens.append(Token(TokenType.STRING, func_name, line_num, 10))
            self.tokens.append(Token(TokenType.COLON, ":", line_num, len(line) - 1))
            return
        
        # Keywords that start statements
        keyword_patterns = [
            (r'^pack\b', TokenType.PACK),
            (r'^namespace\b', TokenType.NAMESPACE),
            (r'^function\b', TokenType.FUNCTION),
            (r'^on_tick\b', TokenType.ON_TICK),
            (r'^on_load\b', TokenType.ON_LOAD),
            (r'^tag\b', TokenType.TAG),
            (r'^add\b', TokenType.ADD),
            (r'^if\b', TokenType.IF),
            (r'^else\b', TokenType.ELSE),
            (r'^while\b', TokenType.WHILE),
            (r'^for\b', TokenType.FOR),
            (r'^in\b', TokenType.IN),
        ]
        
        # Check for keywords first
        for pattern, token_type in keyword_patterns:
            match = re.match(pattern, line)
            if match:
                self.tokens.append(Token(token_type, match.group(0), line_num, 0))
                remaining = line[match.end():].strip()
                if remaining:
                    self._tokenize_remaining(remaining, line_num)
                return
        
        # Check for "else if" pattern
        if line.startswith('else if'):
            self.tokens.append(Token(TokenType.ELSE_IF, "else if", line_num, 0))
            remaining = line[8:].strip()
            if remaining:
                self._tokenize_remaining(remaining, line_num)
            return
        
        # Check for function declaration (ends with colon)
        if line.startswith('function ') and line.endswith(':'):
            self.tokens.append(Token(TokenType.FUNCTION, "function", line_num, 0))
            func_name = line[9:-1].strip()  # Remove 'function ' and ':'
            # Handle quoted function names
            if func_name.startswith('"') and func_name.endswith('"'):
                self.tokens.append(Token(TokenType.STRING, func_name[1:-1], line_num, 10))
            else:
                # Handle unquoted function names
                self.tokens.append(Token(TokenType.STRING, func_name, line_num, 10))
            self.tokens.append(Token(TokenType.COLON, ":", line_num, len(line) - 1))
            return
        
        # Check for function call (but not function declaration)
        if line.startswith('function ') and not line.endswith(':'):
            self.tokens.append(Token(TokenType.FUNCTION, "function", line_num, 0))
            remaining = line[9:].strip()
            if remaining:
                self._tokenize_remaining(remaining, line_num)
            return
        
        # Check for colon at end (control structure)
        if line.endswith(':'):
            # This is a control structure
            base_line = line[:-1].strip()
            self._tokenize_control_structure(base_line, line_num)
            self.tokens.append(Token(TokenType.COLON, ":", line_num, len(line) - 1))
            return
        
        # Otherwise, treat as a command
        self.tokens.append(Token(TokenType.COMMAND, line, line_num, 0))
    
    def _tokenize_control_structure(self, line: str, line_num: int):
        """Tokenize a control structure line."""
        # Handle if statements
        if line.startswith('if '):
            self.tokens.append(Token(TokenType.IF, "if", line_num, 0))
            condition = line[3:].strip()
            # Handle quoted conditions properly
            if condition.startswith('"') and condition.endswith('"'):
                self.tokens.append(Token(TokenType.STRING, condition[1:-1], line_num, 4))
            else:
                self.tokens.append(Token(TokenType.STRING, condition, line_num, 4))
            return
        
        # Handle while statements
        if line.startswith('while '):
            self.tokens.append(Token(TokenType.WHILE, "while", line_num, 0))
            condition = line[6:].strip()
            # Handle quoted conditions properly
            if condition.startswith('"') and condition.endswith('"'):
                self.tokens.append(Token(TokenType.STRING, condition[1:-1], line_num, 7))
            else:
                self.tokens.append(Token(TokenType.STRING, condition, line_num, 7))
            return
        
        # Handle for loops
        if line.startswith('for '):
            self.tokens.append(Token(TokenType.FOR, "for", line_num, 0))
            remaining = line[4:].strip()
            self._tokenize_for_loop(remaining, line_num)
            return
        
        # Handle other declarations
        self._tokenize_remaining(line, line_num)
    
    def _tokenize_for_loop(self, line: str, line_num: int):
        """Tokenize a for loop declaration."""
        # Pattern: for <var> in <selector>
        parts = line.split()
        if len(parts) >= 3 and parts[1] == 'in':
            # Variable name
            self.tokens.append(Token(TokenType.IDENTIFIER, parts[0], line_num, 5))
            # 'in' keyword
            self.tokens.append(Token(TokenType.IN, "in", line_num, 5 + len(parts[0]) + 1))
            # Selector
            selector = ' '.join(parts[2:])
            self.tokens.append(Token(TokenType.STRING, selector, line_num, 5 + len(parts[0]) + 4))
    
    def _tokenize_remaining(self, line: str, line_num: int):
        """Tokenize remaining parts of a line."""
        # Handle quoted strings first (they might contain spaces)
        import re
        
        # Find all quoted strings
        quoted_strings = re.findall(r'"([^"]*)"', line)
        remaining_line = line
        
        # Replace quoted strings with placeholders
        for i, quoted in enumerate(quoted_strings):
            placeholder = f"__QUOTED_{i}__"
            remaining_line = remaining_line.replace(f'"{quoted}"', placeholder, 1)
        
        # Split the remaining line
        parts = remaining_line.split()
        
        # Process each part
        quoted_index = 0
        for part in parts:
            if part.startswith("__QUOTED_") and part.endswith("__"):
                # This is a placeholder for a quoted string
                self.tokens.append(Token(TokenType.STRING, quoted_strings[quoted_index], line_num, 0))
                quoted_index += 1
            elif part.isdigit():
                self.tokens.append(Token(TokenType.NUMBER, part, line_num, 0))
            elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_:]*$', part):
                self.tokens.append(Token(TokenType.IDENTIFIER, part, line_num, 0))
            else:
                self.tokens.append(Token(TokenType.STRING, part, line_num, 0))

def lex_mdl(source: str) -> List[Token]:
    """Convenience function to lex MDL source code."""
    lexer = MDLLexer(source)
    return lexer.tokenize()
