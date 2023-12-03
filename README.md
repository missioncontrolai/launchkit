# Missioncontrolbot

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

4. Deploy it

```bash
git init
git add .
git commit -m "Initial commit"
```

- Create a new repo on github and push to it.
- Create a Discord bot and save the token.
- Go to https://www.missioncontrolbot.com/ and add your repo.
