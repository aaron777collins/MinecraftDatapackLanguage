"""
MDL Error Classes - Custom error types with detailed location information
"""

from dataclasses import dataclass
from typing import Optional, List, Any
import os


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
        try:
            from .cli_colors import color
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
        except ImportError:
            # Fallback if colors aren't available
            parts = []
            
            if self.file_path:
                # Show relative path if possible
                try:
                    rel_path = os.path.relpath(self.file_path)
                    parts.append(f"File: {rel_path}")
                except ValueError:
                    parts.append(f"File: {self.file_path}")
            
            if self.line is not None:
                parts.append(f"Line: {self.line}")
                if self.column is not None:
                    parts.append(f"Column: {self.column}")
            
            if self.line_content:
                parts.append(f"Code: {self.line_content.strip()}")
                if self.column is not None:
                    # Add a caret to show the exact position
                    indent = " " * (self.column - 1)
                    parts.append(f"      {indent}^")
            
            parts.append(f"Error: {self.message}")
            
            if self.suggestion:
                parts.append(f"Suggestion: {self.suggestion}")
            
            # Add context if we have file and line information
            if self.file_path and self.line is not None:
                context = format_error_context(self.file_path, self.line, self.column, self.context_lines)
                if context:
                    parts.append(f"\nContext:\n{context}")
            
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
        try:
            from .cli_colors import color
            return f"{color.error_type('Syntax Error:')} {super().__str__()}"
        except ImportError:
            return f"Syntax Error: {super().__str__()}"


@dataclass
class MDLLexerError(MDLError):
    """Error during lexical analysis."""
    error_type: str = "lexer_error"
    
    def __str__(self) -> str:
        try:
            from .cli_colors import color
            return f"{color.error_type('Lexer Error:')} {super().__str__()}"
        except ImportError:
            return f"Lexer Error: {super().__str__()}"


@dataclass
class MDLParserError(MDLError):
    """Error during parsing."""
    error_type: str = "parser_error"
    
    def __str__(self) -> str:
        try:
            from .cli_colors import color
            return f"{color.error_type('Parser Error:')} {super().__str__()}"
        except ImportError:
            return f"Parser Error: {super().__str__()}"


@dataclass
class MDLValidationError(MDLError):
    """Error during validation."""
    error_type: str = "validation_error"
    
    def __str__(self) -> str:
        try:
            from .cli_colors import color
            return f"{color.error_type('Validation Error:')} {super().__str__()}"
        except ImportError:
            return f"Validation Error: {super().__str__()}"


@dataclass
class MDLBuildError(MDLError):
    """Error during build process."""
    error_type: str = "build_error"
    
    def __str__(self) -> str:
        try:
            from .cli_colors import color
            return f"{color.error_type('Build Error:')} {super().__str__()}"
        except ImportError:
            return f"Build Error: {super().__str__()}"


@dataclass
class MDLCompilationError(MDLError):
    """Error during compilation."""
    error_type: str = "compilation_error"
    
    def __str__(self) -> str:
        try:
            from .cli_colors import color
            return f"{color.error_type('Compilation Error:')} {super().__str__()}"
        except ImportError:
            return f"Compilation Error: {super().__str__()}"


@dataclass
class MDLCompilerError(MDLError):
    """Error during compilation process."""
    error_type: str = "compiler_error"
    
    def __str__(self) -> str:
        try:
            from .cli_colors import color
            return f"{color.error_type('Compiler Error:')} {super().__str__()}"
        except ImportError:
            return f"Compiler Error: {super().__str__()}"


@dataclass
class MDLFileError(MDLError):
    """Error related to file operations."""
    error_type: str = "file_error"
    
    def __str__(self) -> str:
        try:
            from .cli_colors import color
            return f"{color.error_type('File Error:')} {super().__str__()}"
        except ImportError:
            return f"File Error: {super().__str__()}"


@dataclass
class MDLConfigurationError(MDLError):
    """Error related to configuration."""
    error_type: str = "configuration_error"
    
    def __str__(self) -> str:
        try:
            from .cli_colors import color
            return f"{color.error_type('Configuration Error:')} {super().__str__()}"
        except ImportError:
            return f"Configuration Error: {super().__str__()}"


class MDLErrorCollector:
    """Collects and manages multiple MDL errors."""
    
    def __init__(self):
        self.errors: List[MDLError] = []
        self.warnings: List[MDLError] = []
    
    def add_error(self, error: MDLError) -> None:
        """Add an error to the collection."""
        self.errors.append(error)
    
    def add_warning(self, warning: MDLError) -> None:
        """Add a warning to the collection."""
        self.warnings.append(warning)
    
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0
    
    def get_all_issues(self) -> List[MDLError]:
        """Get all errors and warnings."""
        return self.errors + self.warnings
    
    def print_errors(self, verbose: bool = False, ignore_warnings: bool = False) -> None:
        """Print all errors and warnings."""
        if not self.errors and not self.warnings:
            return
        
        try:
            from .cli_colors import color
            if self.errors:
                print(f"\n{color.error_type('ERROR:')} Found {color.error(str(len(self.errors)))} error(s):")
                for i, error in enumerate(self.errors, 1):
                    print(f"\n{color.highlight(str(i))}. {error}")
            
            if self.warnings and not ignore_warnings:
                print(f"\n{color.warning('WARNING:')} Found {color.warning(str(len(self.warnings)))} warning(s):")
                for i, warning in enumerate(self.warnings, 1):
                    print(f"\n{color.highlight(str(i))}. {warning}")
        except ImportError:
            # Fallback if colors aren't available
            if self.errors:
                print(f"\nERROR: Found {len(self.errors)} error(s):")
                for i, error in enumerate(self.errors, 1):
                    print(f"\n{i}. {error}")
            
            if self.warnings and not ignore_warnings:
                print(f"\nWARNING: Found {len(self.warnings)} warning(s):")
                for i, warning in enumerate(self.warnings, 1):
                    print(f"\n{i}. {warning}")
    
    def raise_if_errors(self) -> None:
        """Raise an exception if there are any errors."""
        if self.has_errors():
            error_messages = [str(error) for error in self.errors]
            raise MDLBuildError(
                message=f"Build failed with {len(self.errors)} error(s):\n" + "\n".join(error_messages),
                error_type="build_error"
            )
    
    def get_summary(self) -> str:
        """Get a summary of errors and warnings."""
        summary_parts = []
        
        if self.errors:
            summary_parts.append(f"{len(self.errors)} error(s)")
        
        if self.warnings:
            summary_parts.append(f"{len(self.warnings)} warning(s)")
        
        if not summary_parts:
            return "No issues found"
        
        return ", ".join(summary_parts)


def create_error(error_type: str, message: str, file_path: Optional[str] = None, 
                line: Optional[int] = None, column: Optional[int] = None, 
                line_content: Optional[str] = None, suggestion: Optional[str] = None) -> MDLError:
    """Factory function to create appropriate error type."""
    error_classes = {
        "syntax": MDLSyntaxError,
        "lexer": MDLLexerError,
        "parser": MDLParserError,
        "validation": MDLValidationError,
        "build": MDLBuildError,
        "compilation": MDLCompilationError,
        "compiler": MDLCompilerError,
        "file": MDLFileError,
        "configuration": MDLConfigurationError
    }
    
    error_class = error_classes.get(error_type, MDLError)
    return error_class(
        message=message,
        file_path=file_path,
        line=line,
        column=column,
        line_content=line_content,
        error_type=error_type,
        suggestion=suggestion
    )


def get_line_content(file_path: str, line_number: int) -> Optional[str]:
    """Get the content of a specific line from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if 1 <= line_number <= len(lines):
                return lines[line_number - 1]
    except (FileNotFoundError, UnicodeDecodeError):
        pass
    return None


def format_error_context(file_path: str, line: int, column: int, 
                        context_lines: int = 2) -> str:
    """Format error context with surrounding lines."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        start_line = max(1, line - context_lines)
        end_line = min(len(lines), line + context_lines)
        
        context = []
        for i in range(start_line, end_line + 1):
            prefix = ">>> " if i == line else "    "
            line_num = f"{i:4d}"
            content = lines[i - 1].rstrip('\n')
            context.append(f"{prefix}{line_num}: {content}")
            
            if i == line and column is not None:
                # Add caret to show exact position
                indent = " " * (column - 1)
                context.append(f"     {indent}^")
        
        return "\n".join(context)
    except (FileNotFoundError, UnicodeDecodeError):
        return f"Unable to read file: {file_path}"


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

