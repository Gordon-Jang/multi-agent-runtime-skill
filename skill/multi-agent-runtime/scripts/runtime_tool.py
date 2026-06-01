import argparse
import json
import os
from pathlib import Path
from typing import Optional


def default_runtime() -> Optional[Path]:
    env_value = os.getenv("MULTI_AGENT_RUNTIME")
    if env_value:
        return Path(env_value).resolve()
    cwd = Path.cwd()
    for directory in [cwd, *cwd.parents]:
        nested = directory / "multi-agent-runtime" / "run_team.py"
        if nested.exists():
            return nested.parent.resolve()
        direct = directory / "run_team.py"
        if direct.exists() and directory.name == "multi-agent-runtime":
            return directory.resolve()
    return None


def resolve_runtime(value: Optional[str]) -> Path:
    runtime = Path(value).resolve() if value else default_runtime()
    if runtime is None:
        raise SystemExit("Runtime not found. Pass --runtime or set MULTI_AGENT_RUNTIME.")
    if not (runtime / "run_team.py").exists():
        raise SystemExit(f"Runtime not found: {runtime}")
    return runtime


def team_path(runtime: Path, team: str) -> Path:
    path = runtime / "agents" / team
    if path.suffix != ".json":
        path = path.with_suffix(".json")
    if not path.exists():
        raise SystemExit(f"Team file not found: {path}")
    return path


def load_team(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_team(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def find_runtime(start: Optional[str]) -> None:
    root = Path(start).resolve() if start else Path.cwd()
    for directory in [root, *root.parents]:
        candidate = directory / "multi-agent-runtime" / "run_team.py"
        if candidate.exists():
            print(candidate.parent)
            return
        direct = directory / "run_team.py"
        if direct.exists() and directory.name == "multi-agent-runtime":
            print(directory)
            return
    runtime = default_runtime()
    if runtime:
        print(runtime)
        return
    raise SystemExit("No multi-agent-runtime found.")


def list_agents(args: argparse.Namespace) -> None:
    runtime = resolve_runtime(args.runtime)
    path = team_path(runtime, args.team)
    data = load_team(path)
    print(f"Team: {data.get('name', path.stem)}")
    for agent in data.get("agents", []):
        print(f"- {agent.get('name')}: {agent.get('role')}")


def add_agent(args: argparse.Namespace) -> None:
    runtime = resolve_runtime(args.runtime)
    path = team_path(runtime, args.team)
    data = load_team(path)
    agents = data.setdefault("agents", [])
    if any(item.get("name") == args.name for item in agents):
        raise SystemExit(f"Agent already exists: {args.name}")
    agents.append({"name": args.name, "role": args.role, "system_message": args.system_message})
    save_team(path, data)
    print(f"Added agent {args.name} to {path}")


def update_agent(args: argparse.Namespace) -> None:
    runtime = resolve_runtime(args.runtime)
    path = team_path(runtime, args.team)
    data = load_team(path)
    for agent in data.get("agents", []):
        if agent.get("name") == args.name:
            if args.role:
                agent["role"] = args.role
            if args.system_message:
                agent["system_message"] = args.system_message
            save_team(path, data)
            print(f"Updated agent {args.name} in {path}")
            return
    raise SystemExit(f"Agent not found: {args.name}")


def delete_agent(args: argparse.Namespace) -> None:
    runtime = resolve_runtime(args.runtime)
    path = team_path(runtime, args.team)
    data = load_team(path)
    before = len(data.get("agents", []))
    data["agents"] = [agent for agent in data.get("agents", []) if agent.get("name") != args.name]
    if len(data["agents"]) == before:
        raise SystemExit(f"Agent not found: {args.name}")
    save_team(path, data)
    print(f"Deleted agent {args.name} from {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage a local multi-agent runtime.")
    sub = parser.add_subparsers(dest="command", required=True)

    find = sub.add_parser("find")
    find.add_argument("--start")
    find.set_defaults(func=lambda args: find_runtime(args.start))

    def add_common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--runtime")
        p.add_argument("--team", default="camera-team.json")

    list_p = sub.add_parser("list")
    add_common(list_p)
    list_p.set_defaults(func=list_agents)

    add_p = sub.add_parser("add")
    add_common(add_p)
    add_p.add_argument("--name", required=True)
    add_p.add_argument("--role", required=True)
    add_p.add_argument("--system-message", required=True)
    add_p.set_defaults(func=add_agent)

    update_p = sub.add_parser("update")
    add_common(update_p)
    update_p.add_argument("--name", required=True)
    update_p.add_argument("--role")
    update_p.add_argument("--system-message")
    update_p.set_defaults(func=update_agent)

    delete_p = sub.add_parser("delete")
    add_common(delete_p)
    delete_p.add_argument("--name", required=True)
    delete_p.set_defaults(func=delete_agent)

    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
