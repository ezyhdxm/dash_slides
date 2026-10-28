"""dcc.Dropdown: pick from a list; the app gets the chosen item."""
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(
        id="sector",
        options=["Banks", "Energy", "Tech"],
        value="Banks",                     # chosen at the start
        # multi=True,          # pick several: value becomes a list
    ),
    html.Pre(id="out"),
])

@app.callback(Output("out", "children"), Input("sector", "value"))
def show(sector):
    return f"sector = {sector!r}"

if __name__ == "__main__":
    app.run(debug=True)
