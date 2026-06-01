param(
    [string]$CodexHome = "$HOME\.codex",
    [string]$RuntimeTarget = ""
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillSource = Join-Path $RepoRoot "skill\multi-agent-runtime"
$SkillTarget = Join-Path $CodexHome "skills\multi-agent-runtime"

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $SkillTarget) | Out-Null
Copy-Item -Recurse -Force $SkillSource $SkillTarget
Write-Host "Installed Codex skill to: $SkillTarget"

if ($RuntimeTarget) {
    $RuntimeSource = Join-Path $RepoRoot "runtime"
    New-Item -ItemType Directory -Force -Path $RuntimeTarget | Out-Null
    Copy-Item -Recurse -Force (Join-Path $RuntimeSource "*") $RuntimeTarget
    Write-Host "Copied runtime to: $RuntimeTarget"
    Write-Host "Next: cd $RuntimeTarget; python -m venv .venv; .\.venv\Scripts\python.exe -m pip install -r requirements.txt; Copy-Item .env.example .env"
}

Write-Host "Restart Codex to pick up the new skill."
