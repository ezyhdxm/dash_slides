"""dcc.Checklist (tick several) and dcc.RadioItems (exactly one)."""
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)
app.layout = html.Div([
    dcc.Checklist(
        id="ratings",
        options=["AA", "A", "BBB"],
        value=["A", "BBB"],    # a list: several can be ticked
    ),
    dcc.RadioItems(
        id="measure",
        options=["spread", "coupon"],
        value="spread",        # one value: exactly one is chosen
    ),
    html.Pre(id="out"),
])

@app.callback(Output("out", "children"),
              Input("ratings", "value"), Input("measure", "value"))
def show(ratings, measure):
    return f"ratings = {ratings}\nmeasure = {measure!r}"

if __name__ == "__main__":
    app.run(debug=True)
