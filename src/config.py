from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .utils import bool_from_env, project_root


@dataclass
class ProjectPaths:
    root: Path
    prompts: Path
    requirements: Path
    gold_specs: Path
    outputs: Path
    artifacts: Path


@dataclass
class RuntimeConfig:
    provider: str
    model: str
    candidates: int
    enable_repair: bool
    paths: ProjectPaths


def resolve_paths(base_dir: Path | None = None) -> ProjectPaths:
    root = base_dir or project_root()
    return ProjectPaths(
        root=root,
        prompts=root / "prompts",
        requirements=root / "data" / "requirements",
        gold_specs=root / "data" / "gold_specs",
        outputs=root / "outputs",
        artifacts=root / "artifacts",
    )


def load_runtime_config(
    base_dir: Path | None = None,
    provider: str | None = None,
    model: str | None = None,
    candidates: int | None = None,
) -> RuntimeConfig:
    paths = resolve_paths(base_dir)
    return RuntimeConfig(
        provider=(provider or os.getenv("ARG_TEST_PROVIDER", "mock")).strip(),
        model=(model or os.getenv("ARG_TEST_MODEL", "mock-arg-test")).strip(),
        candidates=candidates or int(os.getenv("ARG_TEST_CANDIDATES", "3")),
        enable_repair=bool_from_env("ARG_TEST_ENABLE_REPAIR", True),
        paths=paths,
    )
