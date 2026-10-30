"""Step 5: wait for a button. Change the boxes, then press Generate; the chart changes only on the press.

    Input  runs the callback when it changes: here the button's n_clicks (how many times it was pressed)
    State  passes a value in without running the callback when it changes: here the two number boxes
    PreventUpdate  stops the callback without changing anything on the page

Run:  python step5_button_state.py   ->  http://127.0.0.1:8050
"""
import numpy as np
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate

app = Dash(__name__)
app.layout = html.Div([
    html.H1("Generate a random path"),
    html.Label("Points"), dcc.Input(id="points", type="number", value=50, min=10, max=500, style={"width": 160}),
    html.Label("Volatility"), dcc.Input(id="vol", type="number", value=1.0, min=0.1, step=0.1, style={"width": 160}),
    html.Button("Generate", id="go", n_clicks=0),
    dcc.Graph(id="chart"),
])


@app.callback(Output("chart", "figure"),
              Input("go", "n_clicks"),
              State("points", "value"),
              State("vol", "value"))
def generate(n_clicks, points, vol):
    if points is None or vol is None:          # a box is empty or out of range
        raise PreventUpdate
    rng = np.random.default_rng(n_clicks)      # new numbers on every press
    y = rng.normal(0, vol, int(points)).cumsum()
    return px.line(y=y, title=f"{points} points, volatility {vol} (button presses: {n_clicks})")


if __name__ == "__main__":
    app.run(debug=True)
