# ⚙️ Custom Modifiers Guide

`haunted-shell` features a unified modifier architecture allowing users to customize both **visual text transformations**, **spirit tone overlays**, and **user-defined command rules**.

---

## 🎨 Visual / Text Modifiers
Enable via `-M <name>`:

| Modifier | Description | Sample Output |
|---|---|---|
| `matrix` | Phosphor binary code rain | `0x00The ｦBorrow ｱChecker...` |
| `cursed` | Inverts text upside-down | `˙uʍouʞun ǝɥʇ oʇuᴉ ɥɔuɐɹq ∀` |
| `morse` | Appends telegraphic morse code | `... [📡 --.- --.-]` |
| `whisper` | Lowers case and spaces letters | `... d o   n o t   l o o k ...` |
| `vaporwave`| Aesthetic fullwidth typography | `Ｙｏｕ　ａｒｅ　ｍｅｒｅｌｙ...` |
| `zalgo` | Unicode combining diacritics | `G̕o̶n̡e. B̕a̢n̵i̕s̵h̴e̶d...` |

---

## 🎭 Tone Modifiers
- `eldritch`: Injects cosmic horror, non-Euclidean voids, and waking elder gods.
- `cyberpunk`: Injects corrupted neural ICE, rogue subroutines, and synthetic decay.
- `sarcastic`: Injects dry roasts mocking developer habits and Stack Overflow dependency.
- `gothic`: Injects 19th-century Victorian romanticism and tolling midnight bells.

---

## 📝 Custom Command Rules Configuration

Users can create a custom JSON file at `~/.config/haunted-shell/modifiers.json`:

```json
{
  "docker": [
    "You isolate daemons inside cgroups... but containers cannot contain the restless void."
  ],
  "npm": [
    "You invite 40,000 strangers from npm registry to execute unvetted code..."
  ],
  "kubectl": [
    "Pods dying across the cluster like autumn leaves in a cemetery."
  ]
}
```

Generate a starter configuration anytime with:
```bash
haunt modifier init
```
