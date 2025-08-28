.\.venv\Scripts\Activate.ps1
mdl --help | Out-Null
Remove-Item -Recurse -Force tmp_mdl_test -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force tmp_mdl_test | Out-Null
mdl new tmp_mdl_test --name "Test Pack" --pack-format 48
mdl check tmp_mdl_test\mypack.mdl
mdl build --mdl tmp_mdl_test\mypack.mdl -o tmp_mdl_test\dist --pack-format 48
if (!(Test-Path tmp_mdl_test\dist\pack.mcmeta)) { throw "pack.mcmeta missing" }
Write-Host "[+] CLI smoke test OK"
