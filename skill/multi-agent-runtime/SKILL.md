---
name: multi-agent-runtime
description: Diagnose, run, and manage a Codex-global AutoGen-style multi-agent runtime. Use when the user asks to check API/model configuration, run multi-agent collaboration, use agent-control-agent workflows, or create, list, assign, modify, or delete agents stored under the Codex runtime root.
---

# Multi-Agent Runtime

Use this skill for a Codex-global multi-agent runner. The runtime root is `%USERPROFILE%\.codex\multi-agent-runtime` by default. Agent definitions, API config, scripts, and dependencies live there. A target project only receives lightweight state under `.codex-multi-agent/`.

## Runtime Discovery

Default runtime path:

```powershell
$env:USERPROFILE\.codex\multi-agent-runtime
```

Do not require a project-local `multi-agent-runtime` folder. Treat the current workspace as the target project unless the user provides another `-Workspace`.

Use `scripts/runtime_tool.py find --start <workspace>` only if the global runtime is missing or the user asks to locate a runtime.

## Diagnostic Workflow

Run diagnostics before real model work when:

- The user changed `.env`, API key, base URL, or model.
- The previous run failed with connection, permission, or model errors.
- The user asks whether configuration is complete.

Steps:

1. Run `check-config.ps1` from the global runtime directory.
2. If it fails with model access, query the provider's model list if available and update `AUTOGEN_MODEL` in `.env`.
3. If it fails with connection errors, verify `OPENAI_BASE_URL` ends with `/v1` for compatible gateways and that PowerShell can reach the host.
4. Run `dry-run.ps1` to verify the runtime shape without model calls.
5. Run a short worker-only task to verify the agent chain.

Never print the full API key. Mask it in summaries.

## Running Multi-Agent Work

From any project directory, call the global runtime:

```powershell
& "$env:USERPROFILE\.codex\multi-agent-runtime\run-codex-workers.ps1" -Goal "researcher inspect context, coder propose minimal changes, reviewer check risks, tester define verification"
```

Use worker-only mode when the current Codex chat should coordinate work instead of an AutoGen `planner`.

Full internal team mode:

```powershell
& "$env:USERPROFILE\.codex\multi-agent-runtime\run-team.ps1" -Goal "review this project and propose improvements"
```

For another project:

```powershell
& "$env:USERPROFILE\.codex\multi-agent-runtime\run-codex-workers.ps1" -Goal "inspect this repo and create a test plan" -Workspace "D:\path\to\project"
```

Use concrete goals. Include expected output when useful, such as review findings, implementation plan, test plan, or documentation draft.

## Agent Management

Global team files live at:

```text
%USERPROFILE%\.codex\multi-agent-runtime\agents\<team-name>.json
```

Team JSON shape:

```json
{
  "name": "default-team",
  "description": "Portable multi-agent software team.",
  "agents": [
    {
      "name": "planner",
      "role": "Lead coordinator",
      "system_message": "..."
    }
  ]
}
```

Use `scripts/runtime_tool.py` for deterministic edits:

```powershell
python <skill-dir>\scripts\runtime_tool.py list --runtime "$env:USERPROFILE\.codex\multi-agent-runtime"
python <skill-dir>\scripts\runtime_tool.py add --runtime "$env:USERPROFILE\.codex\multi-agent-runtime" --name security-reviewer --role "Security review agent" --system-message "Review changes for security risks and data exposure."
python <skill-dir>\scripts\runtime_tool.py update --runtime "$env:USERPROFILE\.codex\multi-agent-runtime" --name tester --role "Verification agent" --system-message "Define and run practical verification steps."
python <skill-dir>\scripts\runtime_tool.py delete --runtime "$env:USERPROFILE\.codex\multi-agent-runtime" --name security-reviewer
```

When assigning work, prefer changing the goal prompt first. Modify agents only when a role should persist across future runs.

## Editing Rules

- Keep team JSON valid UTF-8 with two-space indentation.
- Do not delete agents unless the user explicitly asks.
- Do not expose secrets from `.env`.
- Prefer adding one focused agent over bloating existing prompts.
- After changing agents, run the global `check-config.ps1` and then a short worker-only task if API config is valid.

## Useful Failure Mapping

- `OPENAI_API_KEY is missing`: fill global `.env`.
- `no access to model`: change `AUTOGEN_MODEL` to a provider-supported model.
- `APIConnectionError` or `WinError 10054`: network, gateway, or proxy problem.
- `Model ... is not found` warning from AutoGen pricing: set `AUTOGEN_PRICE_PROMPT_1K=0` and `AUTOGEN_PRICE_COMPLETION_1K=0`.
- Missing `openai`: run `.venv\Scripts\python.exe -m pip install -r requirements.txt` in the global runtime directory.
