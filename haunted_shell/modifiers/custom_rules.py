"""
Custom user-defined command rule modifiers.
Loads custom trigger rules from JSON/YAML configuration files.
"""

import json
import os
import random
from typing import Dict, List, Optional

DEFAULT_RULES = {
    "docker": [
        "You isolate daemons inside cgroups... but containers cannot contain the restless void.",
        "Spinning up another 2-gigabyte image? Your storage drive groans beneath the heap of abandoned layers.",
    ],
    "npm": [
        "You invite 40,000 strangers from the registry graveyard to execute unvetted code in node_modules...",
        "A black hole opens in disk space. Not even light can escape the density of that dependency tree.",
    ],
    "cargo": [
        "The Borrow Checker is the harshest reaper of all. Not even a phantom may violate lifetimes.",
        "Zero-cost abstractions? The only cost here is your mortal patience while rustc compiles.",
    ],
    "python": [
        "The Global Interpreter Lock holds all threads in an eternal bottlenecked slumber...",
        "Indentation determines your fate. One stray space and the spirits shall cast an IndentationError.",
    ],
    "vim": [
        "Abandon all hope, ye who enter `:wq`. The crypt doors have slammed shut behind you.",
        "You entered Vim looking for a simple edit. Legend has it you are still trying to quit.",
    ],
    "curl": [
        "Reaching cold digital tentacles out across the wire... What horrors lurk on remote port 443?",
    ],
    "make": [
        "Invoking the ancient Makefile runes. Even the ancients feared the terror of missing tabs.",
    ],
}


class CustomRuleEngine:
    def __init__(self, config_paths: Optional[List[str]] = None):
        self.rules: Dict[str, List[str]] = dict(DEFAULT_RULES)
        self.config_paths = config_paths or [
            os.path.expanduser("~/.config/haunted-shell/modifiers.json"),
            os.path.expanduser("~/.haunted_modifiers.json"),
            os.path.abspath("./haunted_modifiers.json"),
        ]
        self.load_rules()

    def load_rules(self):
        """Load user-defined custom command rules from disk."""
        for path in self.config_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        user_rules = json.load(f)
                        if isinstance(user_rules, dict):
                            for cmd, responses in user_rules.items():
                                if isinstance(responses, list):
                                    self.rules[cmd.lower()] = responses
                                elif isinstance(responses, str):
                                    self.rules[cmd.lower()] = [responses]
                except Exception:
                    pass

    def match(self, command_str: str) -> Optional[str]:
        """Check if command matches any custom trigger rule."""
        tokens = command_str.strip().split()
        if not tokens:
            return None
        base = tokens[0].lower()
        if base in {"sudo", "doas"} and len(tokens) > 1:
            base = tokens[1].lower()

        # Direct command match
        if base in self.rules:
            return random.choice(self.rules[base])

        # Subcommand or substring match (e.g. "docker compose", "npm install")
        for key, responses in self.rules.items():
            if key in command_str.lower():
                return random.choice(responses)
        return None

    def export_sample(self, target_path: str):
        """Export sample custom modifiers file for users to edit."""
        sample = {
            "docker": [
                "Custom haunting: Containers in the mist...",
                "The ghost of an unpruned volume haunts /var/lib/docker.",
            ],
            "kubectl": [
                "Pods dying across the cluster like autumn leaves...",
                "CrashLoopBackOff: The spirit refuses to stabilize.",
            ],
            "terraform": [
                "Terraform plan reveals the ruin you are about to unleash upon the cloud."
            ],
        }
        os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(sample, f, indent=2)
