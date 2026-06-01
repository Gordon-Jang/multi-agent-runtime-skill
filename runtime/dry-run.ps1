$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$Root\.venv\Scripts\python.exe" "$Root\run_team.py" "review this project and propose a practical multi-agent work plan" --dry-run
