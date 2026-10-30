# 🧟 Exorcism & Kernel Process Monitoring

In operating systems, defunct processes that have completed execution but still occupy a slot in the process table are known as **zombie processes** (`Z` state).

---

## 🔎 How the Exorcist Works

The `Exorcist` module leverages `psutil` to inspect the host OS process table in real-time, categorizing restless spirits:
1. **Zombies (`psutil.STATUS_ZOMBIE`):** Defunct children awaiting parent reaping via `waitpid()`.
2. **Orphaned Shades:** Processes with PPID 1 that were abandoned when their parent terminated.
3. **Memory Wraiths:** Rogue processes consuming excessive RAM (> 600MB).

---

## ⚡ Exorcism Commands

```bash
# Perform a spectral necropsy scan
haunt exorcise

# Banish a specific PID via SIGTERM
haunt exorcise --banish 1311

# Force banish via SIGKILL
haunt exorcise --banish 1311 --force
```
