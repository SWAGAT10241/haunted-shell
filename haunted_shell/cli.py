"""
Command line interface for haunted-shell: The Ghost in the Machine.
Production-grade terminal companion powered by local open-weight AI.
"""

import os
import readline
import subprocess
import sys
from pathlib import Path

import click

from .config import HauntedConfig, get_default_config_path, load_config, save_config
from .doctor import run_doctor
from .exorcist import Exorcist
from .ghost import GhostEngine
from .logger import setup_logger
from .personas import available_persona_names, get_persona, list_personas
from .shell_hook import generate_hook
from .ui import (
    BLOOD_RED,
    BOLD,
    DIM,
    GHOST_PURPLE,
    MARIGOLD_AMBER,
    RESET,
    SLIME_GREEN,
    SPECTRAL_CYAN,
    get_banner,
    set_color_enabled,
    spectral_box,
    typewriter,
)

__version__ = "1.0.0"

COLOR_MAP = {"poltergeist": GHOST_PURPLE, "calavera": MARIGOLD_AMBER, "unix-elder": SLIME_GREEN}


def _setup_readline(history_path: str) -> None:
    """Initialize GNU readline with history persistence."""
    try:
        hist = Path(history_path).expanduser()
        if hist.is_file():
            readline.read_history_file(str(hist))
        readline.set_history_length(1000)
    except Exception:
        pass


def _save_readline(history_path: str) -> None:
    """Save history on exit."""
    try:
        hist = Path(history_path).expanduser()
        hist.parent.mkdir(parents=True, exist_ok=True)
        readline.write_history_file(str(hist))
    except Exception:
        pass


@click.group(invoke_without_command=True)
@click.version_option(__version__, "-v", "--version", message="haunted-shell %(version)s")
@click.option(
    "--persona",
    "-p",
    default=None,
    type=click.Choice(["poltergeist", "calavera", "unix-elder"], case_sensitive=False),
    help="Spectral persona possessing the shell.",
)
@click.option(
    "--offline",
    "-o",
    is_flag=True,
    default=None,
    help="Force 100% offline mode (bypasses any local/external LLM probes).",
)
@click.option(
    "--model", "-m", default=None, help="Local open-weight model name (e.g. gemma2:2b, llama3.2)."
)
@click.option(
    "--glitch", "-g", default=None, type=int, help="Glitch/zalgo text intensity level (0 to 3)."
)
@click.option("--no-color", is_flag=True, default=False, help="Disable ANSI colors and styling.")
@click.option("--debug", is_flag=True, default=False, help="Enable debug logging output to stderr.")
@click.option(
    "--config",
    "-c",
    "config_file",
    default=None,
    type=click.Path(dir_okay=False),
    help="Path to custom configuration JSON file.",
)
@click.pass_context
def cli(ctx, persona, offline, model, glitch, no_color, debug, config_file):
    """👻 haunted-shell: A terminal possessed by open-source AI."""
    ctx.ensure_object(dict)

    # 1. Load configuration with CLI overrides
    cfg_path = Path(config_file).expanduser().resolve() if config_file else None
    overrides = {}
    if persona is not None:
        overrides["persona"] = persona.lower()
    if offline is not None:
        overrides["offline"] = offline
    if model is not None:
        overrides["model"] = model
    if glitch is not None:
        overrides["glitch_intensity"] = glitch
    if no_color:
        overrides["no_color"] = True
    if debug:
        overrides["debug"] = True

    config: HauntedConfig = load_config(config_path=cfg_path, **overrides)
    setup_logger(debug=config.debug)

    if config.no_color:
        set_color_enabled(False)

    ctx.obj["config"] = config
    ctx.obj["engine"] = GhostEngine(config=config)

    if ctx.invoked_subcommand is None:
        ctx.invoke(shell)


@cli.command()
@click.pass_context
def shell(ctx):
    """Enter the possessed interactive terminal REPL."""
    config: HauntedConfig = ctx.obj["config"]
    engine: GhostEngine = ctx.obj["engine"]
    _setup_readline(config.history_file)

    color = COLOR_MAP.get(engine.persona.name, GHOST_PURPLE)

    # Print spooky intro banner
    print(get_banner(engine.persona.name))
    status_mode = (
        "Offline Neural Persona Engine"
        if config.offline or not engine.has_local_model
        else f"Local Open-Weight Model [{config.model}]"
    )
    print(f"{DIM}👻 Spirit: {BOLD}{engine.persona.title}{RESET}")
    print(
        f"{DIM}🔒 Air-gap Security: {SLIME_GREEN}Verified Local-Only{RESET}{DIM} ({status_mode}){RESET}"
    )
    print(f"{DIM}💡 Type regular commands or ':help' for builtins. Type 'exit' to escape.{RESET}\n")

    prev_dir = os.getcwd()

    try:
        while True:
            cwd_short = os.path.basename(os.getcwd()) or "/"
            prompt_symbol = engine.persona.prompt_symbol
            prompt_str = f"{color}[{cwd_short}] {prompt_symbol} {RESET}"

            try:
                cmd = input(prompt_str).strip()
            except KeyboardInterrupt:
                print()  # Clean newline on Ctrl+C, do not terminate session
                continue
            except EOFError:
                print()
                typewriter(f"\n{engine.persona.get_farewell()}", color=color)
                break

            if not cmd:
                continue

            # Check built-in commands
            if cmd in {"exit", "quit", ":q", ":exit"}:
                farewell = engine.haunt_command("exit", exit_code=0)
                typewriter(f"\n{farewell}\n", color=color)
                break

            if cmd in {":help", "help"}:
                lines = [
                    f"Active Spirit: {engine.persona.title}",
                    "Type standard shell commands (ls, git, python, etc.) to execute them.",
                    "",
                    "Special Commands:",
                    "  :help               Show this spectral guidance",
                    "  :seance             Enter communion chamber with the spirit",
                    "  :exorcise           Scan running processes for zombies and wraiths",
                    "  :persona <name>     Switch active spirit (poltergeist, calavera, unix-elder)",
                    "  :clear              Clear terminal display",
                    "  :exit / quit        Depart the possessed session",
                ]
                spectral_box("HAUNTED REPL GUIDANCE", lines, color=color)
                continue

            if cmd == ":clear" or cmd == "clear":
                click.clear()
                continue

            if cmd.startswith(":persona"):
                parts = cmd.split(maxsplit=1)
                if len(parts) > 1 and parts[1].strip() in available_persona_names():
                    new_name = parts[1].strip().lower()
                    config.persona = new_name
                    engine = GhostEngine(config=config)
                    ctx.obj["engine"] = engine
                    color = COLOR_MAP.get(new_name, GHOST_PURPLE)
                    typewriter(
                        f"The veil shifts... {engine.persona.title} now inhabits the shell.\n",
                        color=color,
                    )
                else:
                    valid = ", ".join(available_persona_names())
                    print(f"Usage: :persona <{valid}>")
                continue

            if cmd in {":seance", "seance"}:
                ctx.invoke(seance)
                continue

            if cmd in {":exorcise", "exorcise"}:
                ctx.invoke(exorcise)
                continue

            # Handle cd
            if cmd == "cd" or cmd.startswith("cd "):
                target = cmd[3:].strip()
                if not target:
                    dest = os.path.expanduser("~")
                elif target == "-":
                    dest = prev_dir
                else:
                    dest = os.path.expanduser(target)

                try:
                    curr = os.getcwd()
                    os.chdir(dest)
                    prev_dir = curr
                    exit_code = 0
                except Exception as err:
                    print(f"cd: {err}", file=sys.stderr)
                    exit_code = 1
            else:
                try:
                    res = subprocess.run(cmd, shell=True)
                    exit_code = res.returncode
                except Exception as err:
                    print(f"Execution error: {err}", file=sys.stderr)
                    exit_code = 127

            # Spectral response
            whisper = engine.haunt_command(cmd, exit_code=exit_code)
            print()
            typewriter(f"  {prompt_symbol}  {whisper}", color=color)
            print()
    finally:
        _save_readline(config.history_file)


@cli.command()
@click.argument("command_str")
@click.option("--exit-code", "-e", default=0, type=int, help="Exit code of the executed command.")
@click.pass_context
def whisper(ctx, command_str, exit_code):
    """Whisper spooky commentary on a command (ideal for shell hooks)."""
    engine: GhostEngine = ctx.obj["engine"]
    color = COLOR_MAP.get(engine.persona.name, GHOST_PURPLE)

    comment = engine.haunt_command(command_str, exit_code=exit_code)
    prompt_symbol = engine.persona.prompt_symbol
    print(f"{color}{prompt_symbol} {comment}{RESET}")


@cli.command()
@click.option("--banish", "-b", type=int, default=None, help="PID of the spirit to exorcise.")
@click.option("--force", "-f", is_flag=True, default=False, help="Use SIGKILL instead of SIGTERM.")
@click.pass_context
def exorcise(ctx, banish, force):
    """Scan the operating system for zombie processes and memory wraiths."""
    exorcist = Exorcist()

    if banish is not None:
        click.echo(f"{BLOOD_RED}⚡ Channeling exorcism rite against PID {banish}...{RESET}")
        success, message = exorcist.exorcise(banish, force=force)
        if success:
            click.echo(f"{SLIME_GREEN}✓ {message}{RESET}")
        else:
            click.echo(f"{BLOOD_RED}✗ {message}{RESET}")
        return

    spirits = exorcist.scan_spirits()
    exorcist.render_spectral_report(spirits)
    if spirits:
        click.echo(
            f"\n{DIM}To banish a restless PID, run: {BOLD}haunt exorcise --banish <PID>{RESET}"
        )


@cli.command()
@click.pass_context
def seance(ctx):
    """Hold an interactive séance dialogue with the spirit."""
    engine: GhostEngine = ctx.obj["engine"]
    color = COLOR_MAP.get(engine.persona.name, GHOST_PURPLE)

    print(get_banner(engine.persona.name))
    spectral_box(
        "SÉANCE CHAMBER",
        [
            f"You are conversing directly with {engine.persona.title}.",
            "The candles are lit. No shell commands are executed here.",
            "Speak your queries to the spirit. Type 'farewell' to leave.",
        ],
        color=color,
    )

    while True:
        try:
            utterance = input(f"\n{BOLD}You:{RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not utterance:
            continue
        if utterance.lower() in {"farewell", "exit", "goodbye", "adios", "quit"}:
            typewriter(f"\n{engine.persona.get_farewell()}\n", color=color)
            break

        reply = engine.converse(utterance)
        sys.stdout.write(f"{color}{BOLD}Spirit:{RESET} ")
        typewriter(reply, color=color)


@cli.command()
@click.argument(
    "shell_type", default="zsh", type=click.Choice(["zsh", "bash", "fish"], case_sensitive=False)
)
def hook(shell_type):
    """Output shell hook script for ~/.zshrc, ~/.bashrc, or config.fish."""
    click.echo(generate_hook(shell_type))


@cli.command()
@click.pass_context
def airgap(ctx):
    """Audit local-first air-gap security and zero external telemetry."""
    engine: GhostEngine = ctx.obj["engine"]
    audit = engine.audit_airgap()

    lines = [
        f"Active Persona: {audit['persona']}",
        f"Inference Engine: {audit['engine_mode']}",
        f"Configured Model: {audit['model_configured']}",
        f"External Telemetry: {'DISABLED (100% Local)' if audit['external_telemetry_disabled'] else 'Active'}",
        f"Can Run Offline: {'YES (Zero Cloud Dependencies)' if audit['can_run_fully_offline'] else 'No'}",
        f"Air-Gap Verification: {'Safe for Air-Gapped Laptops' if audit['airgap_safe'] else 'Warning'}",
    ]
    spectral_box("AIR-GAP & PRIVACY AUDIT", lines, color=SLIME_GREEN)


@cli.command()
@click.pass_context
def doctor(ctx):
    """Perform diagnostic health check of the local system and AI environment."""
    config: HauntedConfig = ctx.obj["config"]
    run_doctor(config)


@cli.group()
def persona():
    """Inspect and list available spectral personas."""
    pass


@persona.command("list")
def persona_list():
    """List all available personas."""
    personas = list_personas()
    lines = []
    for name, p in personas.items():
        lines.append(f"• {BOLD}{p.name}{RESET} [{p.prompt_symbol}] - {p.title}")
    spectral_box("SPECTRAL PERSONAS", lines, color=SPECTRAL_CYAN)


@persona.command("show")
@click.argument("name")
def persona_show(name):
    """Show details and sample lore for a persona."""
    p = get_persona(name)
    color = COLOR_MAP.get(p.name, GHOST_PURPLE)
    lines = [
        f"Name:   {BOLD}{p.name}{RESET}",
        f"Title:  {p.title}",
        f"Glyph:  {p.prompt_symbol}",
        f"Color:  {p.color_name}",
        "",
        "System Lore Prompt:",
        f"{DIM}{p.system_prompt}{RESET}",
    ]
    spectral_box(f"PERSONA: {p.name.upper()}", lines, color=color)


@cli.group()
def config():
    """Inspect or manage configuration settings."""
    pass


@config.command("show")
@click.pass_context
def config_show(ctx):
    """Print the currently resolved configuration."""
    cfg: HauntedConfig = ctx.obj["config"]
    path = get_default_config_path()
    lines = [f"Path: {path} ({'Found' if path.is_file() else 'Default values'})", ""]
    for k, v in cfg.to_dict().items():
        lines.append(f"{k:20}: {v}")
    spectral_box("CURRENT CONFIGURATION", lines, color=MARIGOLD_AMBER)


@config.command("init")
@click.pass_context
def config_init(ctx):
    """Initialize a default configuration file in ~/.config/haunted-shell/config.json."""
    cfg: HauntedConfig = ctx.obj["config"]
    target = save_config(cfg)
    click.echo(f"{SLIME_GREEN}✓ Default configuration written to {target}{RESET}")


@config.command("path")
def config_path():
    """Print the path to the configuration file."""
    click.echo(str(get_default_config_path()))


def main():
    """Primary entry point."""
    cli(obj={})


if __name__ == "__main__":
    main()
