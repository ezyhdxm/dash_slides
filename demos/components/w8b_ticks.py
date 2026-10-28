"""dcc.Interval + a tick database: fetch the new ticks, append them."""
from datetime import datetime
from dash import Dash, html, dcc, Input, Output, State, no_update
import plotly.graph_objects as go
from tickdb import ticks_since         # swap in your own DB query

app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id="chart",
              figure=go.Figure(go.Scatter(x=[], y=[], mode="lines"))),
    dcc.Interval(id="timer", interval=1000),   # ask every second
    dcc.Store(id="last_ts", data=0),           # newest tick on screen
])

@app.callback(Output("chart", "extendData"), Output("last_ts", "data"),
              Input("timer", "n_intervals"), State("last_ts", "data"))
def add_ticks(n, last_ts):
    rows = ticks_since(last_ts)            # only the ticks not yet shown
    if not rows:
        return no_update, no_update
    ts, price = zip(*rows)
    x = [datetime.fromtimestamp(t) for t in ts]
    new = dict(x=[x], y=[list(price)])     # one list per trace
    return (new, [0], 2000), ts[-1]        # trace 0, keep last 2000

if __name__ == "__main__":
    app.run(debug=True)
