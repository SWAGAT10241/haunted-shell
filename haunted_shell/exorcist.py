"""
Exorcist: Detects zombie processes, orphaned daemons, and memory-devouring wraiths on the host system.
"""

import os
import time
import random
from typing import List, Dict, Any, Optional
import psutil

from .ui import (
    BOLD, RESET, DIM, BLOOD_RED, GHOST_PURPLE, SLIME_GREEN,
    DEATH_GRAY, spectral_box
)


EPITAPHS = [
    "Spawned in haste, abandoned in cold memory. It wanders kernel space seeking its parent PID.",
    "A runaway loop that slipped past the bounds of mortality, consuming heap like a starving ghoul.",
    "Dead in purpose, yet refusing to yield its slot in the process table.",
    "An uncollected corpse in the operating system cemetery, awaiting waitpid() redemption.",
    "A spectral daemon born at midnight, whispering into broken pipes that lead to nowhere.",
]


class Exorcist:
    def scan_spirits(self, limit: int = 7) -> List[Dict[str, Any]]:
        """Inspect all running processes to find zombies, dead pipes, and heavy wraiths."""
        spirits = []
        now = time.time()

        for proc in psutil.process_iter(['pid', 'name', 'status', 'create_time', 'memory_info', 'ppid']):
            try:
                info = proc.info
                status = info.get('status')
                pid = info.get('pid')
                name = info.get('name') or "unknown_specter"
                create_time = info.get('create_time') or now
                age_minutes = (now - create_time) / 60.0
                mem_bytes = info['memory_info'].rss if info.get('memory_info') else 0
                mem_mb = mem_bytes / (1024 * 1024)
                ppid = info.get('ppid')

                is_zombie = (status == psutil.STATUS_ZOMBIE) or ("defunct" in name.lower())
                is_wraith = (mem_mb > 600)  # Heavy memory devourer (> 600MB)

                if is_zombie:
                    spirits.append({
                        "pid": pid,
                        "name": name,
                        "type": "Zombie (Defunct)",
                        "age_min": round(age_minutes, 1),
                        "mem_mb": round(mem_mb, 1),
                        "epitaph": random.choice(EPITAPHS),
                        "danger": "HIGH"
                    })
                elif is_wraith and len(spirits) < limit:
                    spirits.append({
                        "pid": pid,
                        "name": name,
                        "type": "Memory Wraith",
                        "age_min": round(age_minutes, 1),
                        "mem_mb": round(mem_mb, 1),
                        "epitaph": f"Devours {round(mem_mb, 1)} MB of physical memory like a restless devourer.",
                        "danger": "LOW"
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # If no strict zombies found, add top long-running background tasks
        if len(spirits) < 3:
            for proc in psutil.process_iter(['pid', 'name', 'status', 'create_time', 'memory_info']):
                try:
                    info = proc.info
                    pid = info.get('pid')
                    name = info.get('name') or "daemon"
                    mem_bytes = info['memory_info'].rss if info.get('memory_info') else 0
                    mem_mb = mem_bytes / (1024 * 1024)
                    if mem_mb > 150 and pid not in [s['pid'] for s in spirits]:
                        spirits.append({
                            "pid": pid,
                            "name": name,
                            "type": "Shadow Daemon",
                            "age_min": round((now - (info.get('create_time') or now)) / 60.0, 1),
                            "mem_mb": round(mem_mb, 1),
                            "epitaph": random.choice(EPITAPHS),
                            "danger": "MEDIUM"
                        })
                    if len(spirits) >= limit:
                        break
                except Exception:
                    continue

        return spirits[:limit]

    def render_spectral_report(self, spirits: List[Dict[str, Any]]):
        """Render a formatted supernatural census of processes."""
        if not spirits:
            spectral_box(
                "SANCTUARY DECREE",
                [
                    "No zombies or restless wraiths haunt your kernel process table.",
                    "The system sleeps in blessed, undisturbed peace.",
                    "All child processes have been dutifully reaped."
                ],
                color=SLIME_GREEN
            )
            return

        lines = [
            f"Detected {len(spirits)} restless entity/entities lurking in memory:",
            ""
        ]
        for s in spirits:
            type_color = BLOOD_RED if "Zombie" in s["type"] else GHOST_PURPLE
            lines.append(f"• PID {BOLD}{s['pid']}{RESET} [{type_color}{s['type']}{RESET}] - {s['name']}")
            lines.append(f"  {DIM}Memory: {s['mem_mb']} MB | Age: {s['age_min']} mins{RESET}")
            lines.append(f"  {DEATH_GRAY}\"{s['epitaph']}\"{RESET}")
            lines.append("")

        spectral_box("SPECTRAL PROCESS NECROPSY", lines, color=BLOOD_RED)

    def exorcise(self, pid: int, force: bool = False) -> bool:
        """Banish a process spirit via SIGTERM or SIGKILL."""
        try:
            p = psutil.Process(pid)
            if force:
                p.kill()
            else:
                p.terminate()
            p.wait(timeout=1.0)
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            return False
