# Standard
# None

# Pip
import typer

from adversaries.settings.constants.natural_order_group import NaturalOrderGroup

# Custom
app = typer.Typer(
    no_args_is_help=True,
    name="app",
    add_completion=False,
    cls=NaturalOrderGroup,
)


@app.command()
def zee():
    """
    Goodbye
    """
    # Your code herecl
    typer.echo("Hello, Typer!")


@app.command()
def goodbye():
    """
    Goodbye
    """
    # Your code here
    typer.echo("Hello, Typer!")


@app.command()
def hello():
    """
    Hello
    """
    # Your code here
    typer.echo("Hello, Typer!")


if __name__ == "__main__":
    app()
