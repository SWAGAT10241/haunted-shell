# 🏛️ Architecture & System Design

The architecture of `haunted-shell` adheres to the classic Unix philosophy: modular components, stdin/stdout piping, minimal dependencies, and strict data isolation.

---

## 📐 System Pipeline

```
┌────────────────────────────────────────────────────────┐
│                   User Shell Command                   │
└───────────────────────────┬────────────────────────────┘
                            │
              ┌─────────────▼─────────────┐
              │    Subprocess Execution   │
              └─────────────┬─────────────┘
                            │ (Exit code, CWD, Command tokens)
              ┌─────────────▼─────────────┐
              │       GhostEngine         │
              └──────┬─────────────┬──────┘
                     │             │
        (If available)             (Air-gapped fallback)
                     │             │
        ┌────────────▼──────┐   ┌──▼──────────────────────────┐
        │ Local Open-Weight │   │ Offline Spectral Engine     │
        │ Model (Gemma 2 via│   │ (Contextual matrices,       │
        │ Ollama/localhost) │   │ calaveritas & glitch-zalgo) │
        └────────────┬──────┘   └──┬──────────────────────────┘
                     │             │
                     └──────┬──────┘
                            │
              ┌─────────────▼─────────────┐
              │  Modifier Pipeline Layer  │
              │  (Tone & Visual Glitches) │
              └─────────────┬─────────────┘
                            │
              ┌─────────────▼─────────────┐
              │    Typewriter & ANSI UI   │
              └───────────────────────────┘
```

---

## 🔒 The Air-Gap Philosophy

Because developers execute commands containing SSH private keys, AWS tokens, database credentials, and proprietary code, `haunted-shell` enforces a strict **Zero External Telemetry** policy:
- No analytics or crash tracking SDKs.
- No outbound HTTP/HTTPS calls to commercial third-party cloud AI APIs.
- All neural inference is strictly bound to `http://localhost:11434` (Ollama) or internal local servers.
- When no local model server is reachable, it executes purely through offline Python algorithms without touching sockets.
