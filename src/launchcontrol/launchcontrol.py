
import inspect
from typing import Any, Callable, Coroutine, Literal, TypedDict
from asyncer import asyncify

from pydantic import create_model

class FunctionSchema(TypedDict):
    name: str
    description: str
    parameters: dict[str, Any]

class ToolSchema(TypedDict):
    type: Literal["function"]
    function: FunctionSchema

def get_func_model(f):
    kw = {
        n: (o.annotation, ... if o.default == inspect.Parameter.empty else o.default)
        for n, o in inspect.signature(f).parameters.items()
    }
    return create_model(f"Input for `{f.__name__}`", **kw)  # type: ignore


def get_func_schema(f) -> FunctionSchema:
    s = get_func_model(f).schema()
    return {
        "name": f.__name__,
        "description": (f.__doc__ or "").strip(),
        "parameters": s
    }

class LaunchControl:
    def __init__(self, funcs: list[Callable| Coroutine]) -> None:
        self._funcs = {
            f.__name__: f for f in funcs
        }

    def openai_tools(self) -> list[ToolSchema]:
        return [
        {"type": "function", "function": get_func_schema(f)} for f in self._funcs.values()
    ]

    async def call_func(self, func_name: str, **kwargs) -> Any:
        f = self._funcs[func_name]
        s = get_func_model(f)
        p = s(**kwargs)
        if inspect.iscoroutinefunction(f):
            return await f(**dict(p))
        else:
            return await asyncify(f)(**dict(p)) # type: ignore


