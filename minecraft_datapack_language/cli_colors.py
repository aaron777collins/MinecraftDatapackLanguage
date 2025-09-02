"""
CLI Color Utilities - Windows-compatible color system for MDL CLI
Provides vibrant colors without unicode characters for maximum readability
"""

import os
import sys
from typing import Optional


class Colors:
    """Color constants for CLI output - Windows compatible."""
    
    # Basic colors using ANSI escape codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"
    
    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright foreground colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    # Bright background colors
    BG_BRIGHT_BLACK = "\033[100m"
    BG_BRIGHT_RED = "\033[101m"
    BG_BRIGHT_GREEN = "\033[102m"
    BG_BRIGHT_YELLOW = "\033[103m"
    BG_BRIGHT_BLUE = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN = "\033[106m"
    BG_BRIGHT_WHITE = "\033[107m"


class ColorFormatter:
    """Formats text with colors and styling for CLI output."""
    
    def __init__(self, force_colors: bool = False):
        """Initialize color formatter.
        
        Args:
            force_colors: If True, force colors even when not supported
        """
        self.colors_enabled = self._check_color_support() or force_colors
    
    def _check_color_support(self) -> bool:
        """Check if the terminal supports colors."""
        # Check if we're on Windows
        if os.name == 'nt':
            # On Windows, check if we're in a modern terminal
            try:
                import colorama
                return True
            except ImportError:
                # Check if we're in a modern Windows terminal
                return 'TERM' in os.environ and os.environ['TERM'] != 'dumb'
        else:
            # On Unix-like systems, check if we have a TTY
            return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    
    def _format(self, text: str, *colors: str) -> str:
        """Format text with colors if enabled."""
        if not self.colors_enabled:
            return text
        
        color_codes = ''.join(colors)
        return f"{color_codes}{text}{Colors.RESET}"
    
    def header(self, text: str) -> str:
        """Format a header with bright cyan and bold."""
        return self._format(text, Colors.BRIGHT_CYAN, Colors.BOLD)
    
    def title(self, text: str) -> str:
        """Format a title with bright blue and bold."""
        return self._format(text, Colors.BRIGHT_BLUE, Colors.BOLD)
    
    def command(self, text: str) -> str:
        """Format a command with bright green."""
        return self._format(text, Colors.BRIGHT_GREEN)
    
    def option(self, text: str) -> str:
        """Format an option with bright yellow."""
        return self._format(text, Colors.BRIGHT_YELLOW)
    
    def success(self, text: str) -> str:
        """Format success message with bright green."""
        return self._format(text, Colors.BRIGHT_GREEN)
    
    def warning(self, text: str) -> str:
        """Format warning message with bright yellow."""
        return self._format(text, Colors.BRIGHT_YELLOW)
    
    def error(self, text: str) -> str:
        """Format error message with bright red."""
        return self._format(text, Colors.BRIGHT_RED)
    
    def info(self, text: str) -> str:
        """Format info message with bright cyan."""
        return self._format(text, Colors.BRIGHT_CYAN)
    
    def highlight(self, text: str) -> str:
        """Format highlighted text with bright magenta."""
        return self._format(text, Colors.BRIGHT_MAGENTA)
    
    def dim(self, text: str) -> str:
        """Format dimmed text."""
        return self._format(text, Colors.DIM)
    
    def bold(self, text: str) -> str:
        """Format bold text."""
        return self._format(text, Colors.BOLD)
    
    def underline(self, text: str) -> str:
        """Format underlined text."""
        return self._format(text, Colors.UNDERLINE)
    
    def separator(self, char: str = "=", length: int = 60) -> str:
        """Create a colored separator line."""
        separator_line = char * length
        return self._format(separator_line, Colors.BRIGHT_BLUE)
    
    def section(self, title: str, char: str = "=") -> str:
        """Create a colored section header."""
        line_length = max(60, len(title) + 4)
        left_pad = (line_length - len(title)) // 2
        right_pad = line_length - len(title) - left_pad
        
        section = f"{char * left_pad} {title} {char * right_pad}"
        return self._format(section, Colors.BRIGHT_BLUE, Colors.BOLD)
    
    def bullet(self, text: str, bullet_char: str = "•") -> str:
        """Format a bullet point."""
        return self._format(f"{bullet_char} {text}", Colors.BRIGHT_WHITE)
    
    def code(self, text: str) -> str:
        """Format code or technical text."""
        return self._format(text, Colors.BRIGHT_YELLOW, Colors.BG_BLACK)
    
    def file_path(self, text: str) -> str:
        """Format file paths."""
        return self._format(text, Colors.BRIGHT_CYAN)
    
    def line_number(self, text: str) -> str:
        """Format line numbers."""
        return self._format(text, Colors.BRIGHT_YELLOW)
    
    def column_number(self, text: str) -> str:
        """Format column numbers."""
        return self._format(text, Colors.BRIGHT_YELLOW)
    
    def error_type(self, text: str) -> str:
        """Format error type labels."""
        return self._format(text, Colors.BRIGHT_RED, Colors.BOLD)
    
    def suggestion(self, text: str) -> str:
        """Format suggestions."""
        return self._format(text, Colors.BRIGHT_GREEN, Colors.BOLD)
    
    def context(self, text: str) -> str:
        """Format context information."""
        return self._format(text, Colors.DIM)


# Global color formatter instance
color = ColorFormatter()


def print_header(text: str):
    """Print a formatted header."""
    print(color.header(text))


def print_title(text: str):
    """Print a formatted title."""
    print(color.title(text))


def print_section(title: str):
    """Print a formatted section."""
    print(color.section(title))


def print_separator(char: str = "=", length: int = 60):
    """Print a formatted separator."""
    print(color.separator(char, length))


def print_success(text: str):
    """Print a success message."""
    print(color.success(text))


def print_warning(text: str):
    """Print a warning message."""
    print(color.warning(text))


def print_error(text: str):
    """Print an error message."""
    print(color.error(text))


def print_info(text: str):
    """Print an info message."""
    print(color.info(text))


def print_bullet(text: str):
    """Print a bullet point."""
    print(color.bullet(text))


def print_code(text: str):
    """Print formatted code."""
    print(color.code(text))


def print_file_path(text: str):
    """Print a formatted file path."""
    print(color.file_path(text))


def print_error_type(text: str):
    """Print a formatted error type."""
    print(color.error_type(text))


def print_suggestion(text: str):
    """Print a formatted suggestion."""
    print(color.suggestion(text))


def print_context(text: str):
    """Print formatted context."""
    print(color.context(text))
