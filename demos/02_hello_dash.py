"""The smallest useful Dash app: a page (layout) with a Plotly figure in it.

Run:  python 02_hello_dash.py   ->  http://127.0.0.1:8050
"""
from dash import Dash, html, dcc
import plotly.express as px
from data import bonds

app = Dash(__name__)

fig = px.scatter(bonds, x="maturity", y="spread", color="sector", hover_name="issuer")

app.layout = html.Div([                    # components nest like boxes: code order = page order
    html.H1("Corporate bonds"),
    html.P(f"{len(bonds)} bonds from {bonds.issuer.nunique()} issuers"),
    dcc.Graph(id="chart", figure=fig),     # an id lets the app find this later
])

if __name__ == "__main__":
    app.run(debug=True)
