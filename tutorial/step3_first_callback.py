"""Step 3: the first callback. Move the slider and the sentence under it changes.

A callback is a Python function that Dash calls for you whenever an input changes:
    Input("n", "value")         watch the value of the component whose id is "n"
    Output("msg", "children")   put the returned value inside the component whose id is "msg"

Run:  python step3_first_callback.py   ->  http://127.0.0.1:8050
Watch the terminal: every move of the slider prints a line, because the function runs in Python.
"""
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)
app.layout = html.Div([
    html.H1("My first callback"),
    dcc.Slider(1, 10, 1, value=3, id="n"),     # min, max, step, starting value; the id names it
    html.P(id="msg"),                          # empty: the callback fills it
])


@app.callback(Output("msg", "children"), Input("n", "value"))
def show(n):
    print("show() called with n =", n)
    return f"You picked {n}. Its square is {n * n}."


if __name__ == "__main__":
    app.run(debug=True)
