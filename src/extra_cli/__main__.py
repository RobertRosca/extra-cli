from importlib import metadata
from typing import Annotated
import sys

from structlog import get_logger
import structlog
import typer

log = get_logger(__name__)

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main(verbose: Annotated[int, typer.Option("--verbose", "-v", count=True)] = 0):
    """Main entrypoint for EuXFEL CLI."""
    if verbose > 3:
        verbose = 3

    log_level = 40 - (verbose * 10)

    structlog.configure_once(
        wrapper_class=structlog.make_filtering_bound_logger(log_level)
    )


def load_plugins():
    """Dynamically load plugins from entry points."""

    # Logging has not been configured yet, so parse argv and set it up manually just
    # for this function. Treat -vvvv as trace, one lever more verbose than debug.
    if any(["-vvvv" in arg for arg in sys.argv]):
        _log = lambda *args, **kwargs: log.debug(*args, **kwargs)  # noqa: E731
    else:
        _log = lambda *args, **kwargs: None  # noqa: E731

    for entry_point in metadata.entry_points(group="extra_cli.plugin"):
        _log("Found plugin", name=entry_point.name, entry_point=entry_point)
        plugin = entry_point.load()
        _log("Loaded plugin", plugin=plugin)
        app.add_typer(plugin, name=entry_point.name)


load_plugins()


if __name__ == "__main__":
    app()
