$repo = Split-Path $PSScriptRoot -Parent
python "$PSScriptRoot\run_verification.py" --repo $repo --project all
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$PSScriptRoot\collect_verification_results.py"
exit $LASTEXITCODE
