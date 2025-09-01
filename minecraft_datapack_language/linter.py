"""
MCFunction Linter for MDL

This module provides linting capabilities for generated mcfunction files,
detecting common issues and providing suggestions for improvement.
"""

import re
import os
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LintIssue:
    """Represents a linting issue found in an mcfunction file"""
    line_number: int
    severity: str  # 'error', 'warning', 'info'
    category: str
    message: str
    suggestion: Optional[str] = None
    command: Optional[str] = None


class MCFunctionLinter:
    """Linter for mcfunction files with comprehensive rule checking"""
    
    def __init__(self):
        self.issues = []
        self.rules = {
            'redundant_operations': self._check_redundant_operations,
            'inefficient_storage': self._check_inefficient_storage,
            'unnecessary_temp_vars': self._check_unnecessary_temp_vars,
            'complex_operations': self._check_complex_operations,
            'potential_errors': self._check_potential_errors,
            'performance_issues': self._check_performance_issues,
            'style_issues': self._check_style_issues
        }
    
    def lint_file(self, file_path: str) -> List[LintIssue]:
        """Lint a single mcfunction file"""
        self.issues = []
        
        if not os.path.exists(file_path):
            self.issues.append(LintIssue(
                line_number=0,
                severity='error',
                category='file',
                message=f"File not found: {file_path}"
            ))
            return self.issues
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Run all linting rules on this line
                for rule_name, rule_func in self.rules.items():
                    rule_func(line, line_num)
            
            return self.issues
            
        except Exception as e:
            self.issues.append(LintIssue(
                line_number=0,
                severity='error',
                category='file',
                message=f"Error reading file: {str(e)}"
            ))
            return self.issues
    
    def lint_directory(self, directory_path: str) -> Dict[str, List[LintIssue]]:
        """Lint all mcfunction files in a directory"""
        results = {}
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.mcfunction'):
                    file_path = os.path.join(root, file)
                    results[file_path] = self.lint_file(file_path)
        
        return results
    
    def _check_redundant_operations(self, line: str, line_num: int):
        """Check for redundant operations"""
        # Redundant scoreboard operations
        if re.match(r'scoreboard players operation @s (\w+) = @s \1', line):
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='warning',
                category='redundant_operations',
                message="Redundant scoreboard operation: variable assigned to itself",
                suggestion="Remove this line as it has no effect",
                command=line
            ))
        
        # Redundant storage operations
        if re.match(r'data modify storage mdl:variables (\w+) set value ""', line):
            # Check if next line sets the same variable
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='info',
                category='redundant_operations',
                message="Empty string initialization may be redundant",
                suggestion="Consider removing if immediately followed by assignment",
                command=line
            ))
    
    def _check_inefficient_storage(self, line: str, line_num: int):
        """Check for inefficient storage operations"""
        # Complex temporary storage operations
        if 'execute store result storage mdl:temp' in line and 'run data get storage' in line:
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='warning',
                category='inefficient_storage',
                message="Complex temporary storage operation detected",
                suggestion="Consider using direct storage operations where possible",
                command=line
            ))
        
        # Multiple append operations that could be combined
        if 'data modify storage mdl:variables' in line and 'append value' in line:
            # This is just a note, not necessarily an issue
            pass
    
    def _check_unnecessary_temp_vars(self, line: str, line_num: int):
        """Check for unnecessary temporary variables"""
        # Temporary variables with generic names
        if re.search(r'mdl:temp \w+', line):
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='info',
                category='unnecessary_temp_vars',
                message="Temporary storage variable used",
                suggestion="Consider if this temporary variable is necessary",
                command=line
            ))
        
        # Generated temporary variables
        if re.search(r'left_\d+|right_\d+|concat_\d+', line):
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='warning',
                category='unnecessary_temp_vars',
                message="Generated temporary variable detected",
                suggestion="This may indicate complex expression that could be simplified",
                command=line
            ))
    
    def _check_complex_operations(self, line: str, line_num: int):
        """Check for overly complex operations"""
        # Multi-line operations
        if '\n' in line:
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='warning',
                category='complex_operations',
                message="Multi-line operation detected",
                suggestion="Consider breaking into separate commands for clarity",
                command=line
            ))
        
        # Complex scoreboard operations
        if line.count('scoreboard players') > 1:
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='info',
                category='complex_operations',
                message="Multiple scoreboard operations in single line",
                suggestion="Consider splitting for better readability",
                command=line
            ))
    
    def _check_potential_errors(self, line: str, line_num: int):
        """Check for potential runtime errors"""
        # Missing objective declarations
        if line.startswith('scoreboard players') and 'add' in line and 'dummy' not in line:
            # Check if this is an operation without objective declaration
            if 'operation' in line and not line.startswith('scoreboard objectives add'):
                self.issues.append(LintIssue(
                    line_number=line_num,
                    severity='error',
                    category='potential_errors',
                    message="Scoreboard operation without objective declaration",
                    suggestion="Ensure objective is declared before use",
                    command=line
                ))
        
        # Invalid JSON in tellraw
        if 'tellraw' in line and '{' in line:
            try:
                # Basic JSON validation
                json_start = line.find('{')
                json_end = line.rfind('}') + 1
                json_str = line[json_start:json_end]
                # Simple bracket matching
                if json_str.count('{') != json_str.count('}'):
                    self.issues.append(LintIssue(
                        line_number=line_num,
                        severity='error',
                        category='potential_errors',
                        message="Potential JSON syntax error in tellraw",
                        suggestion="Check JSON syntax and bracket matching",
                        command=line
                    ))
            except:
                pass
        
        # Check for common mcfunction syntax errors
        self._check_mcfunction_syntax(line, line_num)
    
    def _check_mcfunction_syntax(self, line: str, line_num: int):
        """Check for actual mcfunction syntax errors"""
        import re
        
        # Incomplete scoreboard commands
        if re.match(r'scoreboard players (add|remove|set|operation)\s*$', line):
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='error',
                category='syntax_errors',
                message="Incomplete scoreboard command - missing target and value",
                suggestion="Add target selector and value/objective",
                command=line
            ))
        
        # Invalid scoreboard operation syntax
        # Check for valid patterns: =, +=, -=, *=, /=, %=
        valid_patterns = [
            r'@\w+\s+\w+\s*=\s*@\w+\s+\w+',      # assignment: target = source
            r'@\w+\s+\w+\s*\+=\s*@\w+\s+\w+',    # addition: target += source
            r'@\w+\s+\w+\s*-=\s*@\w+\s+\w+',     # subtraction: target -= source
            r'@\w+\s+\w+\s*\*=\s*@\w+\s+\w+',    # multiplication: target *= source
            r'@\w+\s+\w+\s*/=\s*@\w+\s+\w+',     # division: target /= source
            r'@\w+\s+\w+\s*%=\s*@\w+\s+\w+'      # modulo: target %= source
        ]
        
        if 'scoreboard players operation' in line:
            is_valid = any(re.search(pattern, line) for pattern in valid_patterns)
            if not is_valid:
                self.issues.append(LintIssue(
                    line_number=line_num,
                    severity='error',
                    category='syntax_errors',
                    message="Invalid scoreboard operation syntax",
                    suggestion="Use format: scoreboard players operation <target> <objective> <operator> <source> <objective>",
                    command=line
                ))
        
        # Unclosed quotes in data commands
        if 'data modify' in line and line.count('"') % 2 != 0:
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='error',
                category='syntax_errors',
                message="Unclosed quotes in data command",
                suggestion="Check quote matching in data modify command",
                command=line
            ))
        
        # Invalid entity selectors
        if re.search(r'@[^aeprs]', line):
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='error',
                category='syntax_errors',
                message="Invalid entity selector",
                suggestion="Use valid selectors: @a, @e, @p, @r, @s",
                command=line
            ))
        
        # Invalid effect names
        if 'effect give' in line and not re.search(r'minecraft:[a-z_]+', line):
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='error',
                category='syntax_errors',
                message="Invalid effect name format",
                suggestion="Use format: minecraft:effect_name",
                command=line
            ))
        
        # Malformed execute commands
        if line.startswith('execute') and not re.search(r'run\s+\w+', line):
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='error',
                category='syntax_errors',
                message="Malformed execute command - missing 'run' clause",
                suggestion="Add 'run <command>' to execute statement",
                command=line
            ))
        
        # Invalid data storage syntax
        if 'data modify storage' in line and not re.search(r'storage\s+\w+:\w+', line):
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='error',
                category='syntax_errors',
                message="Invalid data storage syntax",
                suggestion="Use format: storage <namespace>:<path>",
                command=line
            ))
    
    def _check_performance_issues(self, line: str, line_num: int):
        """Check for performance issues"""
        # Expensive operations
        if 'execute store result' in line and 'run data get storage' in line:
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='info',
                category='performance_issues',
                message="Potentially expensive storage operation",
                suggestion="Consider if this operation is necessary or can be optimized",
                command=line
            ))
        
        # Multiple storage operations
        if line.count('data modify storage') > 1:
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='warning',
                category='performance_issues',
                message="Multiple storage operations in single line",
                suggestion="Consider combining or optimizing storage operations",
                command=line
            ))
    
    def _check_style_issues(self, line: str, line_num: int):
        """Check for style and consistency issues"""
        # Inconsistent spacing
        if re.search(r'  +', line):  # Multiple spaces
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='info',
                category='style_issues',
                message="Inconsistent spacing detected",
                suggestion="Use consistent single spaces between command parts",
                command=line
            ))
        
        # Long lines
        if len(line) > 120:
            self.issues.append(LintIssue(
                line_number=line_num,
                severity='info',
                category='style_issues',
                message="Line is very long",
                suggestion="Consider breaking into multiple lines for readability",
                command=line
            ))


def lint_mcfunction_file(file_path: str) -> List[LintIssue]:
    """Convenience function to lint a single mcfunction file"""
    linter = MCFunctionLinter()
    return linter.lint_file(file_path)


def lint_mcfunction_directory(directory_path: str) -> Dict[str, List[LintIssue]]:
    """Convenience function to lint all mcfunction files in a directory"""
    linter = MCFunctionLinter()
    return linter.lint_directory(directory_path)


def format_lint_report(issues: List[LintIssue], file_path: str = None) -> str:
    """Format lint issues into a readable report"""
    if not issues:
        return "[OK] No linting issues found!"
    
    report = []
    if file_path:
        report.append(f"[DIR] Linting Report for: {file_path}")
    else:
        report.append("[DIR] Linting Report")
    
    report.append("=" * 50)
    
    # Group by severity
    by_severity = {'error': [], 'warning': [], 'info': []}
    for issue in issues:
        by_severity[issue.severity].append(issue)
    
    for severity in ['error', 'warning', 'info']:
        if by_severity[severity]:
            icon = {'error': 'ERROR', 'warning': 'WARNING', 'info': 'INFO'}[severity]
            report.append(f"\n{icon} {severity.upper()}S ({len(by_severity[severity])})")
            report.append("-" * 30)
            
            for issue in by_severity[severity]:
                report.append(f"Line {issue.line_number}: {issue.message}")
                if issue.suggestion:
                    report.append(f"  Suggestion: {issue.suggestion}")
                if issue.command:
                    report.append(f"  Command: {issue.command[:80]}{'...' if len(issue.command) > 80 else ''}")
                report.append("")
    
    return "\n".join(report)


# Global linter instance
mcfunction_linter = MCFunctionLinter()
