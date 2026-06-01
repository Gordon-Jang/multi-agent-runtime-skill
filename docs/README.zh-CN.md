# Multi-Agent Runtime Skill 中文说明

[English](../README.md) | 中文

本仓库包含一个 Codex skill 和一个轻量 AutoGen 运行时，用于本地多 agent 工作流。

核心结构：

```text
用户
  -> 当前 Codex 对话担任 planner / coordinator
  -> 后台 worker agents:
     researcher / coder / reviewer / tester
```

同时也保留完整 AutoGen 团队模式，即运行时内部也包含 `planner` agent。

## 内容

- Codex skill：`skill/multi-agent-runtime`
- 可复制到任意项目的运行时：`runtime/`
- API key / base URL / 模型名诊断
- 当前 Codex 对话担任 planner，后台只调用 worker agents
- agent 管理：查看、新增、修改、删除 team JSON 中的 agent
- 中英文文档

## 环境要求

- Windows PowerShell
- Python 3.9+
- 支持本地 skills 的 Codex Desktop / Codex 环境
- OpenAI 兼容 API key

## 安装

克隆仓库后运行：

```powershell
.\install.ps1 -RuntimeTarget "D:\你的项目\multi-agent-runtime"
```

脚本会把 skill 安装到：

```text
%USERPROFILE%\.codex\skills\multi-agent-runtime
```

同时把 runtime 复制到指定项目目录。

安装后重启 Codex。

## 配置运行时

```powershell
cd D:\你的项目\multi-agent-runtime
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

编辑 `.env`：

```env
OPENAI_API_KEY=替换成你的key
OPENAI_BASE_URL=https://api.openai.com/v1
AUTOGEN_MODEL=gpt-4o-mini
AUTOGEN_TEMPERATURE=0.2
AUTOGEN_PRICE_PROMPT_1K=0
AUTOGEN_PRICE_COMPLETION_1K=0
```

可替换项：

- `OPENAI_API_KEY`：你的 API key，必填，不要提交到 GitHub
- `OPENAI_BASE_URL`：官方 OpenAI 或兼容中转地址，通常以 `/v1` 结尾
- `AUTOGEN_MODEL`：你的服务商支持的模型名
- `AUTOGEN_TEMPERATURE`：建议代码任务使用 `0.2`
- `AUTOGEN_PRICE_*`：中转模型不在 AutoGen 价格表时可设为 `0`

## 验证

```powershell
.\check-config.ps1
.\dry-run.ps1
```

预期结果：

```text
Result: API check passed
Reply: OK
```

## 在 Codex 中使用

重启 Codex 后，可以直接说：

```text
使用 $multi-agent-runtime。当前 Codex 对话担任 planner，只在后台调用 researcher/coder/reviewer/tester 审查当前项目。
```

或者：

```text
用 multi-agent-runtime 检查我的多 agent 配置
```

## 直接运行命令

Worker-only 模式：当前 Codex 对话负责规划，后台只运行 worker agents。

```powershell
.\run-codex-workers.ps1 -Goal "researcher 分析上下文，coder 提出最小改动，reviewer 检查风险，tester 给出验证步骤"
```

完整团队模式：AutoGen 内部也包含 `planner`。

```powershell
.\run-team.ps1 -Goal "review this project and propose improvements"
```

迁移到其他项目：

```powershell
.\run-codex-workers.ps1 -Goal "分析这个仓库并给出测试计划" -Workspace "D:\path\to\project"
```

## Agent 配置

团队文件位于：

```text
runtime/agents/default-team.json
runtime/agents/codex-workers.json
```

agent 结构：

```json
{
  "name": "reviewer",
  "role": "Code review agent",
  "system_message": "Review proposed changes for bugs, regressions, security risks, and missing tests."
}
```

可替换项：

- `name`：稳定 agent id
- `role`：简短角色名称
- `system_message`：长期行为说明

## Agent 管理

```powershell
python skill\multi-agent-runtime\scripts\runtime_tool.py list --runtime "D:\你的项目\multi-agent-runtime"
python skill\multi-agent-runtime\scripts\runtime_tool.py add --runtime "D:\你的项目\multi-agent-runtime" --name security-reviewer --role "Security review agent" --system-message "Review changes for security risks and data exposure."
python skill\multi-agent-runtime\scripts\runtime_tool.py update --runtime "D:\你的项目\multi-agent-runtime" --name tester --role "Verification agent" --system-message "Define practical verification steps."
python skill\multi-agent-runtime\scripts\runtime_tool.py delete --runtime "D:\你的项目\multi-agent-runtime" --name security-reviewer
```

## 开源前检查

- 不要提交 `.env`
- 不要提交 `.venv`
- 不要提交 API key
- 检查 README 里的示例路径是否为通用路径
- 检查 agent 的 `system_message` 是否包含个人信息或私有业务信息

## 许可证

Apache-2.0
