"""Builds an Assistant from the YAML config (with optional overrides)."""
from pathlib import Path

import yaml

from assistant.agent import Assistant
from assistant.llm import get_llm
from assistant.retriever import Retriever

ROOT = Path(__file__).resolve().parent.parent


def deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for key, value in override.items():
        out[key] = deep_merge(out[key], value) if isinstance(value, dict) and isinstance(out.get(key), dict) else value
    return out


def build_assistant(overrides: dict | None = None) -> Assistant:
    settings = yaml.safe_load((ROOT / "config" / "settings.yaml").read_text())
    tools = yaml.safe_load((ROOT / "config" / "tools.yaml").read_text())["tools"]
    settings = deep_merge(settings, overrides or {})
    retriever = Retriever(settings["kb_dirs"], settings["chunk_size_words"], settings["chunk_overlap_words"], ROOT)
    return Assistant(settings, tools, retriever, get_llm(settings))
