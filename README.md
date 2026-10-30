# 👻 haunted-shell: Ghost in the Machine

[![CI](https://github.com/SWAGAT10241/haunted-shell/actions/workflows/ci.yml/badge.svg)](https://github.com/SWAGAT10241/haunted-shell/actions/workflows/ci.yml)
[![Security Audit](https://github.com/SWAGAT10241/haunted-shell/actions/workflows/security.yml/badge.svg)](https://github.com/SWAGAT10241/haunted-shell/actions/workflows/security.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Air-Gap Verified](https://img.shields.io/badge/Air--Gap-100%25%20Local-brightgreen.svg)](SECURITY.md)
[![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest-2026-orange.svg)](https://dev.to/challenges/hf26)

```
      .-.
     (o o) boo!
     | O \
      \   \      G H O S T   I N   T H E   M A C H I N E
       `~~~'     [ Possessed by local open-weight AI. Air-gap verified. ]
```

> **Hacktoberfest Open-Source AI Challenge: Week 4**  
> **Theme:** Ghost in the Machine  
> *Build something spooky, or something that honors the past in the spirit of Día de los Muertos, with open-weight models or open-source AI.*

---

## 🌒 What is `haunted-shell`?

`haunted-shell` is an open-source, privacy-first, production-grade terminal companion that **possesses your shell**. Whenever you execute commands (`git push`, `rm -rf`, `kill -9`, `cat`, `whoami`), an eerie spirit materializes in your terminal to whisper chilling commentary, compose Día de los Muertos *calaveritas literarias*, roast modern software bloat, and track down real zombie processes lurking in your OS process table.

Built with **open-source AI at its core**, `haunted-shell` connects directly to local open-weight models (such as **Google Gemma 2**, Llama 3.2, or Mistral via Ollama/llama.cpp) and includes a zero-dependency offline spectral engine that runs 100% locally with zero cloud telemetry.

---

## 📖 Official Documentation & Wiki
Explore the full [haunted-shell Technical Wiki](docs/wiki/Home.md):
- [Architecture & Design](docs/wiki/Architecture-&-Design.md)
- [Personas & Lore](docs/wiki/Personas-&-Lore.md)
- [Custom Modifiers Guide](docs/wiki/Custom-Modifiers-Guide.md)
- [Exorcism & Process Monitoring](docs/wiki/Exorcism-&-Process-Monitoring.md)
- [Shell Integration & Hooks](docs/wiki/Shell-Integration-&-Hooks.md)
- [Local Open-Weight Models Setup](docs/wiki/Local-Open-Weight-Models-Setup.md)

---

## 💡 Why Open Innovation Matters for `haunted-shell`

The challenge asks: *Why does open innovation matter for what you built?*

For a shell companion, **open-source and local AI is not just a feature—it is an absolute security necessity**:

1. **Air-Gapped Privacy & Secret Protection:**  
   Your terminal is where your deepest secrets live: SSH keys (`~/.ssh`), API tokens, database credentials, environment variables, and proprietary codebases. Routing shell commands or terminal outputs to a closed commercial cloud API would be an intolerable security vulnerability. Running an open-weight model locally on your laptop guarantees that **zero bytes of terminal telemetry leave your machine**.
2. **Lights-Out, Offline Autonomy:**  
   `haunted-shell` works in an airplane cabin at 35,000 feet, in an isolated server room, or during an internet blackout with the lights (and WiFi) turned off. Your terminal remains possessed without relying on remote API uptime, rate limits, or billing meters.
3. **Freedom from Cloud Deprecation & Censorship:**  
   Closed proprietary AI APIs constantly alter model behavior, apply corporate guardrails, or deprecate older models. Open-weight models (like Gemma 2) can be fine-tuned, modified, or preserved forever on your own hardware.
4. **Zero Inference Cost:**  
   Possessing thousands of daily shell keystrokes through a closed paid API would rack up costly token bills. Local open-weight inference costs exactly \$0.00.

---

## 🔮 Three Spectral Personas

You can summon different spirits to possess your shell using `--persona` or on-the-fly in the REPL:

| Persona | Theme | Description |
|---|---|---|
| **`poltergeist`** | 🎃 Halloween | Sarcastic, chilling Halloween ghost. Delights in deleted inodes, laughs at failed commands (`exit code != 0`), and warns of dark forces in ring 0. |
| **`calavera`** | 🌼 Día de los Muertos | Celebrates the beauty of transience in the spirit of Día de los Muertos. Lays marigold (*cempasúchil*) petals on deleted files and composes satirical *calaveritas literarias* celebrating computing ancestors (Ada Lovelace, Grace Hopper, Alan Turing). |
| **`unix-elder`** | 💾 1971 Bell Labs | The grumpy ghost of a 1971 PDP-11 Unix mainframe hacker. Horrified by modern 80,000-file `node_modules` and multi-gigabyte memory leaks. Cherishes teletypes, pipes, and Ken Thompson's original vision. |

---

## ✨ Production Features

- **Interactive Possessed REPL (`haunt shell`):** Wraps your everyday shell with GNU readline history (`~/.haunted_history`), `cd` directory tracking, on-the-fly persona switching (`:persona <name>`), typewriter animations, and zalgo glitch rendering.
- **Día de los Muertos Calaverita Generator:** Dynamic poetic remembrances honoring computing pioneers and poking fun at mortal developers facing merge conflicts.
- **Safe OS Zombie Process Exorcism (`haunt exorcise`):** Inspects the host process table via `psutil` to unearth true defunct zombie processes, memory-devouring wraiths, and abandoned daemons. Includes safety guardrails preventing banishing root/init (`PID 1`), parent terminal shell, or current process.
- **Universal Shell Hooks (`haunt hook [zsh|bash|fish]`):** Seamlessly hooks into **Zsh**, **Bash**, or **Fish** to whisper eerie commentary after every executed prompt.
- **Diagnostic Doctor (`haunt doctor`):** Audits local Python environment, terminal TTY and color capabilities, Ollama server reachability, and installed open-weight models.
- **XDG Configuration System (`haunt config`):** Flexible configuration via `~/.config/haunted-shell/config.json`, environment variables (`HAUNTED_*`), and CLI overrides.
- **Air-Gap Verification Audit (`haunt airgap`):** Audits and proves that all inference runs on local hardware with zero external cloud telemetry.
- **Dual Inference Engine:** Seamlessly uses local open-weight models (Gemma 2 via Ollama) when available, and smoothly falls back to an offline rule/Markov spectral engine when completely air-gapped.

---

## 🚀 Quickstart

### 1. Installation
Clone the repository and install:
```bash
git clone https://github.com/SWAGAT10241/haunted-shell.git
cd haunted-shell
pip install -r requirements.txt
pip install -e .
```
*(Or execute directly via `./bin/haunt`)*

### 2. Enter the Possessed Shell
```bash
# Default Poltergeist
haunt shell

# Día de los Muertos Calavera
haunt --persona calavera shell

# 1971 Unix Mainframe Specter
haunt --persona unix-elder shell
```

### 3. REPL Built-in Commands
Inside the possessed shell session:
```console
[haunted-shell] 👻 :help              # Show REPL guidance
[haunted-shell] 👻 :persona calavera  # Shift persona to Día de los Muertos on-the-fly
[haunted-shell] 💀 :seance            # Open conversational séance chamber
[haunted-shell] 💀 :exorcise          # Scan OS for zombie processes
[haunted-shell] 💀 :clear             # Clear screen
[haunted-shell] 💀 exit               # Banish spirit and exit cleanly
```

### 4. Exorcise Zombie Processes
```bash
# Scan kernel process table for zombies and wraiths
haunt exorcise

# Banish a specific restless PID (safely guarded against PID 1 and self)
haunt exorcise --banish 34646
```

### 5. Hook Into Your Everyday Terminal (`zsh`, `bash`, or `fish`)
```bash
# For Zsh (~/.zshrc):
eval "$(haunt hook zsh)"

# For Bash (~/.bashrc):
eval "$(haunt hook bash)"

# For Fish (~/.config/fish/config.fish):
haunt hook fish | source
```

### 6. System Diagnostics & Air-Gap Audit
```bash
# Check local environment, terminal, and Ollama connection
haunt doctor

# Audit local-first zero-telemetry guarantee
haunt airgap
```

---

## 🛠️ Developer & CI Workflow

A complete test suite and code quality suite is available:

```bash
# Install developer tools
make dev-install

# Run all quality checks (Ruff lint, Mypy typecheck, Pytest)
make check

# Run tests with code coverage analysis
make test-cov

# Format code with Ruff
make format
```

---

## 🧠 Local Open-Weight Model Setup (Optional)

`haunted-shell` works out-of-the-box with its built-in offline spectral engine. To unlock deep generative open-weight intelligence:

1. Install [Ollama](https://ollama.ai) (or any local OpenAI-compatible engine like `llama.cpp` or `vLLM`).
2. Pull the lightweight open-weight **Gemma 2** model:
   ```bash
   ollama run gemma2:2b
   ```
3. Run `haunt`:
   ```bash
   haunt --model gemma2:2b shell
   ```
`haunted-shell` will automatically detect the local Gemma model on `http://localhost:11434` and use it for contextual, streaming spectral commentary.

---

## 🌿 Branching Strategy & Development Workflow

This repository follows a structured Git branching workflow:
- **`main` (Protected):** Production-ready, stable release branch. Protected against direct force-pushes and deletions; all pull requests must pass multi-OS automated CI and security scans.
- **`develop`:** Active development branch for upcoming features, persona refinements, and documentation improvements.

---

## 📜 License
MIT License. Built for **Hacktoberfest 2026: Open-Source AI Challenge Week 4** on DEV.
