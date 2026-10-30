"""Step 1: the smallest Dash app. A page with a heading and a sentence, no chart yet.

Run:   python step1_hello.py   ->  open http://127.0.0.1:8050 in a browser
Stop:  Ctrl+C in the terminal
"""
from dash import Dash, html

app = Dash(__name__)                   # the app: a small web server plus the page it serves

app.layout = html.Div([                # the page. html.Div is a box that holds other components
    html.H1("Hello Dash"),             # a heading
    html.P("This page was written in Python."),
])

if __name__ == "__main__":
    app.run(debug=True)                # debug=True: reload when you save the file, show errors on the page
