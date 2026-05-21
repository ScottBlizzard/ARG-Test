from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .utils import bool_from_env, load_dotenv_file, project_root


@dataclass
class ProjectPaths:
    root: Path
    runtime_root: Path
    prompts: Path
    requirements: Path
    gold_specs: Path
    outputs: Path
    artifacts: Path
    env_file: Path


@dataclass
class RuntimeConfig:
    provider: str
    model: str
    candidates: int
    enable_repair: bool
    paths: ProjectPaths


def resolve_runtime_root(root: Path, output_root: str | None = None) -> Path:
    raw_output_root = (output_root or os.getenv('ARG_TEST_OUTPUT_ROOT', '')).strip()
    if not raw_output_root:
        return root
    candidate = Path(raw_output_root)
    if not candidate.is_absolute():
        candidate = root / candidate
    return candidate


def resolve_paths(base_dir: Path | None = None, output_root: str | None = None) -> ProjectPaths:
    root = (base_dir or project_root()).resolve()
    env_file = root / '.env'
    load_dotenv_file(env_file)
    runtime_root = resolve_runtime_root(root, output_root)
    return ProjectPaths(
        root=root,
        runtime_root=runtime_root,
        prompts=root / 'prompts',
        requirements=root / 'data' / 'requirements',
        gold_specs=root / 'data' / 'gold_specs',
        outputs=runtime_root / 'outputs',
        artifacts=runtime_root / 'artifacts',
        env_file=env_file,
    )


def load_runtime_config(
    base_dir: Path | None = None,
    provider: str | None = None,
    model: str | None = None,
    candidates: int | None = None,
    output_root: str | None = None,
) -> RuntimeConfig:
    paths = resolve_paths(base_dir=base_dir, output_root=output_root)
    return RuntimeConfig(
        provider=(provider or os.getenv('ARG_TEST_PROVIDER', 'mock')).strip(),
        model=(model or os.getenv('ARG_TEST_MODEL', 'mock-arg-test')).strip(),
        candidates=candidates or int(os.getenv('ARG_TEST_CANDIDATES', '3')),
        enable_repair=bool_from_env('ARG_TEST_ENABLE_REPAIR', True),
        paths=paths,
    )
