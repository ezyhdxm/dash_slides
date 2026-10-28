"""dcc.Input: type text or a number; the app gets what was typed."""
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)
app.layout = html.Div([
    dcc.Input(
        id="issuer",
        type="text",           # or "number"
        placeholder="issuer name",
        debounce=True,         # send on Enter, not on every key
    ),
    html.Pre(id="out"),
])

@app.callback(Output("out", "children"), Input("issuer", "value"))
def show(issuer):
    return f"issuer = {issuer!r}"

if __name__ == "__main__":
    app.run(debug=True)
