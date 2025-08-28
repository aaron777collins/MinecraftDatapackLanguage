.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install build
python -m build
Write-Host "[+] Built distributions in .\dist"
Get-ChildItem dist
