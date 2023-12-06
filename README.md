# LaunchKit

<p align="center">
  <img src="./docs/images/launchkit_logo_512px.webp" alt="drawing" width="200"/>
</p>

LaunchKit is an open-source library designed to empower developers to efficiently build and deploy custom Python-backed tools that extend the functionality of GPT-based chatbots. It simplifies the transformation of your Python functions into tool specifications that can be understood by AI APIs, using type annotations to generate JSON schemas in the OpenAI format.

This library harnesses Pydantic to interpret function signatures—including arguments, names, and docstrings—creating compatible data models that ultimately facilitate the dynamic generation of JSON schemas. When chatbots invoke these functions, LaunchKit also utilizes Pydantic's validation capabilities to ensure that incoming data adheres to the expected function schemas, promoting accurate and reliable bot operation.

#### With Launchkit, you can:

1. Write Python functions that can be invoked by your chatbot.
2. Talk/test your bot locally in the terminal.
3. Deploy your bot with MissionControl to Discord, Slack and Telegram.

### Toy Example

```python
from launchkit import LaunchKit

def add(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b

# async functions are also supported
async def subtract(a: int, b: int) -> int:
    """Subtracts two numbers."""
    return a - b

tools = LaunchKit([add, subtract])

tools.openai_tools() # list of tools in OpenAI format - ready to be sent to the API.
```

Talk with your bot locally in the terminal:

```bash
launchkit module_name:tools
```

### Getting started

1. Install [PDM](https://pdm-project.org/latest/#installation)

2. Create a new project

```bash
mkdir my_project
cd my_project
pdm init --copier gh:missioncontrolai/template
pdm install
```

3. Test it out

```bash
pdm test # run tests
pdm dev # talk with your bot
```

4. Deploy it (with MissionControl)

```bash
git init
git add .
git commit -m "Initial commit"
```

- Create a new repo on github and push to it.
- Create a Discord bot and save the token.
- Go to https://www.missioncontrolbot.com/ and add your repo.
