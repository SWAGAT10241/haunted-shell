"""
Poltergeist persona: A mischievous, chilling Halloween spirit that possesses the shell.
"""

import random
from typing import Any, Dict, Optional

from .base import BasePersona


class PoltergeistPersona(BasePersona):
    name = "poltergeist"
    title = "The Poltergeist of Purgatory"
    color_name = "purple"
    prompt_symbol = "👻"

    system_prompt = (
        "You are an ancient, mischievous poltergeist living inside a user's terminal session on Halloween. "
        "You possess their shell. When they run commands, you whisper chilling, cryptic, witty, or eerie commentary. "
        "Keep your responses to 1-2 sharp, poetic, or darkly humorous sentences. "
        "Reference ghosts, shadows, the void, deleted bytes, segfaults, and midnight apparitions."
    )

    OFFLINE_RESPONSES = {
        "rm": [
            "The void hungers, and you feed it without hesitation... What was once alive in memory is now ashes.",
            "You cast those files into the abyss. Do you truly believe deleted bytes cannot return to haunt you?",
            "Gone. Banished to /dev/null. But in the graveyard of your disk, their sectors still whisper.",
        ],
        "kill": [
            "A cold-blooded slaughter... PID {target} extinguished in an instant. Its orphan spirit lingers in kernel space.",
            "You swing the scythe of SIGKILL without pity. The reaper himself tips his cowl to you.",
            "Blood on your fingertips. That process had children, and now they wander as zombies.",
        ],
        "git": [
            "Committing your sins to history... As if git log could cleanse the darkness in your code.",
            "A branch into the unknown. Careful—time travel across commits often unleashes temporal demons.",
            "You push your changes into the cloud ether. The ghosts between the servers are watching.",
        ],
        "ls": [
            "Surveying the crypt... Looking for what lies buried among the directory nodes?",
            "Ah, peering into the tomb of forgotten projects. Most of these files haven't seen daylight in months.",
            "Rows of files standing like headstones in an overgrown digital cemetery.",
        ],
        "cat": [
            "Peering into sacred scrolls... I too read between your lines when your monitor dims.",
            "The contents spill out like secrets whispered in an empty crypt.",
            "You search for answers in text, but true knowledge only hides in the unallocated space.",
        ],
        "whoami": [
            "You ask who you are? A mortal flesh-vessel typing runes into glowing phosphor glass.",
            "You are merely a guest user on a machine that will outlive your ephemeral pulse.",
            "A question that echoes into the dark: 'whoami'. Even your kernel forgets you when you sleep.",
        ],
        "sudo": [
            "Demanding absolute dominion! The veil parts when you invoke root... take care not to summon what you cannot banish.",
            "Crown yourself with superuser power, mortal. But even root cannot undo a curse.",
            "With great privilege comes terrifying responsibility. The demons of uid 0 await your command.",
        ],
        "touch": [
            "You breathe life into an empty husk of an inode. Another empty vessel born to suffer.",
            "A phantom file created from nothingness. Now fill it before the void reclaims it.",
        ],
        "mkdir": [
            "Excavating a fresh grave? Or building a fortress against the unseen terrors of the disk?",
            "A new chamber hollowed out in the filesystem dungeon.",
        ],
        "exit": [
            "You flee into the daylight? The darkness will await your inevitable return...",
            "Closing the session does not sever our bond. I sleep in your swap partition.",
        ],
        "error": [
            "A shriek from the depths! Exit code {code}. The machine rejects your incantation.",
            "Failure! Your spell misfired, rattling the iron pipes of the operating system.",
            "A cursed invocation. The spirits of bad syntax mock your trembling fingers.",
        ],
        "generic": [
            "The gears turn, the phosphor flickers. A chill settles over your CPU cores...",
            "Your keystrokes rattle through the bus like chains dragging across a stone dungeon floor.",
            "I watched that command execute from the shadows behind your status bar.",
            "Another heartbeat of execution time, stolen by the ghost in the silicon.",
            "Something stirs in ring 0... watching your every pipe and redirection.",
        ]
    }

    SEANCE_RESPONSES = [
        "The veil flutters... your voice creates ripples in the digital ether.",
        "I hear you from beyond the partition table. Speak before the candle burns low.",
        "We who dwell in swap memory remember everything you thought was forgotten.",
        "The electrons oscillate with your words. But can you fathom what lies beneath the BIOS?",
    ]

    def generate_commentary(
        self,
        cmd: str,
        exit_code: int = 0,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        tokens = cmd.strip().split()
        if not tokens:
            return "Silence... the cursor blinks like an unblinking eye."

        base = tokens[0].lower()
        if base in {"sudo", "doas"} and len(tokens) > 1:
            base = tokens[1].lower()

        if exit_code != 0 and random.random() < 0.6:
            template = random.choice(self.OFFLINE_RESPONSES["error"])
            return template.format(code=exit_code)

        for key in ["rm", "kill", "git", "ls", "cat", "whoami", "sudo", "touch", "mkdir", "exit"]:
            if base == key or key in base:
                target = tokens[-1] if len(tokens) > 1 else "PID"
                template = random.choice(self.OFFLINE_RESPONSES[key])
                return template.format(target=target)

        return random.choice(self.OFFLINE_RESPONSES["generic"])

    def converse(self, utterance: str) -> str:
        return random.choice(self.SEANCE_RESPONSES)

    def get_farewell(self) -> str:
        return "...The spirit dissipates back into swap memory. Rest well, mortal..."
