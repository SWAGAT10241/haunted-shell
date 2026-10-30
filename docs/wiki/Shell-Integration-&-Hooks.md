# 🐚 Shell Integration & Hooks

You do not need to run inside a separate subshell (`haunt shell`) to experience possession. You can hook `haunted-shell` directly into your daily **Zsh** or **Bash** terminal prompt.

---

## ⚡ Zsh Integration (`~/.zshrc`)

Add the following to your `~/.zshrc`:
```zsh
eval "$(haunt hook zsh)"
```

### How It Works Under the Hood:
Uses `add-zsh-hook` to bind:
- `preexec`: Captures the typed command string.
- `precmd`: Reads the command's exit code (`$?`) and invokes `haunt whisper "$_HAUNTED_LAST_CMD" --exit-code "$last_status"`.

---

## ⚡ Bash Integration (`~/.bashrc`)

Add the following to your `~/.bashrc`:
```bash
eval "$(haunt hook bash)"
```

Uses `PROMPT_COMMAND` to inspect bash history and exit code on every prompt render.
