"""
MDL Error Classes - Custom error types with detailed location information
"""

from dataclasses import dataclass
from typing import Optional, List, Any
import os

# Import color utilities
try:
    from .cli_colors import color
except ImportError:
    # Fallback if colors aren't available
    class DummyColor:
        def __getattr__(self, name):
            return lambda text: text
    color = DummyColor()


@dataclass
class MDLError(BaseException):
    """Base class for MDL errors with location information."""
    message: str
    file_path: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
    line_content: Optional[str] = None
    error_type: str = "error"
    suggestion: Optional[str] = None
    context_lines: int = 2
    
    def __str__(self) -> str:
        """Format error message with location information."""
        parts = []
        
        if self.file_path:
            # Show relative path if possible
            try:
                rel_path = os.path.relpath(self.file_path)
                parts.append(f"{color.file_path('File:')} {color.file_path(rel_path)}")
            except ValueError:
                parts.append(f"{color.file_path('File:')} {color.file_path(self.file_path)}")
        
        if self.line is not None:
            parts.append(f"{color.line_number('Line:')} {color.line_number(str(self.line))}")
            if self.column is not None:
                parts.append(f"{color.column_number('Column:')} {color.column_number(str(self.column))}")
        
        if self.line_content:
            parts.append(f"{color.context('Code:')} {color.context(self.line_content.strip())}")
            if self.column is not None:
                # Add a caret to show the exact position
                indent = " " * (self.column - 1)
                parts.append(f"      {indent}{color.error('^')}")
        
        parts.append(f"{color.error_type('Error:')} {color.error(self.message)}")
        
        if self.suggestion:
            parts.append(f"{color.suggestion('Suggestion:')} {color.suggestion(self.suggestion)}")
        
        # Add context if we have file and line information
        if self.file_path and self.line is not None:
            context = format_error_context(self.file_path, self.line, self.column, self.context_lines)
            if context:
                parts.append(f"\n{color.context('Context:')}\n{context}")
        
        return "\n".join(parts)
    
    def to_dict(self) -> dict:
        """Convert error to dictionary for JSON output."""
        return {
            "type": self.error_type,
            "message": self.message,
            "file": self.file_path,
            "line": self.line,
            "column": self.column,
            "line_content": self.line_content,
            "suggestion": self.suggestion
        }


@dataclass
class MDLSyntaxError(MDLError):
    """Syntax error in MDL code."""
    error_type: str = "syntax_error"
    
    def __str__(self) -> str:
        return f"{color.error_type('Syntax Error:')} {super().__str__()}"


@dataclass
class MDLLexerError(MDLError):
    """Error during lexical analysis."""
    error_type: str = "lexer_error"
    
    def __str__(self) -> str:
        return f"{color.error_type('Lexer Error:')} {super().__str__()}"


@dataclass
class MDLParserError(MDLError):
    """Error during parsing."""
    error_type: str = "parser_error"
    
    def __str__(self) -> str:
        return f"{color.error_type('Parser Error:')} {super().__str__()}"


@dataclass
class MDLValidationError(MDLError):
    """Validation error during semantic analysis."""
    error_type: str = "validation_error"
    
    def __str__(self) -> str:
        return f"{color.error_type('Validation Error:')} {super().__str__()}"


@dataclass
class MDLConfigurationError(MDLError):
    """Configuration or setup error."""
    error_type: str = "configuration_error"
    
    def __str__(self) -> str:
        return f"{color.error_type('Configuration Error:')} {super().__str__()}"


@dataclass
class MDLFileError(MDLError):
    """File I/O or access error."""
    error_type: str = "file_error"
    
    def __str__(self) -> str:
        return f"{color.error_type('File Error:')} {super().__str__()}"


@dataclass
class MDLWarning(MDLError):
    """Warning message (non-fatal)."""
    error_type: str = "warning"
    
    def __str__(self) -> str:
        return f"{color.warning('Warning:')} {super().__str__()}"


class MDLErrorCollector:
    """Collects and manages multiple MDL errors."""
    
    def __init__(self):
        self.errors: List[MDLError] = []
        self.warnings: List[MDLError] = []
    
    def add_error(self, error: MDLError):
        """Add an error to the collector."""
        if isinstance(error, MDLWarning):
            self.warnings.append(error)
        else:
            self.errors.append(error)
    
    def add_warning(self, message: str, **kwargs):
        """Add a warning message."""
        warning = create_error(MDLWarning, message, **kwargs)
        self.warnings.append(warning)
    
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0
    
    def get_error_count(self) -> int:
        """Get the total number of errors."""
        return len(self.errors)
    
    def get_warning_count(self) -> int:
        """Get the total number of warnings."""
        return len(self.warnings)
    
    def clear(self):
        """Clear all errors and warnings."""
        self.errors.clear()
        self.warnings.clear()
    
    def print_errors(self, verbose: bool = True, ignore_warnings: bool = False):
        """Print all collected errors and warnings."""
        if not ignore_warnings and self.warnings:
            print(f"\n{color.warning(f'⚠️  {len(self.warnings)} Warning(s):')}")
            for warning in self.warnings:
                print(f"\n{warning}")
        
        if self.errors:
            print(f"\n{color.error(f'❌ {len(self.errors)} Error(s):')}")
            for error in self.errors:
                print(f"\n{error}")
        
        if not self.errors and not self.warnings:
            print(f"\n{color.success('✅ No errors or warnings found!')}")
    
    def raise_if_errors(self):
        """Raise an exception if there are any errors."""
        if self.has_errors():
            error_summary = f"Compilation failed with {len(self.errors)} error(s)"
            if self.warnings:
                error_summary += f" and {len(self.warnings)} warning(s)"
            
            # Create a summary error
            summary_error = create_error(
                MDLConfigurationError,
                error_summary,
                suggestion="Fix the errors above and try again."
            )
            
            # Add all errors as context
            for error in self.errors:
                summary_error.message += f"\n- {error.message}"
            
            raise summary_error


def create_error(error_class: type, message: str, file_path: Optional[str] = None, 
                line: Optional[int] = None, column: Optional[int] = None, 
                line_content: Optional[str] = None, suggestion: Optional[str] = None,
                context_lines: int = 2) -> MDLError:
    """Create an MDL error with the given information."""
    return error_class(
        message=message,
        file_path=file_path,
        line=line,
        column=column,
        line_content=line_content,
        suggestion=suggestion,
        context_lines=context_lines
    )


def format_error_context(file_path: str, line: int, column: Optional[int], context_lines: int) -> str:
    """Format error context with surrounding lines."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            return ""
        
        # Calculate line range to show
        start_line = max(0, line - context_lines - 1)
        end_line = min(len(lines), line + context_lines)
        
        context_parts = []
        for i in range(start_line, end_line):
            line_num = i + 1
            line_content = lines[i].rstrip('\n\r')
            
            if line_num == line:
                # Highlight the error line
                prefix = f"{color.line_number(f'{line_num:3d}:')} "
                content = color.error(line_content)
                context_parts.append(f"{prefix}{content}")
            else:
                # Show context lines
                prefix = f"{color.context(f'{line_num:3d}:')} "
                content = color.context(line_content)
                context_parts.append(f"{prefix}{content}")
        
        return "\n".join(context_parts)
        
    except Exception:
        return "Unable to load file context"


def create_syntax_error(message: str, file_path: Optional[str] = None, 
                       line: Optional[int] = None, column: Optional[int] = None,
                       line_content: Optional[str] = None, suggestion: Optional[str] = None) -> MDLSyntaxError:
    """Create a syntax error with common suggestions."""
    if not suggestion:
        if "missing semicolon" in message.lower():
            suggestion = "Add a semicolon (;) at the end of the statement"
        elif "missing brace" in message.lower():
            suggestion = "Add a closing brace (}) to match the opening brace"
        elif "unexpected token" in message.lower():
            suggestion = "Check for missing or extra characters in the statement"
        elif "unterminated string" in message.lower():
            suggestion = "Add a closing quote (\") to terminate the string"
    
    return MDLSyntaxError(
        message=message,
        file_path=file_path,
        line=line,
        column=column,
        line_content=line_content,
        suggestion=suggestion
    )


def create_parser_error(message: str, file_path: Optional[str] = None,
                       line: Optional[int] = None, column: Optional[int] = None,
                       line_content: Optional[str] = None, suggestion: Optional[str] = None) -> MDLParserError:
    """Create a parser error with common suggestions."""
    if not suggestion:
        if "expected" in message.lower() and "got" in message.lower():
            suggestion = "Check the syntax and ensure all required tokens are present"
        elif "unexpected end" in message.lower():
            suggestion = "Check for missing closing braces, parentheses, or quotes"
    
    return MDLParserError(
        message=message,
        file_path=file_path,
        line=line,
        column=column,
        line_content=line_content,
        suggestion=suggestion
    )


def create_validation_error(message: str, file_path: Optional[str] = None,
                           line: Optional[int] = None, column: Optional[int] = None,
                           line_content: Optional[str] = None, suggestion: Optional[str] = None) -> MDLValidationError:
    """Create a validation error with common suggestions."""
    if not suggestion:
        if "undefined variable" in message.lower():
            suggestion = "Declare the variable using 'var num variable_name = value;' before using it"
        elif "duplicate" in message.lower():
            suggestion = "Use unique names for functions, variables, and other declarations"
        elif "invalid namespace" in message.lower():
            suggestion = "Use lowercase letters, numbers, and underscores only for namespace names"
    
    return MDLValidationError(
        message=message,
        file_path=file_path,
        line=line,
        column=column,
        line_content=line_content,
        suggestion=suggestion
    )

