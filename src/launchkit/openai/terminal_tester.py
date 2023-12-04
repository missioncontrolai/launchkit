import datetime
import json
import os
from typing import TypedDict, Union

import sys
from rich.console import Console
from openai import AsyncOpenAI
from openai.types.chat.chat_completion_tool_message_param import (
    ChatCompletionToolMessageParam,
)
from openai.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam,
)
from openai.types.chat.chat_completion_system_message_param import (
    ChatCompletionSystemMessageParam,
)
from openai.types.chat.chat_completion_function_message_param import (
    ChatCompletionFunctionMessageParam,
)
from openai.types.chat.chat_completion_assistant_message_param import (
    ChatCompletionAssistantMessageParam,
)


from ..launchkit import LaunchKit

BOT_NAME = os.environ.get("BOT_NAME", "jarvis")

ChatCompletionMessageParam = Union[
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionFunctionMessageParam,
]


openai_client = AsyncOpenAI()
console = Console()


class Thread(TypedDict):
    log: list[ChatCompletionMessageParam]


async def chat(thread: Thread, actions: LaunchKit) -> Thread:
    completion = await openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            *thread["log"],
        ],
        tools=actions.openai_tools(),  # type: ignore
    )
    msg = completion.choices[0].message
    if not msg.tool_calls:
        return {"log": [{"role": "assistant", "content": msg.content}]}
    thread_additions: Thread = {
        "log": [
            {
                "role": "assistant",
                "content": msg.content,
                "tool_calls": [t.model_dump() for t in msg.tool_calls],  # type: ignore
            }
        ]
    }
    for tool in msg.tool_calls or []:
        data = await actions.call_func(
            tool.function.name, **json.loads(tool.function.arguments)
        )
        thread_additions["log"].append(
            {
                "role": "tool",
                "tool_call_id": tool.id or "",
                "content": json.dumps(data),
            }
        )
    return thread_additions


async def talk(actions: LaunchKit) -> None:
    thread: Thread = {"log": []}
    console.print("\n🚀🚀🚀 [magenta bold italic]LaunchKit Terminal Tester[/] 🚀🚀🚀\n")
    system_message = f"""
You are {BOT_NAME}, an AI developed for tool use.
Help with any request.
Current timestamp: {datetime.datetime.now().isoformat()}
Be concise and professional.
"""
    thread["log"].append({"role": "system", "content": system_message})
    while True:
        try:
            user_input = console.input("[bold blue]User:[/] ")
            thread["log"].append({"role": "user", "content": user_input})
            tadds: Thread = {"log": []}
            for _ in range(10):
                tadds = await chat(thread, actions)
                for msg in tadds["log"]:
                    if msg["role"] == "tool":
                        console.print(f"[bold green]Tool:[/] {msg['content']}")
                    elif msg["content"]:
                        console.print(
                            f"[bold yellow]{msg['role'].capitalize()}:[/] {msg['content']}"
                        )
                thread["log"] = [*thread["log"], *tadds["log"]]
                if tadds["log"][-1]["role"] == "tool":
                    pass
                else:
                    break
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit()
        except EOFError:
            print("\nGoodbye!")
            sys.exit()
