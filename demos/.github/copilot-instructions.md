# Instructions for Copilot in this folder

These are Plotly Dash apps for a talk. When you write or change code here:

- Use Dash 3 or later. Import with `from dash import Dash, html, dcc, callback, Output, Input, State, ctx`.
  Do NOT use the old packages `dash_core_components` / `dash_html_components`, and prefer `@callback` over `@app.callback`.
- Put the whole app in one file. Start it with `app.run(debug=True)` under `if __name__ == "__main__":`.
  (`app.run_server` is removed in Dash 3.)
- Get the data with `from data import bonds, history`. Do not invent new data files.
  `bonds` has one row per bond: cusip, issuer, sector, rating, maturity, coupon, spread, amount.
  `history` has the daily spread per bond: date, cusip, spread.
- Use `plotly.express` for figures. Give every component that a callback reads or writes an explicit `id`.
- Keep callbacks as plain functions with no global state. Keep per-user state in `dcc.Store`.
- After a change, tell me which ids and props each callback connects, as `Input(id.prop) -> Output(id.prop)`.
