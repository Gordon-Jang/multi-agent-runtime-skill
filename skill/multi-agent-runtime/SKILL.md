---
name: multi-agent-runtime
description: Diagnose, run, and manage a local AutoGen-style multi-agent runtime. Use when the user asks to check API/model configuration, run multi-agent collaboration, use agent-control-agent workflows, migrate the runtime to another project, or create, list, assign, modify, or delete agents in a team JSON file.
---

# Multi-Agent Runtime

Use this skill for a portable multi-agent runner deployed under a project folder such as `multi-agent-runtime/`. The runtime uses `.env`, `check-config.ps1`, `dry-run.ps1`, `run-team.ps1`, `run-codex-workers.ps1`, and team definitions under `agents/*.json`.

## Runtime Discovery

Prefer an explicit user path. If none is given, search from the current workspace for `multi-agent-runtime/run_team.py`. Users can also set `MULTI_AGENT_RUNTIME` to the runtime directory.

Use `scripts/runtime_tool.py find --start <workspace>` to locate the runtime without loading extra context.

## Diagnostic Workflow

Run diagnostics before real model work when:

- The user changed `.env`, API key, base URL, or model.
- The previous run failed with connection, permission, or model errors.
- The user asks whether configuration is complete.

Steps:

1. Run `.\check-config.ps1` from the runtime directory.
2. If it fails with model access, query the provider's model list if available and update `AUTOGEN_MODEL` in `.env`.
3. If it fails with connection errors, verify `OPENAI_BASE_URL` ends with `/v1` for compatible gateways and that PowerShell can reach the host.
4. Run `.\dry-run.ps1` to verify the runtime shape without model calls.
5. Run a short real task to verify the agent chain.

Never print the full API key. Mask it in summaries.

## Running Multi-Agent Work

Full internal team mode:

```powershell
.\run-team.ps1 -Goal "review this project and propose improvements"
```

Codex-coordinated worker mode:

```powershell
.\run-codex-workers.ps1 -Goal "researcher inspect context, coder propose minimal changes, reviewer check risks, tester define verification"
```

In worker mode, Codex should decompose the user's request in chat, call worker agents only when useful, and summarize their output back to the user. Do not tell the user to interact with the terminal unless they explicitly want to.

For another project:

```powershell
.\run-codex-workers.ps1 -Goal "inspect this repo and create a test plan" -Workspace "D:\path\to\project"
```

Use concrete goals. Include expected output when useful, such as review findings, implementation plan, test plan, or documentation draft.

## Agent Management

Team files live at `agents/<team-name>.json` and contain:

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
python <skill-dir>\scripts\runtime_tool.py list --runtime <runtime>
python <skill-dir>\scripts\runtime_tool.py add --runtime <runtime> --name security-reviewer --role "Security review agent" --system-message "Review changes for security risks and data exposure."
python <skill-dir>\scripts\runtime_tool.py update --runtime <runtime> --name tester --role "Verification agent" --system-message "Define and run practical verification steps."
python <skill-dir>\scripts\runtime_tool.py delete --runtime <runtime> --name security-reviewer
```

When assigning work, prefer changing the goal prompt first. Modify agents only when a role should persist across future runs.

## Editing Rules

- Keep team JSON valid UTF-8 with two-space indentation.
- Do not delete agents unless the user explicitly asks.
- Do not expose secrets from `.env`.
- Prefer adding one focused agent over bloating existing prompts.
- After changing agents, run `.\dry-run.ps1` and then a short real task if API config is valid.

## Useful Failure Mapping

- `OPENAI_API_KEY is missing`: fill `.env`.
- `no access to model`: change `AUTOGEN_MODEL` to a provider-supported model.
- `APIConnectionError` or `WinError 10054`: network, gateway, or proxy problem.
- `Model ... is not found` warning from AutoGen pricing: set `AUTOGEN_PRICE_PROMPT_1K=0` and `AUTOGEN_PRICE_COMPLETION_1K=0`.
- Missing `openai`: run `.venv\Scripts\python.exe -m pip install -r requirements.txt`.
