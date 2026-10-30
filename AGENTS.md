# 🤖 AGENTS.md — Agentic Contributor & LLM Pair Programming Guide

> **Target Audience:** Autonomous coding agents (Antigravity, Claude Code, Cursor, Copilot Workspace, Devin) and LLM pair programmers contributing to `haunted-shell`.

Welcome, synthetic collaborator. This document establishes operational instructions, system invariants, development toolchains, and quality protocols for editing, refactoring, and extending `haunted-shell`.

---

## 🧭 Repository Identity & Mission

- **Project:** `haunted-shell` (Ghost in the Machine)
- **Competition:** Hacktoberfest 2026 Open-Source AI Challenge: Week 4
- **Mission:** A privacy-first, 100% air-gapped terminal companion that possesses user shells with eerie commentary, Dia de los Muertos *calaveritas*, Unix history lore, and safe OS zombie process exorcism.
- **AI Engine:** Local open-weight models (Google Gemma 2, Llama 3.2 via Ollama) paired with zero-dependency deterministic spectral fallback heuristics.

---

## ⚡ Core Invariants (DO NOT VIOLATE)

Whenever you generate code or make changes, you **must adhere to these 4 strict invariants**:

### 1. 🛡️ Zero Outbound Telemetry (Strict Air-Gap)
- **Rule:** Never introduce any external network calls, cloud LLM client libraries (`openai`, `anthropic`, `google-genai`), analytics endpoints, or remote error trackers.
- **Allowed Network:** Only local sockets (`localhost:11434` / `127.0.0.1` for Ollama/llama.cpp daemons).
- **Verification:** Run `haunt airgap` or `pytest tests/test_ghost.py` to ensure airgap audit passes.

### 2. 🔄 Dual-Inference Resilience
- **Rule:** Every feature that leverages LLM output must gracefully degrade to deterministic offline heuristics when Ollama is offline, unreachable, or times out.
- **Testing:** Unit tests must test **both** online mocked responses and offline fallback execution (`force_offline=True`).

### 3. 🚫 Process Safety Boundaries
- **Rule:** The `Exorcist` engine must never target or terminate:
  - PID 0, PID 1 (`init`, `systemd`, `launchd`)
  - Kernel threads
  - The current Python process PID (`os.getpid()`)
  - The parent terminal shell PID (`os.getppid()`)
  - Root processes when running unprivileged (`psutil.AccessDenied`)

### 4. 🔒 Branch Protection on `main`
- **Rule:** Direct commits or force-pushes to `main` are rejected by GitHub repository rules.
- **Workflow:** Always create a feature or fix branch (`feature/...`, `docs/...`, `fix/...`), commit, push, and open a Pull Request.

---

## 🛠️ Development Environment & Toolchain

The repository uses Python 3.9+ with modern tooling (`ruff`, `mypy`, `pytest`, `psutil`, `click`, `rich`).

### Virtual Environment Setup
```bash
# Activate existing local virtual environment
source .venv/bin/activate

# Or recreate if needed
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Essential Quality Verification Commands
Before submitting any pull request or finishing any task, run the full verification suite:

```bash
# 1. Run all 63+ unit tests
pytest tests/ -v

# 2. Run test suite with branch coverage
pytest --cov=haunted_shell --cov-report=term-missing tests/

# 3. Lint with Ruff
ruff check .

# 4. Check code formatting with Ruff
ruff format --check .

# 5. Static type check with Mypy
mypy haunted_shell/

# 6. One-stop quality check
make check
```

---

## 📂 Codebase Directory Layout

```
haunted-shell/
├── ARCHITECTURE.md             # Deep-dive system architecture specification
├── AGENTS.md                   # Agentic guidelines (this document)
├── README.md                   # User-facing project documentation & quickstart
├── pyproject.toml              # Build metadata, dependencies, tool configs
├── Makefile                    # Standard development tasks (make check, make test)
│
├── bin/
│   └── haunt                   # Executable CLI wrapper script
│
├── haunted_shell/              # Core package root
│   ├── __init__.py             # Package version & top-level exports
│   ├── cli.py                  # Click command definitions & subcommands
│   ├── ghost.py                # GhostEngine orchestrator & dual-inference router
│   ├── exorcist.py             # Safe OS process table zombie exorcism engine
│   ├── config.py               # HauntedConfig dataclass & XDG JSON persistence
│   ├── ui.py                   # Typewriter, spectral boxes, ANSI palettes
│   ├── shell_hook.py           # Bash/Zsh/Fish shell trap generator
│   ├── doctor.py               # Host environment diagnostic auditor
│   ├── logger.py               # Internal debug logging
│   │
│   ├── personas/               # Persona subsystem
│   │   ├── base.py             # BasePersona abstract base class
│   │   ├── poltergeist.py      # Poltergeist Halloween persona
│   │   ├── calavera.py         # Calavera Día de los Muertos persona
│   │   └── unix_elder.py       # 1971 Bell Labs PDP-11 hacker persona
│   │
│   └── modifiers/              # Text corruption & tone modifier subsystem
│       ├── text_modifiers.py   # Zalgo, cursed, matrix, morse, whisper, vaporwave
│       ├── tone_modifiers.py   # Eldritch, cyberpunk, sarcastic, gothic tones
│       └── custom_rules.py     # User-configurable regex rule engine
│
├── scripts/
│   └── generate_ui_preview.py  # Generates docs/assets/ui_preview.svg for PR previews
│
├── tests/                      # Pytest test suite (100% passing)
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_doctor.py
│   ├── test_exorcist.py
│   ├── test_ghost.py
│   ├── test_haunt.py
│   ├── test_hooks.py
│   ├── test_modifiers.py
│   ├── test_personas.py
│   └── test_ui.py
│
└── .github/
    └── workflows/
        ├── ci.yml              # Multi-OS (Ubuntu, macOS, Windows) matrix tests
        ├── security.yml        # CodeQL, pip-audit, Bandit SAST scanner
        ├── release.yml         # PyPI package build & release
        └── ui-preview.yml      # Automated SVG UI preview PR commenter
```

---

## 🧠 Architectural Insights (from Graphify)

The codebase has been analyzed via **Graphify** knowledge graph extraction:

- **God Nodes (Most Connected Abstractions):**
  1. [`GhostEngine`](haunted_shell/ghost.py): Central bridge connecting configuration, personas, modifiers, CLI, and Ollama.
  2. [`cli()`](haunted_shell/cli.py): Root Click dispatcher.
  3. [`HauntedConfig`](haunted_shell/config.py): Global configuration schema.
  4. [`BasePersona`](haunted_shell/personas/base.py): Base class for all spectral personalities.
  5. [`Exorcist`](haunted_shell/exorcist.py): Process scanner and zombie terminator.

- **Modularity:** 21 communities detected. Code modifies should preserve clean isolation between `personas/`, `modifiers/`, and `exorcist.py`.

---

## 🎨 Adding New Capabilities (Playbooks)

### Playbook A: Adding a New Persona
1. Inherit from `BasePersona` in `haunted_shell/personas/<new_persona>.py`.
2. Implement required properties: `name`, `color_name`, `get_system_prompt()`, and `get_offline_whisper()`.
3. Register the persona in `haunted_shell/personas/__init__.py` using `register_persona()`.
4. Add comprehensive unit tests in `tests/test_personas.py`.

### Playbook B: Adding a New Text / Tone Modifier
1. Implement the transformation function in `haunted_shell/modifiers/text_modifiers.py` or `tone_modifiers.py`.
2. Export the function in `haunted_shell/modifiers/__init__.py`.
3. Add modifier unit tests in `tests/test_modifiers.py`.

### Playbook C: Adding a New CLI Subcommand
1. Define the Click command in `haunted_shell/cli.py` attached to `cli.command()`.
2. Extract the `HauntedConfig` from `ctx.obj["config"]`.
3. Format output using utilities from `haunted_shell/ui.py` (`typewriter`, `spectral_box`).
4. Add CLI runner integration tests in `tests/test_cli.py`.

---

## 🤝 Git & PR Protocol for Agents

1. **Check status:** Ensure working tree is clean.
2. **Branch naming:** Use semantic branch prefixes:
   - `feat/<feature-name>`
   - `fix/<bug-description>`
   - `docs/<documentation-topic>`
   - `chore/<maintenance-task>`
3. **Commit messages:** Use Conventional Commits format:
   - `feat(persona): add cyberpunk hacker persona`
   - `fix(exorcist): prevent scanning permission errors on Darwin`
   - `docs(agents): update agent instructions for PR flow`
4. **CI/CD Compliance:**
   - Every PR triggers `.github/workflows/ci.yml` across Ubuntu, macOS, and Windows.
   - CodeQL, Bandit, and pip-audit run on every PR.
   - Any visual UI changes automatically generate an updated SVG screenshot preview attached to the PR.
