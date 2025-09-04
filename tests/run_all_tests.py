#!/usr/bin/env python3
"""
Comprehensive test runner for MDL.
Runs all test suites and provides detailed reporting.
Note: Avoids non-ASCII characters for Windows console compatibility.
"""

import sys
import subprocess
import time
from pathlib import Path


def run_test_suite(name, command, description=""):
    """Run a test suite and return results."""
    print(f"\n{'='*60}")
    print(f"Running {name}")
    if description:
        print(f"Description: {description}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"[PASS] {name} in {duration:.2f}s")
            if result.stdout:
                print("Output:")
                print(result.stdout)
            return True
        else:
            print(f"[FAIL] {name} in {duration:.2f}s")
            print("Error output:")
            print(result.stderr)
            if result.stdout:
                print("Standard output:")
                print(result.stdout)
            return False
            
    except Exception as e:
        duration = time.time() - start_time
        print(f"[CRASH] {name} in {duration:.2f}s")
        print(f"Exception: {e}")
        return False


def main():
    """Run all test suites."""
    print("Starting Comprehensive MDL Test Suite")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {Path.cwd()}")
    
    # Test results
    results = []
    
    # 1. Run pytest (conditionally with coverage if plugin available)
    print("\nRunning pytest...")
    # Detect pytest-cov availability
    try:
        import importlib
        has_cov = importlib.util.find_spec("pytest_cov") is not None
    except Exception:
        has_cov = False
    base_cmd = "python -m pytest tests/ -v"
    cov_args = " --cov=minecraft_datapack_language --cov-report=term-missing --cov-report=html:htmlcov" if has_cov else ""
    pytest_result = run_test_suite(
        "Pytest Suite",
        f"{base_cmd}{cov_args}",
        "Comprehensive pytest suite" + (" with coverage" if has_cov else "")
    )
    results.append(("Pytest", pytest_result))
    
    # 2. Run specific test files
    test_files = [
        ("test_comprehensive_end_to_end.py", "End-to-end comprehensive tests"),
        ("test_complex_scenarios.py", "Complex scenario tests"),
        ("test_compiler_fixes.py", "Compiler fix verification tests"),
        ("test_python_bindings.py", "Python bindings tests"),
        ("test_cli.py", "CLI functionality tests"),
    ]
    
    for test_file, description in test_files:
        test_path = Path("tests") / test_file
        if test_path.exists():
            result = run_test_suite(
                f"Direct {test_file}",
                f"python tests/{test_file}",
                description
            )
            results.append((test_file, result))
        else:
            print(f"⚠️  {test_file} not found, skipping")
    
    # 3. Run MDL compilation tests
    print("\nTesting MDL compilation...")
    
    # Test complex scenarios
    complex_result = run_test_suite(
        "Complex Scenarios Compilation",
        "python -c \"from minecraft_datapack_language.mdl_parser import MDLParser; from minecraft_datapack_language.mdl_compiler import MDLCompiler; import tempfile; from pathlib import Path; source = '''pack \\\"test\\\" \\\"Test pack\\\" 82; namespace \\\"test\\\"; var num counter<@s> = 0; var num health<@s> = 20; var num bonus<@s> = 5; function test:complex_math<@s> { counter<@s> = ($counter<@s>$ + $health<@s>$) * $bonus<@s>$; }'''; parser = MDLParser(); ast = parser.parse(source); compiler = MDLCompiler('temp_output'); compiler.compile(ast); print('Complex expressions compilation successful')\"",
        "Test complex mathematical expressions compilation"
    )
    results.append(("Complex Expressions", complex_result))
    
    # Test control flow
    control_result = run_test_suite(
        "Control Flow Compilation",
        "python -c \"from minecraft_datapack_language.mdl_parser import MDLParser; from minecraft_datapack_language.mdl_compiler import MDLCompiler; import tempfile; from pathlib import Path; source = '''pack \\\"test\\\" \\\"Test pack\\\" 82; namespace \\\"test\\\"; var num health<@s> = 20; function test:health_check<@s> { if $health<@s>$ < 10 { say \\\"Health is low!\\\"; } else { say \\\"Health is good!\\\"; } }'''; parser = MDLParser(); ast = parser.parse(source); compiler = MDLCompiler('temp_output'); compiler.compile(ast); print('Control flow compilation successful')\"",
        "Test if/else control flow compilation"
    )
    results.append(("Control Flow", control_result))
    
    # Test function execution
    function_result = run_test_suite(
        "Function Execution Compilation",
        "python -c \"from minecraft_datapack_language.mdl_parser import MDLParser; from minecraft_datapack_language.mdl_compiler import MDLCompiler; import tempfile; from pathlib import Path; source = '''pack \\\"test\\\" \\\"Test pack\\\" 82; namespace \\\"test\\\"; function test:helper<@s> { say \\\"Helper function!\\\"; } function test:main<@s> { exec test:helper<@s>; }'''; parser = MDLParser(); ast = parser.parse(source); compiler = MDLCompiler('temp_output'); compiler.compile(ast); print('Function execution compilation successful')\"",
        "Test function execution with scopes"
    )
    results.append(("Function Execution", function_result))
    
    # 4. Test Python API
    print("\nTesting Python bindings...")
    api_result = run_test_suite(
        "Python Bindings Basic",
        "python -c \"from minecraft_datapack_language import Pack; import tempfile; from pathlib import Path; p = Pack('Test', 'Test pack', 82); ns = p.namespace('test'); ns.function('hello', 'say Hello World!'); with tempfile.TemporaryDirectory() as temp_dir: p.build(temp_dir); output = Path(temp_dir) / 'data' / 'test' / 'function' / 'hello.mcfunction'; assert output.exists(); print('Python API test successful')\"",
        "Test basic Python bindings functionality"
    )
    results.append(("Python Bindings", api_result))
    
    # 5. Test CLI
    print("\nTesting CLI...")
    cli_result = run_test_suite(
        "CLI Help",
        "python -m minecraft_datapack_language.cli --help",
        "Test CLI help command"
    )
    results.append(("CLI Help", cli_result))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status} {name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! MDL is working correctly.")
        return 0
    else:
        print("Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
