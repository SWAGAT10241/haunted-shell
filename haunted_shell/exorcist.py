"""
Exorcist: Detects zombie processes, orphaned daemons, and memory-devouring wraiths on the host system.
Features safety guardrails to prevent banishing critical kernel or shell PIDs.
"""

import os
import random
import time
from typing import Any, Dict, List, Optional, Set, Tuple

import psutil

from .logger import logger
from .ui import BLOOD_RED, BOLD, DEATH_GRAY, DIM, GHOST_PURPLE, RESET, SLIME_GREEN, spectral_box

EPITAPHS = [
    "Spawned in haste, abandoned in cold memory. It wanders kernel space seeking its parent PID.",
    "A runaway loop that slipped past the bounds of mortality, consuming heap like a starving ghoul.",
    "Dead in purpose, yet refusing to yield its slot in the process table.",
    "An uncollected corpse in the operating system cemetery, awaiting waitpid() redemption.",
    "A spectral daemon born at midnight, whispering into broken pipes that lead to nowhere.",
]

PROTECTED_NAMES: Set[str] = {
    "launchd", "systemd", "init", "kernel_task", "kthreadd", "haunted-shell", "haunt"
}


class Exorcist:
    """Manages process zombie inspection, memory profiling, and safe process termination."""

    def __init__(self):
        self._current_pid = os.getpid()
        self._parent_pid = os.getppid()

    def is_protected(self, pid: int, name: Optional[str] = None) -> Tuple[bool, str]:
        """Check if target PID is protected from banishment."""
        if pid <= 1:
            return True, f"PID {pid} is the root kernel/init process and cannot be banished."
        if pid == self._current_pid:
            return True, f"PID {pid} is the current haunted-shell process (suicide averted)."
        if pid == self._parent_pid:
            return True, f"PID {pid} is the host terminal shell process."

        if name and name.lower() in PROTECTED_NAMES:
            return True, f"Process '{name}' is a critical protected system supervisor."

        return False, ""

    def scan_spirits(self, limit: int = 7) -> List[Dict[str, Any]]:
        """Inspect all running processes to find zombies, dead pipes, and heavy wraiths."""
        spirits: List[Dict[str, Any]] = []
        now = time.time()

        for proc in psutil.process_iter(['pid', 'name', 'status', 'create_time', 'memory_info', 'ppid']):
            try:
                info = proc.info
                status = info.get('status')
                pid = info.get('pid')
                if pid is None or pid <= 1:
                    continue

                name = info.get('name') or "unknown_specter"
                create_time = info.get('create_time') or now
                age_minutes = max(0.0, (now - create_time) / 60.0)

                mem_info = info.get('memory_info')
                mem_bytes = mem_info.rss if mem_info else 0
                mem_mb = mem_bytes / (1024 * 1024)

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

        # If few zombies/wraiths, supplement with top background daemons
        if len(spirits) < 3:
            for proc in psutil.process_iter(['pid', 'name', 'status', 'create_time', 'memory_info']):
                try:
                    info = proc.info
                    pid = info.get('pid')
                    if pid is None or pid <= 1 or pid in [s['pid'] for s in spirits]:
                        continue
                    name = info.get('name') or "daemon"
                    mem_info = info.get('memory_info')
                    mem_bytes = mem_info.rss if mem_info else 0
                    mem_mb = mem_bytes / (1024 * 1024)

                    if mem_mb > 150:
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

    def render_spectral_report(self, spirits: List[Dict[str, Any]]) -> None:
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

    def exorcise(self, pid: int, force: bool = False) -> Tuple[bool, str]:
        """
        Banish a process spirit via SIGTERM or SIGKILL with safety checks.
        Returns (success: bool, message: str).
        """
        try:
            p = psutil.Process(pid)
            proc_name = p.name()
        except (psutil.NoSuchProcess, psutil.ZombieProcess):
            return False, f"PID {pid} no longer exists in the process table (already vanished)."
        except psutil.AccessDenied:
            proc_name = "unknown"

        # Check safety guardrails
        blocked, reason = self.is_protected(pid, proc_name)
        if blocked:
            logger.warning("Banishment blocked for PID %d: %s", pid, reason)
            return False, reason

        try:
            if force:
                p.kill()
            else:
                p.terminate()

            p.wait(timeout=1.0)
            return True, f"Spirit PID {pid} ({proc_name}) banished back into the void."
        except psutil.TimeoutExpired:
            return False, f"PID {pid} resisted SIGTERM. Use --force for SIGKILL."
        except psutil.AccessDenied:
            return False, f"Access denied banishing PID {pid}. Run with elevated privileges."
        except Exception as exc:
            return False, f"Error banishing PID {pid}: {exc}"
