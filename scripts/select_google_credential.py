"""Probe Gemini API key/model candidates and optionally write .env.local.

Inputs, in priority order:
- .google_api_keys.local (one key per line, or GOOGLE_API_KEY=...)
- GOOGLE_API_KEYS (comma/semicolon/newline separated)
- GOOGLE_API_KEY

The script never prints full keys. Use --write-local-env to make the selected
key/model active for the lab without editing the real .env file.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"
LOCAL_ENV_FILE = PROJECT_ROOT / ".env.local"
DEFAULT_CANDIDATE_FILE = PROJECT_ROOT / ".google_api_keys.local"

DEFAULT_MODELS = [
    "gemini-flash-lite-latest",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
]


def _mask(secret: str) -> str:
    secret = secret.strip()
    if len(secret) <= 10:
        return "***"
    return f"{secret[:6]}...{secret[-4:]}"


def _split_candidates(value: str) -> list[str]:
    return [part.strip() for part in re.split(r"[,;\s]+", value) if part.strip()]


def _read_key_file(path: Path) -> list[str]:
    if not path.exists():
        return []
    keys: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            _, line = line.split("=", 1)
            line = line.strip().strip('"').strip("'")
        keys.extend(_split_candidates(line))
    return keys


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def load_key_candidates(candidate_file: Path) -> list[str]:
    load_dotenv(ENV_FILE)
    load_dotenv(LOCAL_ENV_FILE, override=True)

    candidates = _read_key_file(candidate_file)
    if os.getenv("GOOGLE_API_KEYS"):
        candidates.extend(_split_candidates(os.environ["GOOGLE_API_KEYS"]))
    if os.getenv("GOOGLE_API_KEY"):
        candidates.append(os.environ["GOOGLE_API_KEY"].strip())
    return _unique([key for key in candidates if key])


def load_model_candidates(raw_models: str | None) -> list[str]:
    models: list[str] = []
    if raw_models:
        models.extend(_split_candidates(raw_models))
    elif os.getenv("GOOGLE_MODEL_CANDIDATES"):
        models.extend(_split_candidates(os.environ["GOOGLE_MODEL_CANDIDATES"]))
    elif os.getenv("GOOGLE_MODEL"):
        models.append(os.environ["GOOGLE_MODEL"])
    models.extend(DEFAULT_MODELS)
    return _unique(models)


def probe(api_key: str, model: str) -> tuple[bool, str]:
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents="Reply with exactly: OK",
        )
        text = (response.text or "").strip()
        return True, text[:80] or "empty response"
    except Exception as exc:  # noqa: BLE001 - we want a compact probe result.
        return False, f"{type(exc).__name__}: {str(exc).splitlines()[0][:180]}"


def write_local_env(api_key: str, model: str) -> None:
    kept_lines: list[str] = []
    if LOCAL_ENV_FILE.exists():
        for line in LOCAL_ENV_FILE.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("GOOGLE_API_KEY="):
                continue
            if stripped.startswith("GOOGLE_MODEL="):
                continue
            if stripped.startswith("GOOGLE_GENAI_USE_VERTEXAI="):
                continue
            kept_lines.append(line)

    kept_lines.extend(
        [
            "GOOGLE_GENAI_USE_VERTEXAI=FALSE",
            f"GOOGLE_API_KEY={api_key}",
            f"GOOGLE_MODEL={model}",
        ]
    )
    LOCAL_ENV_FILE.write_text("\n".join(kept_lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--candidate-file",
        type=Path,
        default=DEFAULT_CANDIDATE_FILE,
        help="Local file containing candidate API keys.",
    )
    parser.add_argument(
        "--models",
        help="Comma/space separated model candidates. Defaults to GOOGLE_MODEL_CANDIDATES/GOOGLE_MODEL plus fallbacks.",
    )
    parser.add_argument(
        "--write-local-env",
        action="store_true",
        help="Write the first passing key/model to .env.local.",
    )
    args = parser.parse_args()

    keys = load_key_candidates(args.candidate_file)
    models = load_model_candidates(args.models)

    if not keys:
        print(
            "No candidate keys found. Put keys in .google_api_keys.local, "
            "GOOGLE_API_KEYS, or GOOGLE_API_KEY."
        )
        return 2

    print(f"Probing {len(keys)} key(s) x {len(models)} model(s). Full keys are hidden.")
    for key_index, api_key in enumerate(keys, start=1):
        for model in models:
            ok, detail = probe(api_key, model)
            status = "OK" if ok else "FAIL"
            print(f"[{status}] key#{key_index} {_mask(api_key)} model={model}: {detail}")
            if ok:
                if args.write_local_env:
                    write_local_env(api_key, model)
                    print(f"Wrote selected credential to {LOCAL_ENV_FILE}")
                return 0

    print("No working key/model pair found.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
