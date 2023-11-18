import typer


app = typer.Typer()

@app.command()
def dev(actions_path: str = typer.Argument(..., help="Path to actions file. Example app.actions:actions")):
    actions_module, actions_name = actions_path.split(":")
    import importlib
    actions = getattr(importlib.import_module(actions_module), actions_name)
    import asyncio
    from .openai.terminal_tester import talk
    asyncio.run(talk(actions))


if __name__ == "__main__":
    app()