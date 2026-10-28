"""dcc.Graph selectedData: which points are inside a box or lasso."""
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

fig = px.scatter(x=[2, 3, 5, 7, 10, 20, 30],          # maturity
                 y=[80, 95, 120, 140, 165, 210, 240])  # spread
fig.update_layout(dragmode="select")   # drag draws a box, not a zoom

app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(
        id="chart",
        figure=fig,
        selectedData=None,        # filled in when a box is drawn
    ),
    html.Pre(id="out"),
])

@app.callback(Output("out", "children"), Input("chart", "selectedData"))
def show(selected):
    if not selected:                       # nothing selected yet
        return "Drag a box around some points"
    xs = [p["x"] for p in selected["points"]]   # every point inside
    return f"{len(xs)} points, maturities {xs}"

if __name__ == "__main__":
    app.run(debug=True)
