# Plotly, Dash & Other Tools

Slides and demo apps for a 30-minute talk on Plotly Dash. The talk goes from a Plotly chart to an interactive app,
shows what happens behind the scenes, and compares Dash with other Python app tools.

**New to Dash?** Start with [`tutorial/`](tutorial/README.md): a step-by-step guide with seven small apps and a
notebook, then building with GitHub Copilot in VS Code (step 9). All the data in this repo is synthetic (random numbers and made-up labels).

## Contents

| path | what |
|---|---|
| `slides/index.html` | the deck (reveal.js, 13 slides plus an appendix of 14 component code slides). Interactive: open it in Chrome. `S` opens the speaker notes, which include timings |
| `slides/build_details.py` | rebuilds the appendix from `demos/components/` and the cards on slides 6 and 7. Re-run it after changing either |
| `slides/plotly_dash_and_other_tools.pdf` | the same deck as a PDF, a backup that works offline (not interactive) |
| `slides/img/` | screenshots of the demos, taken in headless Chrome |
| `demos/run_all.py` | starts every demo app at once, each on its own port, for the slides' **Live app** buttons |
| `demos/data.py` | a synthetic bond universe: 60 bonds from 12 made-up issuers ("Bank A", "Energy B", …) and one year of daily spreads, made in memory |
| `demos/01_plotly_only.py` | Plotly alone: writes `plotly_only.html`. No server |
| `demos/02_hello_dash.py` | the smallest app: a layout with a Plotly chart |
| `demos/03_widgets.py` | a tour of the built-in widgets. One callback echoes every value |
| `demos/04_callback.py` | a dropdown and a checklist drive a sentence and a chart (two Inputs, two Outputs) |
| `demos/05_click_detail.py` | click a point on one chart to see its history in another (`clickData` + `custom_data`) |
| `demos/components/` | one small runnable app per card on slides 6 and 7 (`g*` chart events, `w*` widgets); each runs on its own with `python demos/components/<name>.py` |
| `demos/components/w8b_ticks.py` | live tick data: `dcc.Interval` polls a tick database every second and appends only the new ticks (`extendData`). `tickdb.py` stands in for the database (an in-memory SQLite table fed by a background thread); swap `ticks_since` for your own query |
| `tutorial/README.md` | a step-by-step guide for newcomers: seven small apps (`step1_hello.py` … `step7_matrix.py`), each adding one idea |
| `tutorial/matrix_lines.ipynb` | a notebook: a data matrix with one line per row and one line per column, in a Dash app inside the notebook; edit the table or change the matrix from Python and both charts redraw |
| `.github/copilot-instructions.md` | Dash rules for GitHub Copilot in VS Code, condensed from [Plotly's guide for AI coding assistants](https://dash.plotly.com/ai-coding-assistants) with sources linked, plus a few checked additions. Copy it into your own project |
| `.github/skills/dash-app/` | a Copilot skill for building Dash apps (plan, write, check, report) and `check_app.py`, a checker that needs no browser: ids exist, every callback runs on page load, prints the wiring (`python .github/skills/dash-app/check_app.py app.py`) |
| `.github/prompts/` | reusable Copilot Chat prompts: `/new-dash-app`, `/explain-callbacks`, `/fix-dash-error`. Tutorial step 9 lists the community resources to start from |
| `demos/prompts.md` | the prompts for the VS Code + Copilot demo |
| `demos/.github/copilot-instructions.md` | an example rules file that Copilot follows in `demos/` |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Tested with Dash 4.5.0, dash-ag-grid 35.3.0, Plotly 7.1.0 and pandas 3.1.0.

## Before the talk

```bash
python demos/run_all.py
```

It starts the four demo apps and prints a table when they are all ready. Leave that window open during the talk;
Ctrl+C stops every app.

| slide | demo | address |
|---|---|---|
| 5 | `02_hello_dash.py` | http://127.0.0.1:8052 |
| 7 | `03_widgets.py` | http://127.0.0.1:8053 |
| 8 | `04_callback.py` | http://127.0.0.1:8054 |
| 10 | `05_click_detail.py` | http://127.0.0.1:8055 |

If a port is already taken, it says which one and stops, so you can close whatever is using it. Each app's output
(for example the line demo 04 prints on every change) goes to `demos/.<name>.log`. To show that output live, stop
the launcher and run the demo on its own in a terminal (`cd demos; python 04_callback.py`, on port 8050).

The deck loads reveal.js and plotly.js from a CDN, so it needs internet. Without internet, use the PDF.

## Presenting

- **Open the deck:** open `slides/index.html` in Chrome. Press `F` for full screen and `S` for the speaker notes
  window.
- **Stepping:** each bullet, table row, card and diagram part starts greyed out. Press → or Space to light up the
  next one, and ← to go back. On slide 5 the same keys step through highlighted lines of code; on slide 8 they
  colour each Input with its argument, then each returned value with its Output; on slide 10 they highlight the
  three pieces of the click logic.
- **Slide 3 is a live Plotly chart:** zoom, hover and click the legend. No server is needed.
- **Slides 6 and 7:** the cards' small animations start when each card is stepped in. **Click a card** to open its
  code slide in the appendix: the code of a small app on the left (→ highlights the component, then the callback
  that reads its value) and the animation on the right. **← Back** returns to the same step.
- **Menu:** `M` or the ☰ button (bottom left) lists the 13 talk slides, to jump to one. The code slides are reached by clicking a card.
- **Presenters:** the names are in a comment on the title slide in `slides/index.html`; fill them in and remove the
  comment markers to show them.
- **Live apps:** slides 5, 7, 8 and 10 have a **▶ Live app** button. It opens the running demo over the whole
  slide, and you can click and type in it. **✕ Back to slide** (or moving to another slide) closes it, and the
  arrow keys work again.

## Running order (30 min)

| time | slides | live |
|---|---|---|
| 0:00 | 1–2 title, agenda | |
| 1:00 | 3–4 Plotly alone (live chart), Plotly vs Dash diagram | slide 3 chart |
| 6:00 | 5–7 the smallest app, charts inside Dash, widgets | Live app on 5 and 7 |
| 13:00 | 8–10 a callback, the round trip, click one chart to update another | Live app on 8 and 10 |
| 20:00 | 11 VS Code + Copilot | `demos/prompts.md` |
| 24:00 | 12–13 showcase (your dashboard), other tools | |
