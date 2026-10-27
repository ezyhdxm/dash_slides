"""A callback: when the dropdown or the checklist changes, the server runs a Python function and the page updates.

Run:  python 04_callback.py   ->  http://127.0.0.1:8050
Watch the terminal: every change prints a line, because the function runs on the server.
Open the browser's DevTools > Network tab: every change is one POST to /_dash-update-component.

The Inputs arrive as the function's arguments in the order they are listed (sector, then ratings);
the returned values fill the Outputs in the order they are listed (summary, then chart).
"""
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from data import bonds

app = Dash(__name__)
sectors = sorted(bonds.sector.unique())
ratings = ["AA", "A", "BBB", "BB"]

app.layout = html.Div([
    html.H1("Corporate bonds"),
    dcc.Dropdown(sectors, "Banks", id="sector", clearable=False),
    dcc.Checklist(ratings, ["A", "BBB"], id="rating", inline=True),
    html.P(id="summary"),
    dcc.Graph(id="chart"),
])


@callback(Output("summary", "children"),
          Output("chart", "figure"),
          Input("sector", "value"),
          Input("rating", "value"))
def update(sector, ratings):
    print(f"server: update(sector={sector!r}, ratings={ratings!r})")   # shows up in the terminal
    d = bonds[(bonds.sector == sector) & bonds.rating.isin(ratings)]
    if d.empty:
        text = f"No {sector} bonds with those ratings"
    else:
        text = f"{len(d)} bonds, avg spread {d.spread.mean():.0f} bp"
    fig = px.scatter(d, x="maturity", y="spread", color="issuer", hover_name="cusip")
    return text, fig


if __name__ == "__main__":
    app.run(debug=True)
