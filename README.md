# 👻 haunted-shell: Ghost in the Machine

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

`haunted-shell` is an open-source, privacy-first terminal companion that **possesses your shell**. Whenever you execute commands (`git push`, `rm -rf`, `kill -9`, `cat`, `whoami`), an eerie spirit materializes in your terminal to whisper chilling commentary, compose Día de los Muertos *calaveritas literarias*, roast modern software bloat, and track down real zombie processes lurking in your OS process table.

Built with **open-source AI at its core**, `haunted-shell` connects directly to local open-weight models (such as **Google Gemma 2**, Llama, or Mistral via Ollama/llama.cpp) and includes a zero-dependency offline spectral engine that runs 100% locally with zero cloud telemetry.

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

You can summon different spirits to possess your shell using `--persona`:

| Persona | Theme | Description |
|---|---|---|
| **`poltergeist`** | 🎃 Halloween | Sarcastic, chilling Halloween ghost. Delights in deleted inodes, laughs at failed commands (`exit code != 0`), and warns of dark forces in ring 0. |
| **`calavera`** | 🌼 Día de los Muertos | Celebrates the beauty of transience in the spirit of Día de los Muertos. Lays marigold (*cempasúchil*) petals on deleted files and composes satirical *calaveritas literarias* celebrating computing ancestors (Ada Lovelace, Grace Hopper, Alan Turing). |
| **`unix-elder`** | 💾 1971 Bell Labs | The grumpy ghost of a 1971 PDP-11 Unix mainframe hacker. Horrified by modern 80,000-file `node_modules` and multi-gigabyte memory leaks. Cherishes teletypes, pipes, and Ken Thompson's original vision. |

---

## ✨ Features

- **Interactive Possessed REPL (`haunt shell`):** Wraps your everyday shell. Run real commands; after each command finishes, the specter speaks with typewriter animations and subtle glitch/zalgo text effects.
- **Día de los Muertos Calaverita Generator:** Dynamic poetic remembrances honoring computing pioneers and poking fun at mortal developers facing merge conflicts.
- **Real OS Zombie Process Exorcism (`haunt exorcise`):** Inspects the host operating system's process table via `psutil` to unearth true defunct zombie processes, memory-devouring wraiths, and abandoned daemons, rendering custom gothic epitaphs with the option to banish (`SIGTERM`/`SIGKILL`) them.
- **Shell Hooks for Zsh & Bash (`haunt hook`):** Possess your daily terminal prompt automatically via `precmd`/`preexec` hooks without needing a subshell.
- **Air-Gap Verification Audit (`haunt airgap`):** Audits and proves that all inference runs on local hardware with zero external cloud telemetry.
- **Dual Inference Engine:** Seamlessly uses local open-weight models (Gemma 2 via Ollama) when available, and smoothly falls back to an offline rule/Markov spectral engine when completely air-gapped.

---

## 🚀 Quickstart

### 1. Installation
Clone the repository and run:
```bash
git clone https://github.com/swagatsouravdhar/haunted-shell.git
cd haunted-shell
pip install -r requirements.txt
pip install -e .
```
*(Or run directly via `./bin/haunt`)*

### 2. Enter the Possessed Shell
```bash
# Default Poltergeist
haunt shell

# Día de los Muertos Calavera
haunt --persona calavera shell

# 1971 Unix Mainframe Specter
haunt --persona unix-elder shell
```

### 3. Exorcise Zombie Processes
```bash
# Scan kernel process table for zombies and wraiths
haunt exorcise

# Banish a specific restless PID
haunt exorcise --banish 1311
```

### 4. Possess Your Everyday Terminal (`~/.zshrc` / `~/.bashrc`)
To make your everyday terminal possessed on every command:
```bash
# For Zsh:
eval "$(haunt hook zsh)"

# For Bash:
eval "$(haunt hook bash)"
```

### 5. Verify Air-Gap Isolation
```bash
haunt airgap
```

---

## 🖥️ Live Terminal Previews

### Possession on Common Commands
```console
[haunted-shell] 👻 rm -rf old_secrets.txt
  👻  Gone. Banished to /dev/null. But in the graveyard of your disk, their sectors still whisper.

[haunted-shell] 👻 kill -9 4120
  👻  A cold-blooded slaughter... PID 4120 extinguished in an instant. Its orphan spirit lingers in kernel space.

[haunted-shell] 💀 git commit -m "Fix memory leak"
  💀  Estaba la Catrina sentada en el disco / viendo tus commits con sonrisa y pellizco:
      '¡No te apures, dev, por ese merge conflict / que en el camposanto todo queda fixed!'
```

### Spectral Process Necropsy
```console
$ haunt exorcise
┌─[ SPECTRAL PROCESS NECROPSY ]────────────────────────────────────────────────────┐
│ Detected 3 restless entity/entities lurking in memory:                           │
│                                                                                  │
│ • PID 34646 [Memory Wraith] - Code Helper (Renderer)                             │
│   Memory: 200.7 MB | Age: 36.2 mins                                              │
│   "Devours 200.7 MB of physical memory like a restless devourer."                │
│                                                                                  │
│ • PID 41047 [Shadow Daemon] - language_server                                    │
│   Memory: 201.7 MB | Age: 8.3 mins                                               │
│   "Spawned in haste, abandoned in cold memory. It wanders kernel space..."       │
└──────────────────────────────────────────────────────────────────────────────────┘
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

## 📜 License
MIT License. Built for **Hacktoberfest 2026: Open-Source AI Challenge Week 4** on DEV.
