# Configuration Reference

## Runtime Environment

Create `%USERPROFILE%\.codex\multi-agent-runtime\.env` from `.env.example` after installation.

Do not commit `.env`.

## Required Values

```env
OPENAI_API_KEY=
```

Your provider API key.

## Optional Values

```env
OPENAI_BASE_URL=https://api.openai.com/v1
```

Use this for OpenAI-compatible gateways.

```env
AUTOGEN_MODEL=gpt-4o-mini
```

Replace with a model supported by your provider.

```env
AUTOGEN_TEMPERATURE=0.2
```

Lower values are better for deterministic engineering work.

```env
AUTOGEN_PRICE_PROMPT_1K=0
AUTOGEN_PRICE_COMPLETION_1K=0
```

Set these to `0` for gateway-specific models unknown to AutoGen's local cost table.

## Skill Runtime Discovery

The skill looks for the runtime in this order:

1. Explicit `--runtime <path>`
2. `MULTI_AGENT_RUNTIME` environment variable
3. `%USERPROFILE%\.codex\multi-agent-runtime`
4. `multi-agent-runtime/run_team.py` under the current workspace or parent directories

PowerShell example:

```powershell
$env:MULTI_AGENT_RUNTIME="$env:USERPROFILE\.codex\multi-agent-runtime"
```
