"""
MDL Syntax Linter

This module provides linting capabilities for MDL source files,
validating syntax and providing suggestions for improvement.
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class MDLLintIssue:
    """Represents a linting issue found in an MDL file"""
    line_number: int
    severity: str  # 'error', 'warning', 'info'
    category: str
    message: str
    suggestion: Optional[str] = None
    code: Optional[str] = None


class MDLLinter:
    """Linter for MDL source files with syntax validation"""
    
    def __init__(self):
        self.issues = []
    
    def lint_file(self, file_path: str) -> List[MDLLintIssue]:
        """Lint a single MDL file"""
        self.issues = []
        
        if not Path(file_path).exists():
            self.issues.append(MDLLintIssue(
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
                if not line or line.startswith('//'):
                    continue
                
                # Run all linting rules on this line
                self._check_while_loop_syntax(line, line_num)
                self._check_variable_declaration(line, line_num)
                self._check_scope_syntax(line, line_num)
                self._check_hook_syntax(line, line_num)
                self._check_pack_declaration(line, line_num)
                self._check_namespace_declaration(line, line_num)
                self._check_registry_type_declaration(line, line_num)
                self._check_tag_declaration(line, line_num)
                self._check_raw_text_syntax(line, line_num)
            
            return self.issues
            
        except Exception as e:
            self.issues.append(MDLLintIssue(
                line_number=0,
                severity='error',
                category='file',
                message=f"Error reading file: {str(e)}"
            ))
            return self.issues
    
    def _check_while_loop_syntax(self, line: str, line_num: int):
        """Check while loop syntax including method parameter"""
        # Match while loop with optional method parameter
        while_pattern = r'while\s+"([^"]+)"\s*(?:method\s*=\s*"([^"]+)")?\s*\{'
        match = re.search(while_pattern, line)
        
        if match:
            condition = match.group(1)
            method = match.group(2)
            
            # Check if method parameter is valid
            if method and method not in ['recursion', 'schedule']:
                self.issues.append(MDLLintIssue(
                    line_number=line_num,
                    severity='error',
                    category='while_loop',
                    message=f"Invalid while loop method: '{method}'",
                    suggestion="Method must be 'recursion' or 'schedule'",
                    code=line
                ))
            
            # Check condition syntax
            if not self._is_valid_condition(condition):
                self.issues.append(MDLLintIssue(
                    line_number=line_num,
                    severity='warning',
                    category='while_loop',
                    message=f"Potentially invalid condition: '{condition}'",
                    suggestion="Ensure condition uses proper variable syntax ($var$) and operators",
                    code=line
                ))
    

    
    def _check_variable_declaration(self, line: str, line_num: int):
        """Check variable declaration syntax"""
        # Match variable declaration pattern (with optional scope)
        var_pattern = r'var\s+num\s+(\w+)(?:\s+scope<([^>]+)>)?\s*=\s*([^;]+);'
        match = re.search(var_pattern, line)
        
        if match:
            var_name = match.group(1)
            scope = match.group(2)
            value = match.group(3).strip()
            
            # Check variable name
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', var_name):
                self.issues.append(MDLLintIssue(
                    line_number=line_num,
                    severity='error',
                    category='variable',
                    message=f"Invalid variable name: '{var_name}'",
                    suggestion="Variable names must start with letter or underscore and contain only letters, numbers, and underscores",
                    code=line
                ))
            
            # Check if value is numeric
            if not re.match(r'^\d+$', value):
                self.issues.append(MDLLintIssue(
                    line_number=line_num,
                    severity='warning',
                    category='variable',
                    message=f"Non-numeric value in variable declaration: '{value}'",
                    suggestion="Consider using a numeric value for initialization",
                    code=line
                ))
    
    def _check_scope_syntax(self, line: str, line_num: int):
        """Check scope syntax in variable declarations"""
        # Match scope pattern
        scope_pattern = r'scope<([^>]+)>'
        match = re.search(scope_pattern, line)
        
        if match:
            selector = match.group(1).strip()
            
            # Check for special keywords
            if selector == 'global':
                # Global is a special keyword - no validation needed
                return
            
            # Check for potentially problematic selectors
            if selector in ['@a', '@e', '@r']:
                self.issues.append(MDLLintIssue(
                    line_number=line_num,
                    severity='warning',
                    category='scope',
                    message=f"Broad selector '{selector}' may affect multiple entities",
                    suggestion="Consider using a more specific selector to avoid unintended side effects",
                    code=line
                ))
            
            # Check for valid selector syntax
            if not re.match(r'^@[spear](\[.*\])?$', selector):
                self.issues.append(MDLLintIssue(
                    line_number=line_num,
                    severity='warning',
                    category='scope',
                    message=f"Selector '{selector}' may not be valid",
                    suggestion="Use valid Minecraft selectors like @s, @p, @a, @e, @r with optional arguments, or 'global' for global variables",
                    code=line
                ))
    
    def _check_hook_syntax(self, line: str, line_num: int):
        """Check hook declaration syntax"""
        # Match hook patterns
        hook_patterns = [
            (r'on_tick\s+"([^"]+)";', 'tick'),
            (r'on_load\s+"([^"]+)";', 'load')
        ]
        
        for pattern, hook_type in hook_patterns:
            match = re.search(pattern, line)
            if match:
                function_name = match.group(1)
                
                # Check if function name includes namespace
                if ':' not in function_name:
                    self.issues.append(MDLLintIssue(
                        line_number=line_num,
                        severity='warning',
                        category='hook',
                        message=f"Function name in {hook_type} hook should include namespace",
                        suggestion=f"Use format 'namespace:function_name' instead of '{function_name}'",
                        code=line
                    ))
    
    def _check_pack_declaration(self, line: str, line_num: int):
        """Check pack declaration syntax"""
        pack_pattern = r'pack\s+"([^"]+)"\s+"([^"]+)"\s+(\d+);'
        match = re.search(pack_pattern, line)
        
        if match:
            pack_name = match.group(1)
            description = match.group(2)
            pack_format = int(match.group(3))
            
            # Check pack format
            if pack_format < 1 or pack_format > 999:
                self.issues.append(MDLLintIssue(
                    line_number=line_num,
                    severity='error',
                    category='pack',
                    message=f"Invalid pack format: {pack_format}",
                    suggestion="Pack format should be between 1 and 999",
                    code=line
                ))
    
    def _check_namespace_declaration(self, line: str, line_num: int):
        """Check namespace declaration syntax"""
        namespace_pattern = r'namespace\s+"([^"]+)";'
        match = re.search(namespace_pattern, line)
        
        if match:
            namespace = match.group(1)
            
            # Check namespace name
            if not re.match(r'^[a-z0-9_]+$', namespace):
                self.issues.append(MDLLintIssue(
                    line_number=line_num,
                    severity='warning',
                    category='namespace',
                    message=f"Namespace should use lowercase letters, numbers, and underscores only: '{namespace}'",
                    suggestion="Use lowercase letters, numbers, and underscores for namespace names",
                    code=line
                ))
    
    def _check_registry_type_declaration(self, line: str, line_num: int):
        """Check registry type declaration syntax"""
        # Match registry type patterns
        registry_patterns = [
            (r'recipe\s+"([^"]+)"\s+"([^"]+)";', 'recipe'),
            (r'loot_table\s+"([^"]+)"\s+"([^"]+)";', 'loot_table'),
            (r'advancement\s+"([^"]+)"\s+"([^"]+)";', 'advancement'),
            (r'predicate\s+"([^"]+)"\s+"([^"]+)";', 'predicate'),
            (r'item_modifier\s+"([^"]+)"\s+"([^"]+)";', 'item_modifier'),
            (r'structure\s+"([^"]+)"\s+"([^"]+)";', 'structure')
        ]
        
        for pattern, registry_type in registry_patterns:
            match = re.search(pattern, line)
            if match:
                name = match.group(1)
                file_path = match.group(2)
                
                # Check registry name
                if not re.match(r'^[a-z0-9_]+$', name):
                    self.issues.append(MDLLintIssue(
                        line_number=line_num,
                        severity='warning',
                        category='registry_type',
                        message=f"{registry_type} name should use lowercase letters, numbers, and underscores only: '{name}'",
                        suggestion="Use lowercase letters, numbers, and underscores for registry type names",
                        code=line
                    ))
                
                # Check file path
                if not file_path.endswith('.json'):
                    self.issues.append(MDLLintIssue(
                        line_number=line_num,
                        severity='error',
                        category='registry_type',
                        message=f"{registry_type} file path must end with '.json': '{file_path}'",
                        suggestion="Ensure the file path points to a JSON file",
                        code=line
                    ))
                
                # Check for relative path
                if file_path.startswith('/'):
                    self.issues.append(MDLLintIssue(
                        line_number=line_num,
                        severity='warning',
                        category='registry_type',
                        message=f"{registry_type} file path should be relative: '{file_path}'",
                        suggestion="Use relative paths instead of absolute paths",
                        code=line
                    ))
    
    def _check_tag_declaration(self, line: str, line_num: int):
        """Check tag declaration syntax"""
        # Match tag declaration pattern
        tag_pattern = r'tag\s+(function|item|block|entity_type|fluid|game_event)\s+"([^"]+)"\s*\{'
        match = re.search(tag_pattern, line)
        
        if match:
            tag_type = match.group(1)
            tag_name = match.group(2)
            
            # Check tag name format
            if ':' not in tag_name:
                self.issues.append(MDLLintIssue(
                    line_number=line_num,
                    severity='warning',
                    category='tag',
                    message=f"Tag name should include namespace: '{tag_name}'",
                    suggestion="Use format 'namespace:tag_name' for tag names",
                    code=line
                ))
            
            # Check tag type validity
            valid_tag_types = ['function', 'item', 'block', 'entity_type', 'fluid', 'game_event']
            if tag_type not in valid_tag_types:
                self.issues.append(MDLLintIssue(
                    line_number=line_num,
                    severity='error',
                    category='tag',
                    message=f"Invalid tag type: '{tag_type}'",
                    suggestion=f"Valid tag types are: {', '.join(valid_tag_types)}",
                    code=line
                ))
    
    def _check_raw_text_syntax(self, line: str, line_num: int):
        """Check raw text syntax"""
        # Check for raw text start
        if '$!raw' in line:
            # Check if there's a corresponding raw!$ in the file
            # This is a basic check - in practice, we'd need to track across lines
            pass
        
        # Check for raw text end
        if 'raw!$' in line:
            # Check if there's a corresponding $!raw before this
            # This is a basic check - in practice, we'd need to track across lines
            pass
    
    def _is_valid_condition(self, condition: str) -> bool:
        """Check if a condition string is valid"""
        # Basic validation - should contain variable references and operators
        has_variable = re.search(r'\$[a-zA-Z_][a-zA-Z0-9_]*\$', condition)
        has_operator = re.search(r'[><=!]+', condition)
        return bool(has_variable and has_operator)
    

    
    def lint_directory(self, directory_path: str) -> Dict[str, List[MDLLintIssue]]:
        """Lint all MDL files in a directory"""
        results = {}
        
        for file_path in Path(directory_path).rglob("*.mdl"):
            results[str(file_path)] = self.lint_file(str(file_path))
        
        return results


def lint_mdl_file(file_path: str) -> List[MDLLintIssue]:
    """Convenience function to lint a single MDL file"""
    linter = MDLLinter()
    return linter.lint_file(file_path)


def lint_mdl_directory(directory_path: str) -> Dict[str, List[MDLLintIssue]]:
    """Convenience function to lint all MDL files in a directory"""
    linter = MDLLinter()
    return linter.lint_directory(directory_path)
