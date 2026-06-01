param(
    [Parameter(Mandatory = $true)]
    [string]$Goal,

    [string]$Workspace = (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$Root\.venv\Scripts\python.exe" "$Root\run_team.py" $Goal --workspace $Workspace
