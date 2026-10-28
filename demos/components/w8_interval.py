"""dcc.Interval: a timer; the app gets a tick every few seconds."""
from datetime import datetime
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)
app.layout = html.Div([
    dcc.Interval(
        id="timer",
        interval=2000,                     # milliseconds between ticks
    ),
    html.Pre(id="out"),
])

@app.callback(Output("out", "children"), Input("timer", "n_intervals"))
def refresh(n):
    # re-read live data here, e.g. the latest prices
    return f"tick {n} at {datetime.now():%H:%M:%S}"

if __name__ == "__main__":
    app.run(debug=True)
