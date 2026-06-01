# 配置参考

## 运行时环境

安装后，从 `%USERPROFILE%\.codex\multi-agent-runtime\.env.example` 创建 `%USERPROFILE%\.codex\multi-agent-runtime\.env`。

不要提交 `.env`。

## 必填项

```env
OPENAI_API_KEY=
```

你的服务商 API key。

## 可选项

```env
OPENAI_BASE_URL=https://api.openai.com/v1
```

使用 OpenAI 兼容中转或代理时填写。

```env
AUTOGEN_MODEL=gpt-4o-mini
```

替换成你的服务商支持的模型名。

```env
AUTOGEN_TEMPERATURE=0.2
```

工程任务建议使用较低温度。

```env
AUTOGEN_PRICE_PROMPT_1K=0
AUTOGEN_PRICE_COMPLETION_1K=0
```

中转模型不在 AutoGen 本地价格表时，可以设为 `0`。

## Skill 如何定位 Runtime

顺序：

1. 显式传入 `--runtime <path>`
2. 环境变量 `MULTI_AGENT_RUNTIME`
3. `%USERPROFILE%\.codex\multi-agent-runtime`
4. 当前 workspace 或父目录下的 `multi-agent-runtime/run_team.py`

PowerShell 示例：

```powershell
$env:MULTI_AGENT_RUNTIME="$env:USERPROFILE\.codex\multi-agent-runtime"
```
