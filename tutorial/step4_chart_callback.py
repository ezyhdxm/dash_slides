"""Step 4: a callback that draws a chart. Pick a series and a window; the chart is redrawn.

Two Inputs: the function gets their values as arguments, in the order the Inputs are listed.
It returns a new figure, which goes into the "figure" property of the dcc.Graph.

Run:  python step4_chart_callback.py   ->  http://127.0.0.1:8050
"""
import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

rng = np.random.default_rng(0)
df = pd.DataFrame(rng.normal(0, 1, (100, 3)).cumsum(axis=0), columns=["A", "B", "C"])
df.index.name = "day"

app = Dash(__name__)
app.layout = html.Div([
    html.H1("Pick a series"),
    dcc.Dropdown(["A", "B", "C"], "A", id="series", clearable=False),
    html.Label("Moving average window (days)"),
    dcc.Slider(1, 20, 1, value=5, id="window"),
    dcc.Graph(id="chart"),                     # no figure yet: the callback makes it
])


@app.callback(Output("chart", "figure"),
              Input("series", "value"),        # -> first argument
              Input("window", "value"))        # -> second argument
def draw(series, window):
    d = pd.DataFrame({series: df[series],
                      f"{window}-day average": df[series].rolling(window).mean()})
    return px.line(d, title=f"Series {series}")


if __name__ == "__main__":
    app.run(debug=True)
