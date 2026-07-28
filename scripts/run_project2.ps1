$repo = Split-Path $PSScriptRoot -Parent
python "$PSScriptRoot\run_verification.py" --repo $repo --project 2
exit $LASTEXITCODE
