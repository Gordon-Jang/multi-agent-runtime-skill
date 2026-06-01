# Multi-Agent Runtime Skill

English | [中文](docs/README.zh-CN.md)

This repository contains a Codex skill and a small AutoGen runtime for local multi-agent workflows.

Core idea:

```text
User
  -> Current Codex chat as planner/coordinator
  -> Worker agents in runtime:
     researcher / coder / reviewer / tester
```

It also supports a full internal AutoGen team with an internal `planner` agent.

## Contents

- A Codex skill: `skill/multi-agent-runtime`
- A portable runtime: `runtime/`
- API/model diagnostic scripts
- Worker-only mode for Codex-coordinated tasks
- Agent management: list, add, update, delete agents from team JSON files
- English and Chinese documentation

## Requirements

- Windows PowerShell
- Python 3.9+
- Codex Desktop or Codex environment with local skills support
- An OpenAI-compatible API key

## Install

Clone this repository, then run:

```powershell
.\install.ps1 -RuntimeTarget "D:\your-project\multi-agent-runtime"
```

The script installs the skill into:

```text
%USERPROFILE%\.codex\skills\multi-agent-runtime
```

It also copies the runtime into the target project.

Restart Codex after installing the skill.

## Configure Runtime

```powershell
cd D:\your-project\multi-agent-runtime
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=replace-with-your-key
OPENAI_BASE_URL=https://api.openai.com/v1
AUTOGEN_MODEL=gpt-4o-mini
AUTOGEN_TEMPERATURE=0.2
AUTOGEN_PRICE_PROMPT_1K=0
AUTOGEN_PRICE_COMPLETION_1K=0
```

Set `OPENAI_BASE_URL` and `AUTOGEN_MODEL` to values supported by your provider.

## Verify

```powershell
.\check-config.ps1
.\dry-run.ps1
```

Expected config result:

```text
Result: API check passed
Reply: OK
```

## Use From Codex

After restarting Codex:

```text
Use $multi-agent-runtime. Current Codex chat is the planner. Run worker agents to review this project and summarize findings.
```

For Chinese:

```text
使用 $multi-agent-runtime。当前 Codex 对话担任 planner，只在后台调用 researcher/coder/reviewer/tester。
```

## Direct Runtime Commands

Worker-only mode:

```powershell
.\run-codex-workers.ps1 -Goal "researcher inspect context, coder propose minimal changes, reviewer check risks, tester define verification"
```

Full internal team mode:

```powershell
.\run-team.ps1 -Goal "review this project and propose improvements"
```

Use with another project:

```powershell
.\run-codex-workers.ps1 -Goal "inspect this repo and create a test plan" -Workspace "D:\path\to\project"
```

## Agent Files

Team files are JSON:

```text
runtime/agents/camera-team.json
runtime/agents/codex-workers.json
```

Fields:

```json
{
  "name": "reviewer",
  "role": "Code review agent",
  "system_message": "Review proposed changes for bugs, regressions, security risks, and missing tests."
}
```

Replace:

- `name`: stable agent id
- `role`: short human-readable role
- `system_message`: persistent behavior instruction

## Agent Management

```powershell
python skill\multi-agent-runtime\scripts\runtime_tool.py list --runtime "D:\your-project\multi-agent-runtime"
python skill\multi-agent-runtime\scripts\runtime_tool.py add --runtime "D:\your-project\multi-agent-runtime" --name security-reviewer --role "Security review agent" --system-message "Review changes for security risks and data exposure."
python skill\multi-agent-runtime\scripts\runtime_tool.py update --runtime "D:\your-project\multi-agent-runtime" --name tester --role "Verification agent" --system-message "Define practical verification steps."
python skill\multi-agent-runtime\scripts\runtime_tool.py delete --runtime "D:\your-project\multi-agent-runtime" --name security-reviewer
```

## Security

- Never commit `.env`.
- Do not commit API keys.
- Review `system_message` fields before using third-party agent definitions.
- Keep runtime execution scoped to trusted workspaces.

## License

MIT
