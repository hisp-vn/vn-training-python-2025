import typer

app = typer.Typer()


@app.command()
def hello(name: str, age: int = typer.Option(None, help="Your age")):
    """
    Say hello to someone, and optionally include their age.
    """
    # Basic greeting
    greeting = f"Hello, {name}!"

    if age is not None:
        greeting += f" You are {age} years old."

    typer.echo(greeting)


if __name__ == "__main__":
    app()
