"""
Command line interface for haunted-shell: The Ghost in the Machine.
Hacktoberfest Week 4 Challenge.
"""

import os
import sys
import subprocess
import click

from .ui import (
    BOLD, RESET, DIM, GHOST_PURPLE, MARIGOLD_AMBER, SLIME_GREEN,
    BLOOD_RED, SPECTRAL_CYAN, DEATH_GRAY, typewriter, get_banner, spectral_box
)
from .ghost import GhostEngine
from .exorcist import Exorcist
from .shell_hook import generate_hook


COLOR_MAP = {
    "poltergeist": GHOST_PURPLE,
    "calavera": MARIGOLD_AMBER,
    "unix-elder": SLIME_GREEN
}


@click.group(invoke_without_command=True)
@click.option("--persona", "-p", default="poltergeist",
              type=click.Choice(["poltergeist", "calavera", "unix-elder"], case_sensitive=False),
              help="Spectral persona possessing the shell.")
@click.option("--offline", "-o", is_flag=True, default=False,
              help="Force 100% offline mode (bypasses any local/external LLM probes).")
@click.option("--model", "-m", default="gemma2:2b",
              help="Local open-weight model name (e.g. gemma2:2b, llama3.2).")
@click.option("--glitch", "-g", default=1, type=int,
              help="Glitch/zalgo text intensity level (0 to 3).")
@click.pass_context
def cli(ctx, persona, offline, model, glitch):
    """👻 haunted-shell: A terminal possessed by open-source AI."""
    ctx.ensure_object(dict)
    ctx.obj["persona"] = persona.lower()
    ctx.obj["offline"] = offline
    ctx.obj["model"] = model
    ctx.obj["glitch"] = glitch
    ctx.obj["engine"] = GhostEngine(
        persona_name=persona.lower(),
        model_name=model,
        force_offline=offline,
        glitch_intensity=glitch
    )

    if ctx.invoked_subcommand is None:
        ctx.invoke(shell)


@cli.command()
@click.pass_context
def shell(ctx):
    """Enter the possessed interactive terminal REPL."""
    persona = ctx.obj["persona"]
    engine = ctx.obj["engine"]
    color = COLOR_MAP.get(persona, GHOST_PURPLE)

    # Print spooky intro banner
    print(get_banner(persona))
    status_mode = "Offline Local Neural/Persona Engine" if engine.force_offline or not engine.has_local_model else f"Local Open-Weight Model [{engine.model_name}]"
    print(f"{DIM}👻 Spirit: {BOLD}{engine.persona.title}{RESET}")
    print(f"{DIM}🔒 Air-gap Security: {SLIME_GREEN}Verified Local-Only{RESET}{DIM} ({status_mode}){RESET}")
    print(f"{DIM}💡 Type regular commands (e.g. ls, git status, date). Type 'exit' to escape.{RESET}\n")

    prompt_symbol = "💀" if persona == "calavera" else ("#" if persona == "unix-elder" else "👻")

    while True:
        cwd_short = os.path.basename(os.getcwd()) or "/"
        prompt_str = f"{color}[{cwd_short}] {prompt_symbol} {RESET}"
        try:
            cmd = input(prompt_str).strip()
        except (KeyboardInterrupt, EOFError):
            print()
            typewriter("\n...The spirit dissipates back into swap memory. Rest well, mortal...", color=color)
            break

        if not cmd:
            continue

        if cmd in {"exit", "quit", ":q"}:
            farewell = engine.haunt_command("exit", exit_code=0)
            typewriter(f"\n{farewell}\n", color=color)
            break

        if cmd.startswith("cd ") or cmd == "cd":
            target = cmd[3:].strip() or os.path.expanduser("~")
            try:
                os.chdir(os.path.expanduser(target))
                exit_code = 0
            except Exception as e:
                print(f"cd: {e}", file=sys.stderr)
                exit_code = 1
        else:
            try:
                # Execute user command directly in host shell
                res = subprocess.run(cmd, shell=True)
                exit_code = res.returncode
            except Exception as e:
                print(f"Error executing command: {e}", file=sys.stderr)
                exit_code = 127

        # Spectral response
        whisper = engine.haunt_command(cmd, exit_code=exit_code)
        print()
        typewriter(f"  {prompt_symbol}  {whisper}", color=color)
        print()


@cli.command()
@click.argument("command_str")
@click.option("--exit-code", "-e", default=0, type=int, help="Exit code of the executed command.")
@click.pass_context
def whisper(ctx, command_str, exit_code):
    """Whisper spooky commentary on a command (ideal for shell hooks)."""
    engine = ctx.obj["engine"]
    persona = ctx.obj["persona"]
    color = COLOR_MAP.get(persona, GHOST_PURPLE)

    comment = engine.haunt_command(command_str, exit_code=exit_code)
    prompt_symbol = "💀" if persona == "calavera" else ("#" if persona == "unix-elder" else "👻")
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
        success = exorcist.exorcise(banish, force=force)
        if success:
            click.echo(f"{SLIME_GREEN}✓ Spirit {banish} has been banished back into the void.{RESET}")
        else:
            click.echo(f"{BLOOD_RED}✗ The spirit resisted or was already dispersed.{RESET}")
        return

    spirits = exorcist.scan_spirits()
    exorcist.render_spectral_report(spirits)
    if spirits:
        click.echo(f"\n{DIM}To banish a restless PID, run: {BOLD}haunt exorcise --banish <PID>{RESET}")


@cli.command()
@click.pass_context
def seance(ctx):
    """Hold an interactive séance dialogue with the spirit."""
    persona = ctx.obj["persona"]
    engine = ctx.obj["engine"]
    color = COLOR_MAP.get(persona, GHOST_PURPLE)

    print(get_banner(persona))
    spectral_box("SÉANCE CHAMBER", [
        f"You are conversing directly with {engine.persona.title}.",
        "The candles are lit. No shell commands are executed here.",
        "Speak your queries to the spirit. Type 'farewell' to leave."
    ], color=color)

    while True:
        try:
            utterance = input(f"\n{BOLD}You:{RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not utterance:
            continue
        if utterance.lower() in {"farewell", "exit", "goodbye", "adios"}:
            typewriter("\n...The candle flickers out. The spirit bids you peace...", color=color)
            break

        reply = engine.converse(utterance)
        sys.stdout.write(f"{color}{BOLD}Spirit:{RESET} ")
        typewriter(reply, color=color)


@cli.command()
@click.argument("shell_type", default="zsh", type=click.Choice(["zsh", "bash"], case_sensitive=False))
def hook(shell_type):
    """Output shell hook script for ~/.zshrc or ~/.bashrc."""
    click.echo(generate_hook(shell_type))


@cli.command()
@click.pass_context
def airgap(ctx):
    """Audit local-first air-gap security and zero external telemetry."""
    engine = ctx.obj["engine"]
    audit = engine.audit_airgap()

    lines = [
        f"Active Persona: {audit['persona']}",
        f"Inference Engine: {audit['engine_mode']}",
        f"Configured Model: {audit['model_configured']}",
        f"External Telemetry: {'DISABLED (100% Local)' if audit['external_telemetry_disabled'] else 'Active'}",
        f"Can Run Offline: {'YES (Zero Cloud Dependencies)' if audit['can_run_fully_offline'] else 'No'}",
        f"Hardware Isolation: {'Safe for Air-gapped Laptops' if audit['airgap_safe'] else 'Warning'}"
    ]
    spectral_box("AIR-GAP & PRIVACY AUDIT", lines, color=SLIME_GREEN)


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
