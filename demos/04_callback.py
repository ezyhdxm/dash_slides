"""A callback: when the dropdown's value changes, the server runs a Python function and the page updates.

Run:  python 04_callback.py   ->  http://127.0.0.1:8050
Watch the terminal: every pick prints a line, because the function runs on the server.
Open the browser's DevTools > Network tab: every pick is one POST to /_dash-update-component.
"""
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from data import bonds

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Corporate bonds"),
    dcc.Dropdown(sorted(bonds.sector.unique()), "Banks", id="sector", clearable=False),
    html.P(id="summary"),
    dcc.Graph(id="chart"),
])


@callback(Output("summary", "children"), Output("chart", "figure"),
          Input("sector", "value"))
def update(sector):
    print(f"server: update(sector={sector!r})")          # shows up in the terminal, not the browser
    d = bonds[bonds.sector == sector]
    text = f"{len(d)} {sector} bonds, average spread {d.spread.mean():.0f} bp"
    fig = px.scatter(d, x="maturity", y="spread", color="issuer", hover_name="cusip")
    return text, fig


if __name__ == "__main__":
    app.run(debug=True)
