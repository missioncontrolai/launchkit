# LaunchControl

LaunchControl is a library for building custom tools for GPTs with tool-use support.
Define your own tools as type annotated functions and LaunchControl will help you test, talk to, and deploy your tools.

LaunchControl is using Pydantic under the hood to validate and parse functions to make them friendly to for AI APIs.

### Getting started

1. Install PDM

2. Create a new project

```bash
mkdir my_project
cd my_project
pdm init --copier gh:loopbackai/missioncontrol-template
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
