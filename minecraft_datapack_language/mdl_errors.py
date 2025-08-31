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
    
    def __str__(self) -> str:
        """Format error message with location information."""
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
        
        return "\n".join(parts)
    
    def to_dict(self) -> dict:
        """Convert error to dictionary for JSON output."""
        return {
            "type": self.error_type,
            "message": self.message,
            "file": self.file_path,
            "line": self.line,
            "column": self.column,
            "line_content": self.line_content
        }


@dataclass
class MDLSyntaxError(MDLError):
    """Syntax error in MDL code."""
    error_type: str = "syntax_error"
    
    def __str__(self) -> str:
        return f"Syntax Error: {super().__str__()}"


@dataclass
class MDLLexerError(MDLError):
    """Error during lexical analysis."""
    error_type: str = "lexer_error"
    
    def __str__(self) -> str:
        return f"Lexer Error: {super().__str__()}"


@dataclass
class MDLParserError(MDLError):
    """Error during parsing."""
    error_type: str = "parser_error"
    
    def __str__(self) -> str:
        return f"Parser Error: {super().__str__()}"


@dataclass
class MDLValidationError(MDLError):
    """Error during validation."""
    error_type: str = "validation_error"
    
    def __str__(self) -> str:
        return f"Validation Error: {super().__str__()}"


@dataclass
class MDLBuildError(MDLError):
    """Error during build process."""
    error_type: str = "build_error"
    
    def __str__(self) -> str:
        return f"Build Error: {super().__str__()}"


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
    
    def print_errors(self, verbose: bool = False) -> None:
        """Print all errors and warnings."""
        if not self.errors and not self.warnings:
            return
        
        if self.errors:
            print(f"\n❌ Found {len(self.errors)} error(s):")
            for error in self.errors:
                print(f"\n{error}")
                if verbose and hasattr(error, 'suggestion') and error.suggestion:
                    print(f"💡 Suggestion: {error.suggestion}")
        
        if self.warnings:
            print(f"\n⚠️  Found {len(self.warnings)} warning(s):")
            for warning in self.warnings:
                print(f"\n{warning}")
                if verbose and hasattr(warning, 'suggestion') and warning.suggestion:
                    print(f"💡 Suggestion: {warning.suggestion}")
    
    def raise_if_errors(self) -> None:
        """Raise an exception if there are any errors."""
        if self.has_errors():
            error_messages = [str(error) for error in self.errors]
            raise MDLBuildError(
                message=f"Build failed with {len(self.errors)} error(s):\n" + "\n".join(error_messages),
                error_type="build_error"
            )


def create_error(error_type: str, message: str, file_path: Optional[str] = None, 
                line: Optional[int] = None, column: Optional[int] = None, 
                line_content: Optional[str] = None) -> MDLError:
    """Factory function to create appropriate error type."""
    error_classes = {
        "syntax": MDLSyntaxError,
        "lexer": MDLLexerError,
        "parser": MDLParserError,
        "validation": MDLValidationError,
        "build": MDLBuildError
    }
    
    error_class = error_classes.get(error_type, MDLError)
    return error_class(
        message=message,
        file_path=file_path,
        line=line,
        column=column,
        line_content=line_content,
        error_type=error_type
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

