"""dcc.Graph relayoutData: the visible range after a zoom or pan."""
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

fig = px.scatter(x=[2, 3, 5, 7, 10, 20, 30],          # maturity
                 y=[80, 95, 120, 140, 165, 210, 240])  # spread

app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(
        id="chart",
        figure=fig,
        relayoutData=None,        # filled in on every zoom or pan
    ),
    html.Pre(id="out"),
])

@app.callback(Output("out", "children"), Input("chart", "relayoutData"))
def show(layout):
    if not layout or "xaxis.range[0]" not in layout:  # no zoom yet
        return "Drag a box to zoom in"
    lo, hi = layout["xaxis.range[0]"], layout["xaxis.range[1]"]
    return f"showing maturities {lo:.1f} to {hi:.1f}"

if __name__ == "__main__":
    app.run(debug=True)
