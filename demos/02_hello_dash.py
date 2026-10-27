"""The smallest useful Dash app: a page (layout) with a Plotly figure in it.

Run:  python 02_hello_dash.py   ->  http://127.0.0.1:8050
"""
from dash import Dash, html, dcc
import plotly.express as px
from data import bonds

app = Dash(__name__)                       # a Flask server + the Dash front end

fig = px.scatter(bonds, x="maturity", y="spread", color="sector", hover_name="issuer")

app.layout = html.Div([                    # the page is a tree of components
    html.H1("Corporate bonds"),
    html.P(f"{len(bonds)} bonds from {bonds.issuer.nunique()} issuers"),
    dcc.Graph(figure=fig),                 # any Plotly figure goes in a dcc.Graph
])

if __name__ == "__main__":
    app.run(debug=True)
