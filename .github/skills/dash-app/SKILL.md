---
name: dash-app
description: Build, change or debug a Plotly Dash app (layout, callbacks, dcc.Graph, widgets, AG Grid tables, dcc.Interval, Dash in a notebook). Use whenever a request asks for a Dash app or dashboard, a new callback or component, or a fix to a Dash error.
---

# Building a Dash app

Follow the rules in `.github/copilot-instructions.md`. This skill is the workflow: plan, write, check, report.
To use it in your own project, copy this folder to `.github/skills/dash-app/` there.

## 1. Plan the wiring before the code

Before writing code, list the components and one line per callback:

```
ids:       sector (Dropdown), rating (Checklist), chart (Graph), summary (P)
callbacks: Input(sector.value), Input(rating.value) -> Output(summary.children), Output(chart.figure)
```

A value the callback needs but that should not trigger it is a `State`. If one callback's Output is another's
Input, they chain; say so. Show this plan to the user when the request is more than a small change.

## 2. Write it

Look for a similar app in the project first and follow its style. Otherwise start from this shape:

```python
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)
app.layout = html.Div([
    html.H1("Title"),
    dcc.Slider(1, 10, 1, value=3, id="n"),
    html.P(id="msg"),
])


@app.callback(Output("msg", "children"), Input("n", "value"))
def show(n):
    return f"You picked {n}."


if __name__ == "__main__":
    app.run(debug=True)
```

The Dash docs have a short, runnable example for almost every component and callback pattern; when unsure of a
component's properties, read its page (any page is available as Markdown: add `.md` to its address, and
https://dash.plotly.com/llms.txt lists them all).

## 3. Check it

```bash
python .github/skills/dash-app/check_app.py my_app.py
```

[check_app.py](./check_app.py) imports the app (no server starts), checks that every callback id is in the
layout, runs each callback once with the starting values, and prints the wiring. It catches typos in ids, a
wrong number of returned values, and exceptions on page load. It cannot click: callbacks with
`prevent_initial_call`, and branches that run only after a click, are not exercised. So also run the app and try
the interaction.

## 4. Report

End with: the files changed, the wiring lines, the command to run the app, and anything not verified.
