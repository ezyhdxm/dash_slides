---
description: Build a new Dash app from a plain description, then check it
agent: agent
argument-hint: what the app should show and do
---
Build a new Dash app in `${input:file:my_app.py}` that does this: ${input:what:what the app should show and do}

Follow the `dash-app` skill ([SKILL.md](../skills/dash-app/SKILL.md)) and the repo rules in
[copilot-instructions.md](../copilot-instructions.md):

1. Before writing code, list the component ids and one wiring line per callback,
   `Input(id.prop), State(id.prop) -> Output(id.prop)`.
2. Write the app in one file, with made-up sample data unless I point to real files.
3. Run `python .github/skills/dash-app/check_app.py ${input:file:my_app.py}` and fix every FAIL.
4. Reply with the wiring lines, the command to run the app, and anything you could not check (for example what
   happens after a click).
