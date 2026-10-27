# Prompts for the VS Code + Copilot demo

Before you start: open the `demos/` folder itself in VS Code, so Copilot reads `.github/copilot-instructions.md`
(it only looks at the workspace root). Use Copilot Chat in Agent mode, so it can create and run files.

The two prompts on the slide:
> Build a Dash app for the bonds data: filter by sector, show spread vs maturity, and let me click a bond to see
> its history.

> Add a sector dropdown (id `sector`, default Banks). When it changes, filter the scatter and show the count and
> average spread under it. When I click a point, use `custom_data` to get the cusip and plot its history from
> `history` in a second chart.

Or build it up one step at a time:

Each prompt below builds on the one before it. After each one, run the file and look at the result
before you ask for the next change.

## 1. A page with a chart (about 1 minute)
> Create `my_app.py`: a Dash app showing a scatter of `bonds` with maturity on x, spread on y, colored by sector,
> with the issuer on hover. Add a title above the chart.

## 2. Add a widget and a callback
> Add a dropdown of sectors above the chart, defaulting to "Banks", and a checklist of ratings (AA, A, BBB, BB)
> with A and BBB ticked. When either changes, show only the matching bonds, and show a sentence under them with
> the count and the average spread.

## 3. Drill down on click
> When I click a bond on the scatter, show its spread history from `history` in a second chart to the right.
> Use `custom_data` to carry the cusip. Before anything is clicked, show a hint instead of an empty chart.

## 4. Explain it back (good for learning)
> Explain what happens, step by step, between my click on the scatter and the second chart updating.
> Mention which HTTP request is sent and what is in it.

## 5. Fix an error (a deliberate mistake)
Rename the id of the second chart in the layout only, run the app, then paste the red error box text:
> I get this error in the Dash dev tools: <paste>. Fix it.

## Tips
- Ask for one feature per prompt. Run the app after each one.
- When it uses an old API (`dash_core_components`, `app.run_server`), say "use the Dash 3 API". The
  instructions file prevents most of these.
- Ask "which Input/Output pairs does this app have?" to check the wiring before you read the code.
- Keep `debug=True` while developing: errors show in the browser, and the app reloads when you save the file.
