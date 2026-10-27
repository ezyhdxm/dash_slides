"""Plotly on its own: Python builds the figure once, writes it to HTML, and is gone.

Run:  python 01_plotly_only.py   ->  open plotly_only.html in a browser
Zoom, pan and hover all work, because they run in the browser's JavaScript.
But nothing can ask Python a new question: to show another sector you re-run this script.
"""
import plotly.express as px
from data import bonds

fig = px.scatter(bonds, x="maturity", y="spread", color="sector", hover_name="issuer",
                 title="Corporate bonds: spread vs maturity")
fig.write_html("plotly_only.html", include_plotlyjs="cdn")
print("wrote plotly_only.html")
