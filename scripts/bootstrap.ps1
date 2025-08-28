param([string]$Python="py")
& $Python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
Write-Host "[+] Virtualenv ready. Activate with: .\.venv\Scripts\Activate.ps1"
Write-Host "[+] Try: mdl --help"
