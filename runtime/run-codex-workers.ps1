param(
    [Parameter(Mandatory = $true)]
    [string]$Goal,

    [string]$Workspace = "",

    [int]$MaxRound = 6
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $Workspace) {
    $Workspace = Split-Path -Parent $Root
}
& "$Root\.venv\Scripts\python.exe" "$Root\run_team.py" $Goal --workspace $Workspace --team "$Root\agents\codex-workers.json" --max-round $MaxRound
