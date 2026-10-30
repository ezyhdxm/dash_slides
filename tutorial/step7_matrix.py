"""Step 7: a data matrix and two line charts that follow it. Edit a cell, or press the button, and both redraw.

    top chart     one line per ROW    (x axis = the columns)
    bottom chart  one line per COLUMN (x axis = the rows)

The table is a dash_ag_grid.AgGrid (pip install dash-ag-grid). Its rowData property is the matrix as a list of
rows, one dict per row. Two callbacks:
    new_matrix   the button writes new random numbers into the grid's rowData
    draw         the grid's rowData -> both charts
So a press of the button runs new_matrix, which changes rowData, which runs draw: callbacks chain.
An edit in the grid also changes rowData, but quietly: the grid announces it through its cellValueChanged property
(which cell changed, old and new value). So draw listens to both.

Run:  python step7_matrix.py   ->  http://127.0.0.1:8050
"""
import numpy as np
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
from dash import Dash, html, dcc, Input, Output

ROWS = [f"row {i}" for i in range(1, 6)]
COLS = [f"c{j}" for j in range(1, 9)]


def random_matrix(seed):
    """A made-up 5 x 8 matrix: each row is a smooth curve plus a little noise."""
    rng = np.random.default_rng(seed)
    x = np.linspace(0, 1, len(COLS))
    values = [rng.uniform(1, 5) + rng.uniform(-2, 2) * x + rng.normal(0, 0.2, len(COLS)) for _ in ROWS]
    return pd.DataFrame(np.round(values, 2), index=pd.Index(ROWS, name="row"), columns=pd.Index(COLS, name="column"))


def to_rows(df):
    """DataFrame -> the grid's rowData (a list of dicts)."""
    return df.reset_index().to_dict("records")


def to_frame(rows):
    """The grid's rowData -> DataFrame with the row labels as the index."""
    df = pd.DataFrame(rows).set_index("row")[COLS].apply(pd.to_numeric, errors="coerce")
    df.columns.name = "column"
    return df


app = Dash(__name__)
app.layout = html.Div([
    html.H1("A matrix and its lines"),
    html.Button("New random matrix", id="new", n_clicks=0),
    dag.AgGrid(
        id="grid",
        rowData=to_rows(random_matrix(0)),
        columnDefs=[{"field": "row", "headerName": "row", "editable": False, "width": 90}]
                   + [{"field": c, "headerName": c, "editable": True, "width": 80} for c in COLS],
        dashGridOptions={"domLayout": "autoHeight"},    # as tall as its rows
        style={"width": 760},
    ),
    html.P("Double-click a cell, type a number, press Enter."),
    dcc.Graph(id="by-row"),
    dcc.Graph(id="by-col"),
])


@app.callback(Output("grid", "rowData"), Input("new", "n_clicks"), prevent_initial_call=True)
def new_matrix(n_clicks):
    return to_rows(random_matrix(n_clicks))


@app.callback(Output("by-row", "figure"),
              Output("by-col", "figure"),
              Input("grid", "rowData"),                # a new matrix from the button
              Input("grid", "cellValueChanged"))       # an edit (rowData is already updated by then)
def draw(rows, edit):
    df = to_frame(rows)
    by_row = px.line(df.T, markers=True, title="One line per row")        # df.T: rows become columns
    by_col = px.line(df, markers=True, title="One line per column")
    return by_row, by_col


if __name__ == "__main__":
    app.run(debug=True)
