# MDL (Minecraft Datapack Language) - AI Development Specification

## Development Workflow

### Testing Locally
- **Always test with Python directly**: Use `python -m minecraft_datapack_language.cli` instead of `mdl`
- **Test lexer**: `python -c "from minecraft_datapack_language.mdl_lexer_js import lex_mdl_js; tokens = lex_mdl_js('your code here'); print([t.type + ': ' + t.value for t in tokens])"`
- **Test parser**: `python -c "from minecraft_datapack_language.mdl_parser_js import parse_mdl_js; result = parse_mdl_js('your code here'); import json; print(json.dumps(result, indent=2))"`
- **Test build**: `python -m minecraft_datapack_language.cli build --mdl your_file.mdl -o output_dir`

### Release Process
1. **Commit and push changes** to git
2. **Run release script**: `bash scripts/release.sh patch`
3. **Wait 20 seconds** for PyPI to process
4. **Upgrade globally**: `pipx upgrade minecraft-datapack-language`
5. **Verify**: Test the new version works as expected

## Current Status
- **Language Design**: Complete and well-defined in `docs/_docs/language-reference.md`
- **Tokenization Spec**: Comprehensive specification for lexer/parser consistency
- **Next Step**: Implement the lexer based on the new language specification

## Development Priorities
1. **Implement Lexer**: Follow the tokenization specification exactly
2. **Test Locally**: Use Python directly, not the `mdl` command
3. **Verify Tokenization**: Ensure all language constructs generate correct tokens
4. **Update Parser**: Modify parser to work with new lexer output
5. **Test Build System**: Verify compilation works end-to-end

## Key Principles
- **Follow the spec exactly**: The language reference is the source of truth
- **Test incrementally**: Build and test each component separately
- **Use Python directly**: Avoid `mdl` command during development
- **Commit frequently**: Save progress to git regularly
