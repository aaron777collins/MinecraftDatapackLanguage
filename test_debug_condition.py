#!/usr/bin/env python3

# Test script to debug the condition conversion function
import sys
import os
sys.path.append('minecraft_datapack_language')

from cli_utils import _convert_condition_to_minecraft_syntax

# Test the condition conversion function
def test_condition_conversion():
    # Test case 1: Simple scoped variable
    condition1 = "$playerScore<@s>$ > 10"
    print(f"Test 1: {repr(condition1)}")
    result1 = _convert_condition_to_minecraft_syntax(condition1, "@s", {})
    print(f"Result 1: {result1}")
    print()
    
    # Test case 2: Global scoped variable
    condition2 = "$globalCounter<global>$ > 100"
    print(f"Test 2: {repr(condition2)}")
    result2 = _convert_condition_to_minecraft_syntax(condition2, "@s", {})
    print(f"Result 2: {result2}")
    print()
    
    # Test case 3: Team scoped variable
    condition3 = "$teamScore<@a[team=red]>$ > 50"
    print(f"Test 3: {repr(condition3)}")
    result3 = _convert_condition_to_minecraft_syntax(condition3, "@s", {})
    print(f"Result 3: {result3}")
    print()
    
    # Test case 4: Simple variable (no scope)
    condition4 = "$playerScore$ > 5"
    print(f"Test 4: {repr(condition4)}")
    result4 = _convert_condition_to_minecraft_syntax(condition4, "@s", {})
    print(f"Result 4: {result4}")
    print()

if __name__ == "__main__":
    test_condition_conversion()
