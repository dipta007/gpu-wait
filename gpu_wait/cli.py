import click
import logging
from .command_runner import CommandRunner


@click.command()
@click.argument("command", nargs=-1, required=True)
@click.option("--device", "-d", type=int, help="Specific GPU device ID to wait for")
@click.option(
    "--threshold",
    "-t",
    type=float,
    default=0.9,
    help="Memory usage threshold (0.0 to 1.0)",
)
@click.option(
    "--interval", "-i", type=float, default=1.0, help="Polling interval in seconds"
)
@click.option("--shell/--no-shell", default=False, help="Run command in shell mode")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def main(command, device, threshold, interval, shell, verbose):
    """Run a command when GPU resources become available."""
    logging.basicConfig(
        level=logging.INFO if verbose else logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    from .gpu_monitor import GPUMonitor

    monitor = GPUMonitor(threshold, interval)
    runner = CommandRunner(monitor)

    try:
        result = runner.run_when_available(
            list(command) if not shell else " ".join(command), device, shell=shell
        )
        click.echo(result.stdout)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        exit(1)
