# Dash in 30 Minutes

Slides and demo apps for a 30-minute talk on Plotly Dash. The talk goes from a Plotly chart to an interactive app,
and shows what happens behind the scenes.

## Contents

| path | what |
|---|---|
| `slides/index.html` | the deck (reveal.js). Open it in a browser. `S` opens the speaker notes, which include timings |
| `slides/dash_in_30_minutes.pdf` | the same deck as a PDF, a backup that works offline |
| `slides/img/` | screenshots of the demos, taken in headless Chrome |
| `slides/captured/` | the real request and response bodies shown on slides 12 and 15, recorded from Chrome |
| `demos/data.py` | a synthetic bond universe: 60 bonds and one year of daily spreads, made in memory |
| `demos/01_plotly_only.py` | Plotly alone: writes `plotly_only.html`. No server |
| `demos/02_hello_dash.py` | the smallest app: a layout with a Plotly figure |
| `demos/03_widgets.py` | a tour of the built-in widgets. One callback echoes every value |
| `demos/04_callback.py` | a dropdown drives a sentence and a chart. Each pick prints a line in the terminal |
| `demos/05_drilldown.py` | click a point on one chart to see its history in another (`clickData` + `custom_data`) |
| `demos/06_full_app.py` | the showcase: filters, KPIs, AG Grid, drill-down from chart or grid, live updates, CSV download |
| `demos/prompts.md` | the prompts for the VS Code + Copilot demo |
| `demos/.github/copilot-instructions.md` | the rules Copilot follows in `demos/` |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd demos
python 04_callback.py                                  # then open http://127.0.0.1:8050
```

Run each demo from inside `demos/`, so that `from data import ...` and `assets/` resolve. Only one app can use
port 8050 at a time, so stop one demo (Ctrl+C) before starting the next. The demos were tested with Dash 4.4.1,
Plotly 6.8.0, pandas 3.0.6 and dash-ag-grid 35.3.0.

The deck loads reveal.js from a CDN, so it needs internet. Without internet, use the PDF.

## Running order (30 min)

| time | slides | demo |
|---|---|---|
| 0:00 | 1–2 title, plan | |
| 1:15 | 3–5 Plotly alone vs Dash (the architecture diagram) | `01` |
| 5:15 | 6–9 layout, figures, widgets | `02`, `03` |
| 10:15 | 10–13 callbacks, the round trip, the real JSON, the toolkit | `04` with DevTools → Network open |
| 16:15 | 14–15 click to drill down, behind the scenes | `05` |
| 20:15 | 16–17 VS Code + Copilot | prompts 1–3 from `demos/prompts.md` |
| 24:15 | 18–19 showcase | `06` |
| 29:00 | 20 next steps, questions | |

On slides 6, 10 and 14, the arrow keys step through highlighted lines of the code.
