# Contributing to `haunted-shell`

First off, thank you for considering contributing to `haunted-shell`! Whether you're adding new ghost personas, improving zombie process exorcism algorithms, or fixing edge cases, all contributions are welcome.

---

## 🛠️ Development Setup

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/SWAGAT10241/haunted-shell.git
cd haunted-shell

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install in editable mode with development dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -e ".[dev]"
```

### 2. Run Tests
Ensure all unit tests pass before making changes:
```bash
pytest tests/
```

### 3. Test CLI Locally
```bash
# Test local commands
haunt airgap
haunt whisper "rm -rf junk.txt"
haunt exorcise
```

---

## 👻 Adding a New Spectral Persona

To add a new persona (e.g. `victorian-detective`, `cursed-compiler`):
1. Create a new file in `haunted_shell/personas/<your_persona>.py`.
2. Define a class implementing:
   - `name`: Short identifier string
   - `title`: Display name
   - `system_prompt`: Used when local LLM inference is active
   - `generate_commentary(cmd, exit_code, context)`: Used for offline airgap mode
3. Register your persona in `haunted_shell/personas/__init__.py`.
4. Add unit test coverage in `tests/test_haunt.py`.

---

## 📋 Pull Request Guidelines

1. **Keep it Local-First:** Any feature or integration must never violate the zero external telemetry rule. Outbound internet calls for telemetry or logging will be rejected immediately.
2. **Add Unit Tests:** Every new persona or CLI command should have test coverage.
3. **Format & Lint:** Run `flake8` and `black` before opening a PR:
   ```bash
   flake8 . --exclude=.venv
   black haunted_shell tests
   ```
4. **Descriptive Commits:** Follow conventional commits (e.g. `feat: add cursed compiler persona`, `fix: handle edge case in psutil`).

---

## 📜 Code of Conduct

Please review and adhere to our [Code of Conduct](CODE_OF_CONDUCT.md) in all interactions.
