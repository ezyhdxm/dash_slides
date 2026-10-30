"""Step 2: put a Plotly chart on the page with dcc.Graph.

Run:  python step2_chart.py   ->  http://127.0.0.1:8050
The chart is built once, when the script starts. Zoom and hover work, but nothing on the page changes it yet.
"""
import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# made-up data: three random walks of 100 days
rng = np.random.default_rng(0)
df = pd.DataFrame(rng.normal(0, 1, (100, 3)).cumsum(axis=0), columns=["A", "B", "C"])
df.index.name = "day"

fig = px.line(df, title="Three made-up series")     # an ordinary Plotly figure: one line per column

app = Dash(__name__)
app.layout = html.Div([
    html.H1("A chart in Dash"),
    dcc.Graph(figure=fig),             # dcc.Graph shows a Plotly figure on the page
])

if __name__ == "__main__":
    app.run(debug=True)
