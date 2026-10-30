# Dash: instructions for GitHub Copilot

Rules for writing Plotly Dash apps. Copilot in VS Code adds this file to every chat request when this folder is
open. To use it in your own project, copy it to `.github/copilot-instructions.md` there and trim what you don't
need.

Most rules come from Plotly's guide for AI coding assistants (https://dash.plotly.com/ai-coding-assistants) and
the Dash documentation; each section links its source. The few additions at the end were checked by running
real apps.

## Current Dash API (Plotly's guide)

- Import from `dash` itself: `from dash import Dash, html, dcc, Input, Output, State, callback, no_update`.
  Do not import from `dash.dependencies`, `dash_core_components` or `dash_html_components`.
- Start the app with `app.run(...)`. `app.run_server` no longer exists.
- Do not use `dash_table.DataTable`; use AG Grid (`import dash_ag_grid as dag`, then `dag.AgGrid`).
- Do not use `app.validation_layout`. When the layout is built by callbacks, set
  `suppress_callback_exceptions=True`.

## Callbacks (Plotly's guide; https://dash.plotly.com/advanced-callbacks)

- Give every component that a callback reads or writes a descriptive `id`, unique in the app.
- One callback per interaction.
- For a button-triggered callback, set `prevent_initial_call=True`.
- To skip the whole callback, `raise PreventUpdate`; to leave just one Output unchanged, return `no_update` for it.
- Do not change a callback's arguments in place; build new objects and return them.
- Never use a blocking `time.sleep` loop to wait for data. Poll with `dcc.Interval`
  (https://dash.plotly.com/live-updates) or use a task queue.

## State and data (Plotly's guide; https://dash.plotly.com/sharing-data-between-callbacks)

- Keep per-user state in `dcc.Store` or the URL, never in global variables that callbacks change: the app may
  serve several users and run in several processes.
- Load data inside callbacks rather than at import time, and filter or aggregate in Python before sending it
  to the browser. Keep `dcc.Store` contents small (Plotly suggests under 5 MB).
- Wrap slow outputs in `dcc.Loading`.
- Never put secrets or API keys in the layout or in `dcc.Store`; read them from environment variables.

## Charts (Plotly's guide)

- Use `plotly.express` first; use `plotly.graph_objects` only when express cannot do it.
- Use as few component libraries as possible.

## Additions checked in practice

- A callback's Inputs come first, then its States; the function's arguments arrive in that order, and it must
  return exactly one value per Output, in the order the Outputs are listed.
- `clickData`, `hoverData` and `selectedData` of a `dcc.Graph` are `None` until the user acts; handle `None`.
- A `dcc.Input(type="number")` gives `None` when the box is empty or outside its `min`/`max`; handle `None`.
- In an editable AG Grid, use `Input(grid_id, "cellValueChanged")` to react to edits; a callback that only
  listens to `rowData` does not fire when a cell is edited
  (https://dash.plotly.com/dash-ag-grid/editing-and-callbacks).
- In Jupyter or VS Code notebooks, run the app with `app.run(jupyter_mode="inline")`
  (https://dash.plotly.com/dash-in-jupyter).
- In examples and tests, use made-up sample data generated in the code, not real or confidential data.

## Before saying it works

1. If `.github/skills/dash-app/check_app.py` exists, run `python .github/skills/dash-app/check_app.py <app.py>`
   and fix every FAIL. It imports the app, checks that every callback id exists in the layout, runs each
   callback once as the page load does, and prints the wiring.
2. Start the app and try the interaction that was built.
3. Report the wiring as one line per callback, `Input(id.prop), State(id.prop) -> Output(id.prop)`, and the
   command to run the app.
