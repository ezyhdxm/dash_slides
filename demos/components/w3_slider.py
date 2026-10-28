"""dcc.Slider (one number) and dcc.RangeSlider (a low and a high)."""
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)
app.layout = html.Div([
    dcc.Slider(
        id="max_spread",
        min=0, max=400, step=10,
        value=200,                         # one number
    ),
    dcc.RangeSlider(
        id="maturity",
        min=0, max=30, step=1,
        value=[2, 10],                     # [low, high]
    ),
    html.Pre(id="out"),
])

@app.callback(Output("out", "children"),
              Input("max_spread", "value"), Input("maturity", "value"))
def show(max_spread, maturity):
    return f"max spread = {max_spread}\nmaturity = {maturity}"

if __name__ == "__main__":
    app.run(debug=True)
