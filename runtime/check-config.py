import os
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent


def mask(value: str) -> str:
    if not value:
        return "<missing>"
    if len(value) <= 10:
        return "<set>"
    return f"{value[:6]}...{value[-4:]}"


def main() -> int:
    load_dotenv(ROOT / ".env")

    api_key = os.getenv("OPENAI_API_KEY", "")
    base_url = os.getenv("OPENAI_BASE_URL", "")
    model = os.getenv("AUTOGEN_MODEL", "gpt-4o-mini")

    print("Config")
    print(f"- OPENAI_API_KEY: {mask(api_key)}")
    print(f"- OPENAI_BASE_URL: {base_url or '<default OpenAI API>'}")
    print(f"- AUTOGEN_MODEL: {model}")

    if not api_key:
        print("\nResult: missing OPENAI_API_KEY")
        return 1

    try:
        from openai import OpenAI
    except ImportError:
        print("\nResult: openai package missing. Run: .\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt")
        return 1

    kwargs = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url
    client = OpenAI(**kwargs)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Reply with exactly: OK"}],
            temperature=0,
            max_tokens=8,
        )
    except Exception as exc:
        print("\nResult: API check failed")
        print(f"- {type(exc).__name__}: {exc}")
        print("\nTry:")
        print("- Confirm OPENAI_BASE_URL ends with /v1 for your gateway.")
        print("- Confirm AUTOGEN_MODEL is a model name supported by that gateway.")
        print("- If you use a local proxy, ensure PowerShell can reach it.")
        return 1

    if isinstance(response, str):
        text = response
    elif hasattr(response, "choices") and response.choices:
        choice = response.choices[0]
        message = getattr(choice, "message", None)
        text = getattr(message, "content", None) or getattr(choice, "text", None) or str(response)
    else:
        text = str(response)

    print("\nResult: API check passed")
    print(f"- Reply: {text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
