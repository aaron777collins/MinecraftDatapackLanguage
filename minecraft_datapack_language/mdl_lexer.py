"""
MDL Lexer - Clean, extensible lexer for Minecraft Datapack Language
Fully supports the language specification defined in language-reference.md
"""

import re
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from .mdl_errors import MDLLexerError


@dataclass
class Token:
    """Represents a single token in the MDL language."""
    type: str
    value: str
    line: int
    column: int
    
    def __repr__(self) -> str:
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"


class TokenType:
    """All possible token types in the MDL language."""
    
    # Keywords (Reserved Words)
    PACK = "PACK"
    NAMESPACE = "NAMESPACE"
    FUNCTION = "FUNCTION"
    VAR = "VAR"
    NUM = "NUM"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    SCHEDULED_WHILE = "SCHEDULED_WHILE"
    ON_LOAD = "ON_LOAD"
    ON_TICK = "ON_TICK"
    EXEC = "EXEC"
    TAG = "TAG"
    
    # Tag Types (Resource Categories)
    RECIPE = "RECIPE"
    LOOT_TABLE = "LOOT_TABLE"
    ADVANCEMENT = "ADVANCEMENT"
    ITEM_MODIFIER = "ITEM_MODIFIER"
    PREDICATE = "PREDICATE"
    STRUCTURE = "STRUCTURE"
    
    # Operators
    PLUS = "PLUS"                    # +
    MINUS = "MINUS"                  # -
    MULTIPLY = "MULTIPLY"            # *
    DIVIDE = "DIVIDE"                # /
    ASSIGN = "ASSIGN"                # =
    EQUAL = "EQUAL"                  # ==
    NOT_EQUAL = "NOT_EQUAL"          # !=
    GREATER = "GREATER"              # >
    LESS = "LESS"                    # <
    GREATER_EQUAL = "GREATER_EQUAL"  # >=
    LESS_EQUAL = "LESS_EQUAL"        # <=
    AND = "AND"                      # &&
    OR = "OR"                        # ||
    NOT = "NOT"                      # ! (logical not)
    
    # Delimiters
    SEMICOLON = "SEMICOLON"          # ;
    COMMA = "COMMA"                  # ,
    COLON = "COLON"                  # :
    
    # Brackets and Braces
    LPAREN = "LPAREN"                # (
    RPAREN = "RPAREN"                # )
    LBRACE = "LBRACE"                # {
    RBRACE = "RBRACE"                # }
    LBRACKET = "LBRACKET"            # [
    RBRACKET = "RBRACKET"            # ]
    LANGLE = "LANGLE"                # < (for scope syntax)
    RANGLE = "RANGLE"                # > (for scope syntax)
    
    # Special Tokens
    DOLLAR = "DOLLAR"                # $ (variable substitution)
    QUOTE = "QUOTE"                  # " (string literal delimiter)
    EXCLAMATION = "EXCLAMATION"      # ! (for raw blocks)
    RANGE = "RANGE"                  # .. (range operator)
    DOT = "DOT"                      # . (for paths in with-clause)
    
    # Literals
    IDENTIFIER = "IDENTIFIER"        # Variable names, function names, etc.
    NUMBER = "NUMBER"                # Numbers (integers and floats)
    
    # Special
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    COMMENT = "COMMENT"              # Comments (ignored during parsing)
    RAW_CONTENT = "RAW_CONTENT"      # Raw content inside raw blocks
    MACRO_LINE = "MACRO_LINE"        # Entire macro line starting with '$' at line-begin


class MDLLexer:
    """
    Clean, extensible lexer for the MDL language.
    
    Features:
    - Full support for all language constructs defined in the spec
    - Clean, readable code structure
    - Easy to extend with new token types
    - Comprehensive error handling
    - Efficient tokenization with minimal memory usage
    """
    
    def __init__(self, source_file: str = None):
        self.source_file = source_file
        self.reset()
    
    def reset(self):
        """Reset the lexer state."""
        self.tokens = []
        self.current = 0
        self.start = 0
        self.line = 1
        self.column = 1
        self.in_raw_mode = False
        self.source = ""
    
    def lex(self, source: str) -> List[Token]:
        """
        Lex the source code into tokens.
        
        Args:
            source: The source code string to tokenize
            
        Returns:
            List of Token objects representing the source code
            
        Raises:
            MDLLexerError: If there's a lexical error in the source code
        """
        self.reset()
        self.source = source
        
        while self.current < len(source):
            self.start = self.current
            self._scan_token()
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    def _scan_token(self):
        """Scan a single token from the source."""
        if self.current >= len(self.source):
            return
        
        char = self.source[self.current]
        
        # Handle raw mode
        if self.in_raw_mode:
            self._scan_raw_text()
            return
        
        # Handle whitespace and newlines
        if char.isspace():
            self._scan_whitespace()
            return
        
        # Handle comments
        if char == '/' and self._peek(1) == '/':
            self._scan_single_line_comment()
            return
        
        if char == '/' and self._peek(1) == '*':
            self._scan_multi_line_comment()
            return
        
        # Handle strings (quotes) - support both ' and "
        if char == '"' or char == "'":
            self._scan_string(quote_char=char)
            return
        
        # Handle raw block markers
        if char == '$' and self._peek(1) == '!' and self._peek(2) == 'r':
            if self._peek(3) == 'a' and self._peek(4) == 'w':
                self._scan_raw_block_start()
                return
        

        
        # Handle macro line: '$' as first non-space on the line (not $!raw)
        if char == '$' and self._is_line_start_nonspace():
            self._scan_macro_line()
            return

        # Handle variable substitution
        if char == '$':
            self._scan_variable_substitution()
            return
        
        # Handle numbers
        if char.isdigit():
            self._scan_number()
            return
        
        # Handle identifiers and keywords
        if char.isalpha() or char == '_':
            self._scan_identifier()
            return
        
        # Handle @ selectors (like @s, @a, @e[type=armor_stand])
        if char == '@':
            self._scan_selector()
            return
        
        # Handle scope selectors (<@s>, <@a[team=red]>, etc.)
        if char == '<':
            # Check if this is a scope selector (followed by @ or identifier)
            if (self.current + 1 < len(self.source) and 
                (self.source[self.current + 1] == '@' or 
                 self.source[self.current + 1].isalpha() or 
                 self.source[self.current + 1] == '_')):
                self._scan_scope_selector()
                return
            # Otherwise, treat as LESS operator (handled by _scan_operator_or_delimiter)
        
        # Handle operators and delimiters
        self._scan_operator_or_delimiter()
    
    def _scan_whitespace(self):
        """Scan whitespace characters."""
        while (self.current < len(self.source) and 
               self.source[self.current].isspace()):
            char = self.source[self.current]
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.current += 1
    
    def _scan_single_line_comment(self):
        """Scan a single-line comment (// ...)."""
        # Skip //
        self.current += 2
        self.column += 2
        
        # Scan until end of line or end of source
        while (self.current < len(self.source) and 
               self.source[self.current] != '\n'):
            self.current += 1
            self.column += 1
        
        # Comments are ignored - no token generated
    
    def _scan_multi_line_comment(self):
        """Scan a multi-line comment (/* ... */)."""
        # Skip /*
        self.current += 2
        self.column += 2
        
        # Scan until we find */
        while (self.current < len(self.source) - 1):
            if (self.source[self.current] == '*' and 
                self.source[self.current + 1] == '/'):
                self.current += 2
                self.column += 2
                return
            
            if self.source[self.current] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.current += 1
        
        # Unterminated comment
        self._error("Unterminated multi-line comment", "Add */ to close the comment")
    
    def _scan_string(self, quote_char='"'):
        """Scan a string literal (quoted text)."""
        # Skip opening quote
        self.current += 1
        self.column += 1
        
        start_line = self.line
        start_column = self.column
        
        # Scan until closing quote
        while (self.current < len(self.source) and 
               self.source[self.current] != quote_char):
            if self.source[self.current] == '\n':
                self._error("Unterminated string literal", "Add a closing quote")
            
            if self.source[self.current] == '\\' and self.current + 1 < len(self.source):
                # Handle escape sequences
                self.current += 2
                self.column += 2
            else:
                self.current += 1
                self.column += 1
        
        if self.current >= len(self.source):
            self._error("Unterminated string literal at end of file", "Add a closing quote")
        
        # Include closing quote
        self.current += 1
        self.column += 1
        
        # Generate QUOTE token for the opening quote
        self.tokens.append(Token(TokenType.QUOTE, quote_char, start_line, start_column))
        
        # Generate IDENTIFIER token for the string content
        string_content = self.source[self.start + 1:self.current - 1]
        self.tokens.append(Token(TokenType.IDENTIFIER, string_content, start_line, start_column + 1))
        
        # Generate QUOTE token for the closing quote
        self.tokens.append(Token(TokenType.QUOTE, quote_char, self.line, self.column - 1))

    def _is_line_start_nonspace(self) -> bool:
        """Return True if current position is at the first non-space character in the line."""
        # Find beginning of current line
        idx = self.current - 1
        while idx >= 0 and self.source[idx] != '\n':
            if not self.source[idx].isspace():
                return False
            idx -= 1
        return True

    def _scan_macro_line(self):
        """Scan a full macro line starting with '$' as first non-space char."""
        # Capture from current to end of line (excluding trailing newline)
        line_start = self.current
        while self.current < len(self.source) and self.source[self.current] != '\n':
            self.current += 1
            self.column += 1
        content = self.source[line_start:self.current]
        self.tokens.append(Token(TokenType.MACRO_LINE, content, self.line, 1))
    
    def _scan_raw_block_start(self):
        """Scan the start of a raw block ($!raw)."""
        # Consume $!raw
        self.current += 5
        self.column += 5
        
        # Generate tokens: $ ! raw
        self.tokens.append(Token(TokenType.DOLLAR, "$", self.line, self.column - 5))
        self.tokens.append(Token(TokenType.EXCLAMATION, "!", self.line, self.column - 4))
        self.tokens.append(Token(TokenType.IDENTIFIER, "raw", self.line, self.column - 3))
        
        self.in_raw_mode = True
    

    
    def _scan_raw_text(self):
        """Scan raw text inside a raw block."""
        # Remember where the raw content starts
        content_start = self.current
        
        # Consume all characters until we find raw!$
        while self.current < len(self.source) - 4:
            if (self.source[self.current:self.current + 5] == 'raw!$'):
                # Found the end marker - extract the content
                raw_content = self.source[content_start:self.current]
                # Trim leading/trailing whitespace on each line within the raw block
                try:
                    lines = raw_content.split('\n')
                    trimmed_lines = [ln.strip() for ln in lines]
                    raw_content = '\n'.join(trimmed_lines)
                except Exception:
                    # If anything goes wrong, fall back to original content
                    pass
                
                # Generate a single RAW_CONTENT token with all the content
                self.tokens.append(Token(TokenType.RAW_CONTENT, raw_content, self.line, self.column))
                
                # Consume the end marker and exit raw mode
                self.current += 5
                self.column += 5
                self.in_raw_mode = False
                
                # Generate tokens for the end marker: raw ! $
                self.tokens.append(Token(TokenType.IDENTIFIER, "raw", self.line, self.column - 5))
                self.tokens.append(Token(TokenType.EXCLAMATION, "!", self.line, self.column - 2))
                self.tokens.append(Token(TokenType.DOLLAR, "$", self.line, self.column - 1))
                return
            
            if self.source[self.current] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.current += 1
        
        # If we didn't find the end marker, it's an error
        if self.current >= len(self.source) - 4:
            self._error("Unterminated raw block", "Add 'raw!$' to close the raw block")
    
    def _scan_variable_substitution(self):
        """Scan variable substitution ($variable<scope>$)."""
        # Skip opening $
        self.current += 1
        self.column += 1
        
        # Generate DOLLAR token
        self.tokens.append(Token(TokenType.DOLLAR, "$", self.line, self.column - 1))
        
        # Scan variable name (start from current position, not from start)
        self.start = self.current
        self._scan_identifier()
        
        # Check for scope selector
        if (self.current < len(self.source) and 
            self.source[self.current] == '<'):
            self._scan_scope_selector()
        
        # Check for closing $
        if (self.current < len(self.source) and 
            self.source[self.current] == '$'):
            self.current += 1
            self.column += 1
            self.tokens.append(Token(TokenType.DOLLAR, "$", self.line, self.column - 1))
        else:
            self._error("Unterminated variable substitution", "Add $ to close the variable substitution")
    
    def _scan_selector(self):
        """Scan a selector (@s, @a, @e[type=armor_stand], etc.)."""
        # Consume @
        self.current += 1
        self.column += 1
        
        # Scan selector identifier
        self._scan_identifier()
        
        # Check for bracket parameters
        if (self.current < len(self.source) and 
            self.source[self.current] == '['):
            self._scan_selector_parameters()
    
    def _scan_selector_parameters(self):
        """Scan selector parameters in brackets."""
        # Consume [
        self.current += 1
        self.column += 1
        
        # Generate LBRACKET token
        self.tokens.append(Token(TokenType.LBRACKET, "[", self.line, self.column - 1))
        
        # Remember where the parameters start (after the opening [)
        param_start = self.current
        
        # Scan until we find the matching ]
        bracket_count = 1
        while (self.current < len(self.source) and bracket_count > 0):
            if self.source[self.current] == '[':
                bracket_count += 1
            elif self.source[self.current] == ']':
                bracket_count -= 1
            
            if bracket_count > 0:
                if self.source[self.current] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.current += 1
        
        if bracket_count == 0:
            # Successfully found closing ]
            # Generate IDENTIFIER token for the entire parameter content
            param_content = self.source[param_start:self.current]
            self.tokens.append(Token(TokenType.IDENTIFIER, param_content, self.line, self.column - len(param_content)))
            
            # Generate RBRACKET token
            self.current += 1
            self.column += 1
            self.tokens.append(Token(TokenType.RBRACKET, "]", self.line, self.column - 1))
        else:
            # Unterminated selector parameters
            self._error("Unterminated selector parameters", "Add ] to close the selector parameters")
    
    def _scan_scope_selector(self):
        """Scan a scope selector (<@s>, <@a[team=red]>, etc.)."""
        # Consume <
        self.current += 1
        self.column += 1
        
        # Generate LANGLE token
        self.tokens.append(Token(TokenType.LANGLE, "<", self.line, self.column - 1))
        
        # Scan selector content - this could be @s, @a[team=red], etc.
        if (self.current < len(self.source) and 
            self.source[self.current] == '@'):
            # Handle @ selector - start from current position
            self.start = self.current
            self._scan_selector()
        else:
            # Handle other identifier - start from current position
            self.start = self.current
            self._scan_identifier()
        
        # Consume >
        if (self.current < len(self.source) and 
            self.source[self.current] == '>'):
            self.current += 1
            self.column += 1
            self.tokens.append(Token(TokenType.RANGLE, ">", self.line, self.column - 1))
        else:
            self._error("Unterminated scope selector", "Add > to close the scope selector")
    
    def _scan_number(self):
        """Scan a number literal."""
        # Scan integer part
        while (self.current < len(self.source) and 
               self.source[self.current].isdigit()):
            self.current += 1
            self.column += 1
        
        # Check for decimal point
        if (self.current < len(self.source) and 
            self.source[self.current] == '.' and
            self.current + 1 < len(self.source) and
            self.source[self.current + 1].isdigit()):
            self.current += 1  # consume decimal point
            self.column += 1
            
            # Scan fractional part
            while (self.current < len(self.source) and 
                   self.source[self.current].isdigit()):
                self.current += 1
                self.column += 1
        
        number_text = self.source[self.start:self.current]
        self.tokens.append(Token(TokenType.NUMBER, number_text, self.line, self.column - len(number_text)))
    
    def _scan_identifier(self):
        """Scan an identifier or keyword."""
        # Scan identifier characters
        while (self.current < len(self.source) and 
               (self.source[self.current].isalnum() or 
                self.source[self.current] == '_')):
            self.current += 1
            self.column += 1
        
        identifier_text = self.source[self.start:self.current]
        
        # Check if it's a keyword
        token_type = self._get_keyword_type(identifier_text)
        
        self.tokens.append(Token(token_type, identifier_text, self.line, self.column - len(identifier_text)))
    
    def _scan_operator_or_delimiter(self):
        """Scan operators and delimiters."""
        char = self.source[self.current]
        
        # Handle two-character operators first
        if self.current + 1 < len(self.source):
            two_char = self.source[self.current:self.current + 2]
            
            if two_char in ['==', '!=', '>=', '<=', '..', '&&', '||']:
                self.current += 2
                self.column += 2
                
                token_type = {
                    '==': TokenType.EQUAL,
                    '!=': TokenType.NOT_EQUAL,
                    '>=': TokenType.GREATER_EQUAL,
                    '<=': TokenType.LESS_EQUAL,
                    '..': TokenType.RANGE,
                    '&&': TokenType.AND,
                    '||': TokenType.OR
                }[two_char]
                
                self.tokens.append(Token(token_type, two_char, self.line, self.column - 2))
                return
        
        # Handle single-character operators and delimiters
        token_map = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '=': TokenType.ASSIGN,
            '>': TokenType.GREATER,
            '<': TokenType.LESS,
            '!': TokenType.NOT,
            ';': TokenType.SEMICOLON,
            ',': TokenType.COMMA,
            ':': TokenType.COLON,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '.': TokenType.DOT
        }
        
        if char in token_map:
            self.current += 1
            self.column += 1
            self.tokens.append(Token(token_map[char], char, self.line, self.column - 1))
        else:
            # Unknown character
            self._error(f"Unknown character '{char}'", f"Remove or replace the character '{char}'")
    
    def _get_keyword_type(self, text: str) -> str:
        """Get the token type for a keyword."""
        keyword_map = {
            # Keywords
            'pack': TokenType.PACK,
            'namespace': TokenType.NAMESPACE,
            'function': TokenType.FUNCTION,
            'var': TokenType.VAR,
            'num': TokenType.NUM,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'scheduledwhile': TokenType.SCHEDULED_WHILE,
            'on_load': TokenType.ON_LOAD,
            'on_tick': TokenType.ON_TICK,
            'exec': TokenType.EXEC,
            'tag': TokenType.TAG,
            
            # Tag types
            'recipe': TokenType.RECIPE,
            'loot_table': TokenType.LOOT_TABLE,
            'advancement': TokenType.ADVANCEMENT,
            'item_modifier': TokenType.ITEM_MODIFIER,
            'predicate': TokenType.PREDICATE,
            'structure': TokenType.STRUCTURE
        }
        
        return keyword_map.get(text.lower(), TokenType.IDENTIFIER)
    
    def _peek(self, offset: int) -> Optional[str]:
        """Peek ahead in the source without consuming characters."""
        if self.current + offset < len(self.source):
            return self.source[self.current + offset]
        return None
    
    def _error(self, message: str, suggestion: str):
        """Raise a lexer error with context information."""
        # Get the current line content for better error reporting
        lines = self.source.split('\n')
        line_content = ""
        if self.line - 1 < len(lines):
            line_content = lines[self.line - 1]
        
        raise MDLLexerError(
            message=message,
            file_path=self.source_file,
            line=self.line,
            column=self.column,
            line_content=line_content,
            suggestion=suggestion
        )
    
    def get_token_summary(self) -> Dict[str, Any]:
        """Get a summary of the tokenization results."""
        token_counts = {}
        for token in self.tokens:
            if token.type != TokenType.EOF:
                token_counts[token.type] = token_counts.get(token.type, 0) + 1
        
        return {
            'total_tokens': len(self.tokens),
            'token_counts': token_counts,
            'lines_processed': self.line
        }
