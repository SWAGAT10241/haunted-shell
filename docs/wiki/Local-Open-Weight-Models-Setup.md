# 🧠 Local Open-Weight Models Setup

`haunted-shell` works out-of-the-box with zero configuration using its built-in offline spectral rules engine.

To unlock deep generative open-weight AI capabilities, you can connect it to local model servers such as **Ollama**, **llama.cpp**, or **vLLM**.

---

## 🚀 Recommended: Google Gemma 2 via Ollama

1. Install [Ollama](https://ollama.ai).
2. Pull the lightweight open-weight **Gemma 2** model:
   ```bash
   ollama pull gemma2:2b
   ```
3. Run `haunt`:
   ```bash
   haunt --model gemma2:2b shell
   ```

`GhostEngine` automatically discovers the local Ollama server on `http://localhost:11434` and routes prompt inferences locally with strict timeouts and zero data egress.

---

## 🔒 Verifying Air-Gap Isolation

To audit and prove to judges or security auditors that no data leaves your machine:
```bash
haunt airgap
```

Output:
```console
┌─[ AIR-GAP & PRIVACY AUDIT ]────────────────────┐
│ Active Persona: poltergeist                    │
│ Active Modifiers: none                         │
│ Inference Engine: Local Open-Weight Model      │
│ Configured Model: gemma2:2b                    │
│ External Telemetry: DISABLED (100% Local)      │
│ Can Run Offline: YES (Zero Cloud Dependencies) │
│ Hardware Isolation: Safe for Air-gapped Laptops │
└────────────────────────────────────────────────┘
```
