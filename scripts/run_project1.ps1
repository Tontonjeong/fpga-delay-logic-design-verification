$repo = Split-Path $PSScriptRoot -Parent
python "$PSScriptRoot\run_verification.py" --repo $repo --project 1
exit $LASTEXITCODE
