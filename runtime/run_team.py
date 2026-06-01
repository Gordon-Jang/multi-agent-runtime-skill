import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent


def load_team(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_context(workspace: Path) -> str:
    files = []
    for candidate in ["README.md", "package.json", "pyproject.toml", "requirements.txt"]:
        target = workspace / candidate
        if target.exists():
            files.append(f"- {candidate}")
    return (
        f"Workspace: {workspace}\n"
        f"Detected context files:\n" + ("\n".join(files) if files else "- none")
    )


def dry_run(team: dict, goal: str, workspace: Path) -> None:
    print("Multi-agent runtime is deployed.")
    print(f"Team: {team['name']}")
    print(build_context(workspace))
    print("\nPlanned agent chain:")
    for agent in team["agents"]:
        print(f"- {agent['name']}: {agent['role']}")
    print("\nGoal:")
    print(goal)
    print("\nDry run only: set OPENAI_API_KEY in .env, then run without --dry-run.")


def run_autogen(team: dict, goal: str, workspace: Path, max_round: int) -> None:
    try:
        import autogen
    except ImportError as exc:
        raise SystemExit(
            "pyautogen is not installed. Run: python -m pip install -r requirements.txt"
        ) from exc

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is missing. Copy .env.example to .env and fill it.")

    model = os.getenv("AUTOGEN_MODEL", "gpt-4o-mini")
    temperature = float(os.getenv("AUTOGEN_TEMPERATURE", "0.2"))
    base_url = os.getenv("OPENAI_BASE_URL")
    model_config = {"model": model, "api_key": api_key}
    prompt_price = os.getenv("AUTOGEN_PRICE_PROMPT_1K")
    completion_price = os.getenv("AUTOGEN_PRICE_COMPLETION_1K")
    if base_url:
        model_config["base_url"] = base_url
    if prompt_price is not None and completion_price is not None:
        model_config["price"] = [float(prompt_price), float(completion_price)]
    llm_config = {
        "config_list": [model_config],
        "temperature": temperature,
    }

    agents = [
        autogen.AssistantAgent(
            name=item["name"],
            system_message=item["system_message"],
            llm_config=llm_config,
        )
        for item in team["agents"]
    ]
    user_proxy = autogen.UserProxyAgent(
        name="operator",
        human_input_mode="NEVER",
        code_execution_config=False,
        default_auto_reply="Continue. Keep the answer concise and actionable.",
    )

    groupchat = autogen.GroupChat(
        agents=[user_proxy, *agents],
        messages=[],
        max_round=max_round,
        speaker_selection_method="round_robin",
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    prompt = (
        f"{build_context(workspace)}\n\n"
        f"User goal:\n{goal}\n\n"
        "Coordinate as a portable software team. End with concrete next actions and verification."
    )
    try:
        user_proxy.initiate_chat(manager, message=prompt)
    except Exception as exc:
        print("Multi-agent run failed.")
        print(f"{type(exc).__name__}: {exc}")
        print("\nRun .\\check-config.ps1 to verify API key, base URL, and model.")
        raise SystemExit(1) from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a portable AutoGen multi-agent team.")
    parser.add_argument("goal", help="Task for the agent team.")
    parser.add_argument(
        "--workspace",
        default=str(ROOT.parent),
        help="Project path the team should reason about. Defaults to this repository.",
    )
    parser.add_argument(
        "--team",
        default=str(ROOT / "agents" / "default-team.json"),
        help="Path to a team definition JSON file.",
    )
    parser.add_argument("--max-round", type=int, default=8)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    workspace = Path(args.workspace).resolve()
    team = load_team(Path(args.team).resolve())

    if args.dry_run:
        dry_run(team, args.goal, workspace)
    else:
        run_autogen(team, args.goal, workspace, args.max_round)


if __name__ == "__main__":
    main()
