"""html.Button: the app gets how many times it was clicked."""
from dash import Dash, html, Input, Output

app = Dash(__name__)
app.layout = html.Div([
    html.Button("Run", id="run"),          # n_clicks counts the clicks
    html.Pre(id="out"),
])

@app.callback(Output("out", "children"), Input("run", "n_clicks"))
def show(n):
    if n is None:                          # not clicked yet
        return "Press Run"
    return f"clicked {n} time{'s' if n > 1 else ''}"

if __name__ == "__main__":
    app.run(debug=True)
