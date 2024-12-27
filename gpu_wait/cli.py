import click
import logging
from .command_runner import CommandRunner


@click.command()
@click.argument("command", nargs=1, required=True)
@click.option("--device", "-d", type=int, help="Specific GPU device ID to wait for")
@click.option(
    "--threshold",
    "-t",
    type=float,
    default=0.9,
    help="Percentage of free memory needed (0.0 to 1.0); default=0.9 means 'wait until >= 90% gpu is free'",
)
@click.option(
    "--interval",
    "-i",
    type=float,
    default=10,
    help="Polling interval in seconds, default=10",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def main(command, device, threshold, interval, verbose):
    """Run a command when GPU resources become available."""
    logging.basicConfig(
        level=logging.INFO if verbose else logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    from .gpu_monitor import GPUMonitor

    monitor = GPUMonitor(threshold, interval)
    runner = CommandRunner(monitor)

    try:
        # Always use shell=True to handle redirections and pipes
        result = runner.run_when_available(command, device, shell=True)
        # Don't echo the output as it's already handled by shell redirection
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        exit(1)
