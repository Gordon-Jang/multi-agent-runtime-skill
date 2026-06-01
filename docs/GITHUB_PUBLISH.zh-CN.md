# 发布到 GitHub 指南

## 1. 创建 GitHub 仓库

在 GitHub 网页端创建新仓库，例如：

```text
multi-agent-runtime-skill
```

建议：

- Visibility: Public
- License: 不勾选，仓库里已经包含 `LICENSE`
- README: 不勾选，仓库里已经包含 `README.md`
- .gitignore: 不勾选，仓库里已经包含 `.gitignore`

## 2. 本地初始化 Git

进入发布目录：

```powershell
cd D:\path\to\multi-agent-runtime-skill-release
```

初始化：

```powershell
git init
git add .
git status
```

确认没有以下文件：

```text
.env
.venv/
__pycache__/
```

提交：

```powershell
git commit -m "Initial release of multi-agent runtime skill"
```

## 3. 关联远程仓库

把下面地址换成你的 GitHub 用户名和仓库名：

```powershell
git branch -M main
git remote add origin https://github.com/<your-username>/multi-agent-runtime-skill.git
git push -u origin main
```

如果你用 SSH：

```powershell
git remote add origin git@github.com:<your-username>/multi-agent-runtime-skill.git
git push -u origin main
```

## 4. 开源前检查

运行：

```powershell
git status --short
git grep -n "sk-" -- .
git grep -n "OPENAI_API_KEY=.*" -- .
```

如果出现真实 key，不要 push。先删除并重新提交。

## 5. 推荐仓库介绍

GitHub About 可以写：

```text
A Codex skill and portable AutoGen runtime for Codex-coordinated multi-agent workflows.
```

Topics:

```text
codex
skills
autogen
multi-agent
agent-orchestration
openai
```
