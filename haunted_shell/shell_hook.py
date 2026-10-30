"""
Shell hook generator for integrating haunted-shell seamlessly into zsh, bash, or fish.
"""

ZSH_HOOK_TEMPLATE = """# ─────────────────────────────────────────────────────────────
#  H A U N T E D   S H E L L   Z S H   I N T E G R A T I O N
#  Add this to your ~/.zshrc or run: eval "$(haunt hook zsh)"
# ─────────────────────────────────────────────────────────────

autoload -Uz add-zsh-hook

typeset -g _HAUNTED_LAST_CMD=""

_haunted_preexec() {
  typeset -g _HAUNTED_LAST_CMD="$1"
}

_haunted_precmd() {
  local last_status=$?
  if [[ -n "$_HAUNTED_LAST_CMD" ]]; then
    haunt whisper "$_HAUNTED_LAST_CMD" --exit-code "$last_status"
    unset _HAUNTED_LAST_CMD
  fi
}

add-zsh-hook preexec _haunted_preexec
add-zsh-hook precmd _haunted_precmd
"""

BASH_HOOK_TEMPLATE = """# ─────────────────────────────────────────────────────────────
#  H A U N T E D   S H E L L   B A S H   I N T E G R A T I O N
#  Add this to your ~/.bashrc or run: eval "$(haunt hook bash)"
# ─────────────────────────────────────────────────────────────

_haunted_prompt_command() {
  local last_status=$?
  local last_cmd=$(HISTTIMEFORMAT= history 1 | sed 's/^[ ]*[0-9]*[ ]*//')
  if [ -n "$last_cmd" ] && [ "$last_cmd" != "$_HAUNTED_PREV_CMD" ]; then
    _HAUNTED_PREV_CMD="$last_cmd"
    haunt whisper "$last_cmd" --exit-code "$last_status"
  fi
}

if [[ ! "$PROMPT_COMMAND" =~ "_haunted_prompt_command" ]]; then
  PROMPT_COMMAND="_haunted_prompt_command; $PROMPT_COMMAND"
fi
"""

FISH_HOOK_TEMPLATE = """# ─────────────────────────────────────────────────────────────
#  H A U N T E D   S H E L L   F I S H   I N T E G R A T I O N
#  Add this to ~/.config/fish/config.fish or run: haunt hook fish | source
# ─────────────────────────────────────────────────────────────

function __haunted_postexec --on-event fish_postexec
    set -l last_status $status
    haunt whisper "$argv" --exit-code "$last_status"
end
"""


def generate_hook(shell_name: str = "zsh") -> str:
    """Generate shell hook integration script for specified shell."""
    shell = shell_name.lower().strip()
    if "fish" in shell:
        return FISH_HOOK_TEMPLATE
    elif "bash" in shell:
        return BASH_HOOK_TEMPLATE
    return ZSH_HOOK_TEMPLATE
