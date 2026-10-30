---
description: Explain how a Dash app's callbacks are wired, step by step
agent: ask
---
Explain the Dash app in #file:${input:file:path of the app} to someone who knows Python but is new to Dash.

1. List every callback as one wiring line, `Input(id.prop), State(id.prop) -> Output(id.prop)`.
2. For each, say in one sentence what the user does that triggers it, and what changes on the page.
3. Say which callbacks chain (one's Output is another's Input) and which run when the page loads.
4. Point out anything that breaks the repo rules in [copilot-instructions.md](../copilot-instructions.md).

Do not change any code.
