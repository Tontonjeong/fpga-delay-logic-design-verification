$repo = Split-Path $PSScriptRoot -Parent
python "$PSScriptRoot\run_verification.py" --repo $repo --project 3
exit $LASTEXITCODE
