"""Click a point on one chart, see its details in another: dcc.Graph's clickData as a callback Input.

Run:  python 05_click_detail.py   ->  http://127.0.0.1:8050
Click any bond on the left: its one-year spread history appears on the right.
"""
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from data import bonds, history

app = Dash(__name__)

overview = px.scatter(bonds, x="maturity", y="spread", color="rating", hover_name="issuer",
                      custom_data=["cusip"],                # carried with each point, comes back on click
                      title="All bonds: click one")

app.layout = html.Div([
    html.H2("Click a bond to see its history"),
    html.Div([
        dcc.Graph(id="overview", figure=overview, style={"flex": 1}),
        dcc.Graph(id="detail", style={"flex": 1}),
    ], style={"display": "flex"}),
])


@callback(Output("detail", "figure"), Input("overview", "clickData"))
def show_history(click):
    if click is None:                                       # page load: nothing clicked yet
        cusip = bonds.cusip.iloc[0]
    else:
        cusip = click["points"][0]["customdata"][0]         # what the browser sent for the clicked point
    bond = bonds.set_index("cusip").loc[cusip]
    h = history[history.cusip == cusip]
    return px.line(h, x="date", y="spread",
                   title=f"{bond.issuer} {bond.maturity}y ({cusip}): spread history")


if __name__ == "__main__":
    app.run(debug=True)
