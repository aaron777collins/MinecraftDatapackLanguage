"""
Comprehensive tests for the MDL Python API.
Tests all features including variables, control flow, function calls, and more.
"""

import pytest
import tempfile
from pathlib import Path
from minecraft_datapack_language import Pack


class TestPythonAPIBasic:
    """Test basic Python API functionality."""
    
    def test_create_pack(self):
        """Test creating a basic pack."""
        p = Pack("Test Pack", "A test datapack", 82)
        assert p.name == "Test Pack"
        assert p.description == "A test datapack"
        assert p.pack_format == 82
    
    def test_create_namespace(self):
        """Test creating a namespace."""
        p = Pack("Test Pack", "A test datapack", 82)
        ns = p.namespace("test")
        assert ns.name == "test"
    
    def test_add_function(self):
        """Test adding functions to a namespace."""
        p = Pack("Test Pack", "A test datapack", 82)
        ns = p.namespace("test")
        ns.function("hello", "say Hello World!")
        
        # Build and verify
        with tempfile.TemporaryDirectory() as temp_dir:
            p.build(temp_dir)
            output_file = Path(temp_dir) / "data" / "test" / "function" / "hello.mcfunction"
            assert output_file.exists()
            content = output_file.read_text()
            assert "say Hello World!" in content
    
    def test_lifecycle_hooks(self):
        """Test lifecycle hooks (on_load, on_tick)."""
        p = Pack("Test Pack", "A test datapack", 82)
        ns = p.namespace("test")
        ns.function("init", "say Initializing...")
        ns.function("tick", "say Tick...")
        
        p.on_load("test:init")
        p.on_tick("test:tick")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            p.build(temp_dir)
            
            # Check pack.mcmeta
            pack_mcmeta = Path(temp_dir) / "pack.mcmeta"
            assert pack_mcmeta.exists()
            
            # Check function tags
            load_tag = Path(temp_dir) / "data" / "minecraft" / "tags" / "functions" / "load.json"
            tick_tag = Path(temp_dir) / "data" / "minecraft" / "tags" / "functions" / "tick.json"
            
            assert load_tag.exists()
            assert tick_tag.exists()


class TestPythonAPIVariables:
    """Test variable functionality in Python API."""
    
    def test_variable_declaration(self):
        """Test variable declarations."""
        p = Pack("Test Pack", "A test datapack", 82)
        ns = p.namespace("test")
        
        # Test with explicit scopes
        ns.function("var_test",
            "var num counter<@s> = 0",
            "var num health<@a> = 20",
            "var num global_score = 100"
        )
        
        with tempfile.TemporaryDirectory() as temp_dir:
            p.build(temp_dir)
            output_file = Path(temp_dir) / "data" / "test" / "function" / "var_test.mcfunction"
            assert output_file.exists()
            content = output_file.read_text()
            
            # Check for scoreboard objectives
            assert "scoreboard objectives add counter dummy" in content
            assert "scoreboard objectives add health dummy" in content
            assert "scoreboard objectives add global_score dummy" in content
    
    def test_variable_operations(self):
        """Test variable operations."""
        p = Pack("Test Pack", "A test datapack", 82)
        ns = p.namespace("test")
        
        ns.function("ops_test",
            "var num counter<@s> = 0",
            "counter<@s> = 10",
            "counter<@s> = $counter<@s>$ + 5",
            "counter<@s> = $counter<@s>$ - 2",
            "counter<@s> = $counter<@s>$ * 3",
            "counter<@s> = $counter<@s>$ / 2"
        )
        
        with tempfile.TemporaryDirectory() as temp_dir:
            p.build(temp_dir)
            output_file = Path(temp_dir) / "data" / "test" / "function" / "ops_test.mcfunction"
            assert output_file.exists()
            content = output_file.read_text()
            
            # Check for scoreboard operations
            assert "scoreboard players set @s counter 10" in content
            assert "scoreboard players add @s counter 5" in content
            assert "scoreboard players remove @s counter 2" in content


class TestPythonAPIControlFlow:
    """Test control flow functionality in Python API."""
    
    def test_if_statements(self):
        """Test if statements."""
        p = Pack("Test Pack", "A test datapack", 82)
        ns = p.namespace("test")
        
        ns.function("if_test",
            "var num health<@s> = 20",
            "if $health<@s>$ < 10 {",
            "    say Health is low!",
            "    effect give @s minecraft:regeneration 10 1",
            "} else if $health<@s>$ < 15 {",
            "    say Health is medium",
            "    effect give @s minecraft:speed 5 1",
            "} else {",
            "    say Health is good",
            "}"
        )
        
        with tempfile.TemporaryDirectory() as temp_dir:
            p.build(temp_dir)
            output_file = Path(temp_dir) / "data" / "test" / "function" / "if_test.mcfunction"
            assert output_file.exists()
            content = output_file.read_text()
            
            # Check for execute if commands
            assert "execute if score" in content
            assert "execute unless score" in content
    
    def test_while_loops(self):
        """Test while loops."""
        p = Pack("Test Pack", "A test datapack", 82)
        ns = p.namespace("test")
        
        ns.function("while_test",
            "var num counter<@s> = 5",
            "while $counter<@s>$ > 0 {",
            "    say Countdown: $counter<@s>$",
            "    counter<@s> = $counter<@s>$ - 1",
            "}",
            "say Blast off!"
        )
        
        with tempfile.TemporaryDirectory() as temp_dir:
            p.build(temp_dir)
            output_file = Path(temp_dir) / "data" / "test" / "function" / "while_test.mcfunction"
            assert output_file.exists()
            content = output_file.read_text()
            
            # Check for while loop function calls
            assert "function test:while_" in content


class TestPythonAPIFunctionCalls:
    """Test function call functionality in Python API."""
    
    def test_function_calls(self):
        """Test function calls."""
        p = Pack("Test Pack", "A test datapack", 82)
        ns = p.namespace("test")
        
        # Helper functions
        ns.function("helper1", "say Helper 1!")
        ns.function("helper2", "say Helper 2!")
        
        # Main function with calls
        ns.function("main",
            "say Starting...",
            "exec test:helper1",
            "exec test:helper2<@s>",
            "exec test:helper1<@a>"
        )
        
        with tempfile.TemporaryDirectory() as temp_dir:
            p.build(temp_dir)
            output_file = Path(temp_dir) / "data" / "test" / "function" / "main.mcfunction"
            assert output_file.exists()
            content = output_file.read_text()
            
            # Check for function calls
            assert "function test:helper1" in content
            assert "execute as @s run function test:helper2" in content
            assert "execute as @a run function test:helper1" in content


class TestPythonAPITags:
    """Test tag functionality in Python API."""
    
    def test_function_tags(self):
        """Test function tags."""
        p = Pack("Test Pack", "A test datapack", 82)
        ns = p.namespace("test")
        
        ns.function("init", "say Initializing...")
        ns.function("tick", "say Tick...")
        
        # Create tags
        p.tag("function", "minecraft:load", values=["test:init"])
        p.tag("function", "minecraft:tick", values=["test:tick"])
        
        with tempfile.TemporaryDirectory() as temp_dir:
            p.build(temp_dir)
            
            # Check function tags
            load_tag = Path(temp_dir) / "data" / "minecraft" / "tags" / "functions" / "load.json"
            tick_tag = Path(temp_dir) / "data" / "minecraft" / "tags" / "functions" / "tick.json"
            
            assert load_tag.exists()
            assert tick_tag.exists()
            
            # Check tag content
            import json
            load_content = json.loads(load_tag.read_text())
            tick_content = json.loads(tick_tag.read_text())
            
            assert "test:init" in load_content["values"]
            assert "test:tick" in tick_content["values"]
    
    def test_item_tags(self):
        """Test item tags."""
        p = Pack("Test Pack", "A test datapack", 82)
        
        p.tag("item", "test:swords", values=[
            "minecraft:diamond_sword",
            "minecraft:netherite_sword"
        ])
        
        with tempfile.TemporaryDirectory() as temp_dir:
            p.build(temp_dir)
            
            item_tag = Path(temp_dir) / "data" / "test" / "tags" / "items" / "swords.json"
            assert item_tag.exists()
            
            import json
            content = json.loads(item_tag.read_text())
            assert "minecraft:diamond_sword" in content["values"]
            assert "minecraft:netherite_sword" in content["values"]


class TestPythonAPIMultiNamespace:
    """Test multi-namespace functionality in Python API."""
    
    def test_cross_namespace_calls(self):
        """Test calls between namespaces."""
        p = Pack("Test Pack", "A test datapack", 82)
        
        # Core namespace
        core = p.namespace("core")
        core.function("init", "say Core initialized")
        core.function("tick", "say Core tick")
        
        # Feature namespace
        feature = p.namespace("feature")
        feature.function("start",
            "say Feature starting...",
            "function core:init"
        )
        feature.function("update",
            "function core:tick"
        )
        
        with tempfile.TemporaryDirectory() as temp_dir:
            p.build(temp_dir)
            
            # Check feature functions
            start_file = Path(temp_dir) / "data" / "feature" / "function" / "start.mcfunction"
            update_file = Path(temp_dir) / "data" / "feature" / "function" / "update.mcfunction"
            
            assert start_file.exists()
            assert update_file.exists()
            
            start_content = start_file.read_text()
            update_content = update_file.read_text()
            
            assert "function core:init" in start_content
            assert "function core:tick" in update_content


class TestPythonAPIBuildOptions:
    """Test build options in Python API."""
    
    def test_build_with_wrapper(self):
        """Test building with custom wrapper."""
        p = Pack("Test Pack", "A test datapack", 82)
        ns = p.namespace("test")
        ns.function("hello", "say Hello World!")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            p.build(temp_dir, wrapper="my_wrapper")
            
            # Check wrapper directory
            wrapper_dir = Path(temp_dir) / "my_wrapper"
            assert wrapper_dir.exists()
            
            # Check pack.mcmeta in wrapper
            pack_mcmeta = wrapper_dir / "pack.mcmeta"
            assert pack_mcmeta.exists()
    
    def test_build_output_structure(self):
        """Test build output structure."""
        p = Pack("Test Pack", "A test datapack", 82)
        ns = p.namespace("test")
        ns.function("hello", "say Hello World!")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            p.build(temp_dir)
            
            # Check required files
            pack_mcmeta = Path(temp_dir) / "pack.mcmeta"
            data_dir = Path(temp_dir) / "data"
            test_dir = data_dir / "test"
            function_dir = test_dir / "function"
            hello_file = function_dir / "hello.mcfunction"
            
            assert pack_mcmeta.exists()
            assert data_dir.exists()
            assert test_dir.exists()
            assert function_dir.exists()
            assert hello_file.exists()


class TestPythonAPIComplexScenarios:
    """Test complex scenarios in Python API."""
    
    def test_complex_math_expressions(self):
        """Test complex mathematical expressions."""
        p = Pack("Test Pack", "A test datapack", 82)
        ns = p.namespace("test")
        
        ns.function("complex_math",
            "var num a<@s> = 10",
            "var num b<@s> = 5",
            "var num c<@s> = 2",
            "a<@s> = ($a<@s>$ + $b<@s>$) * $c<@s>$",
            "b<@s> = ($a<@s>$ - $b<@s>$) / $c<@s>$"
        )
        
        with tempfile.TemporaryDirectory() as temp_dir:
            p.build(temp_dir)
            output_file = Path(temp_dir) / "data" / "test" / "function" / "complex_math.mcfunction"
            assert output_file.exists()
            content = output_file.read_text()
            
            # Check for temporary variables
            assert "scoreboard players set @s temp_" in content
    
    def test_nested_control_flow(self):
        """Test nested control flow."""
        p = Pack("Test Pack", "A test datapack", 82)
        ns = p.namespace("test")
        
        ns.function("nested_control",
            "var num level<@s> = 5",
            "var num health<@s> = 20",
            "if $level<@s>$ > 10 {",
            "    if $health<@s>$ > 15 {",
            "        say High level and health!",
            "        effect give @s minecraft:strength 10 1",
            "    } else {",
            "        say High level, low health",
            "        effect give @s minecraft:regeneration 10 1",
            "    }",
            "} else {",
            "    say Low level",
            "}"
        )
        
        with tempfile.TemporaryDirectory() as temp_dir:
            p.build(temp_dir)
            output_file = Path(temp_dir) / "data" / "test" / "function" / "nested_control.mcfunction"
            assert output_file.exists()
            content = output_file.read_text()
            
            # Check for nested control flow
            assert "execute if score" in content
            assert "execute unless score" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
