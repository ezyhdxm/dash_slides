"""Step 6: click a chart to drive another chart. Click a bar to see that series day by day.

A dcc.Graph has properties that the browser fills in when you use the chart. clickData holds the point
you clicked last (None before the first click). The box under the charts prints it, so you can see its shape.

Run:  python step6_click_chart.py   ->  http://127.0.0.1:8050
"""
import json

import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

rng = np.random.default_rng(1)
df = pd.DataFrame(rng.normal(0, 1, (100, 5)).cumsum(axis=0), columns=["A", "B", "C", "D", "E"])
df.index.name = "day"
last = df.iloc[-1].round(2).rename("last value").reset_index().rename(columns={"index": "series"})

app = Dash(__name__)
app.layout = html.Div([
    html.H1("Click a bar"),
    dcc.Graph(id="bars", figure=px.bar(last, x="series", y="last value", title="Last value of each series"),
              style={"height": 320}),
    dcc.Graph(id="detail", style={"height": 320}),
    html.Pre(id="raw"),
])


@app.callback(Output("detail", "figure"),
              Output("raw", "children"),
              Input("bars", "clickData"))
def detail(click):
    series = "A" if click is None else click["points"][0]["x"]     # the clicked bar's x value
    fig = px.line(df[series], title=f"Series {series}, day by day")
    return fig, "clickData = " + json.dumps(click, indent=2)


if __name__ == "__main__":
    app.run(debug=True)
