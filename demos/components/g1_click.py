"""dcc.Graph clickData: click a point and the app learns which point."""
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

fig = px.scatter(x=[2, 3, 5, 7, 10, 20, 30],          # maturity
                 y=[80, 95, 120, 140, 165, 210, 240])  # spread

app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id="chart", figure=fig),
    html.Pre(id="out"),
])

@app.callback(Output("out", "children"), Input("chart", "clickData"))
def show(click):
    if click is None:                      # nothing clicked yet
        return "Click a point"
    p = click["points"][0]                 # the clicked point
    return f"maturity {p['x']}, spread {p['y']}"

if __name__ == "__main__":
    app.run(debug=True)
