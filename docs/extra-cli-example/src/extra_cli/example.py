import typer

app = typer.Typer(
    help="Example entrypoint for EuXFEL CLI plugin.",
    no_args_is_help=True,
)


@app.command()
def main():
    """Main function in the 'example' namespace package."""
    typer.echo("Hello from 'example'!")


if __name__ == "__main__":
    app()