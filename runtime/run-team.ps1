param(
    [Parameter(Mandatory = $true)]
    [string]$Goal,

    [string]$Workspace = ""
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $Workspace) {
    $Workspace = (Get-Location).Path
}
& "$Root\.venv\Scripts\python.exe" "$Root\run_team.py" $Goal --workspace $Workspace
