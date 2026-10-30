"""A tour of Dash's built-in widgets. One callback echoes every value, so you can see what each one sends.

Run:  python 03_widgets.py   ->  http://127.0.0.1:8050
"""
from dash import Dash, html, dcc, callback, Output, Input
from data import bonds

app = Dash(__name__)
sectors = sorted(bonds.sector.unique())


def row(label, component):
    return html.Div([html.Label(label, style={"width": "170px", "fontWeight": 600}), component],
                    style={"display": "flex", "alignItems": "center", "gap": "12px", "margin": "10px 0"})


app.layout = html.Div([
    html.H2("Dash widgets (dash.dcc)"),
    row("Dropdown", dcc.Dropdown(sectors, "Banks", id="dropdown", style={"width": "260px"})),
    row("Dropdown (multi)", dcc.Dropdown(sectors, ["Tech"], multi=True, id="multi", style={"width": "360px"})),
    row("Checklist", dcc.Checklist(["AA", "A", "BBB", "BB"], ["A", "BBB"], id="checklist", inline=True)),
    row("RadioItems", dcc.RadioItems(["spread", "coupon"], "spread", id="radio", inline=True)),
    row("Slider", html.Div(dcc.Slider(2, 30, 1, value=10, marks={2: "2y", 10: "10y", 30: "30y"}, id="slider"),
                           style={"width": "360px"})),
    row("RangeSlider", html.Div(dcc.RangeSlider(0, 400, 50, value=[100, 250], id="range"), style={"width": "360px"})),
    row("Input", dcc.Input(id="text", type="text", value="Bank A", debounce=True)),
    row("DatePickerSingle", dcc.DatePickerSingle(id="date", date="2026-09-30")),
    row("Tabs", dcc.Tabs(id="tabs", value="chart", children=[dcc.Tab(label="Chart", value="chart"),
                                                             dcc.Tab(label="Table", value="table")])),
    html.Hr(),
    html.H3("What the server received"),
    html.Pre(id="echo", style={"background": "#f4f4f4", "padding": "12px"}),
    # also built in, not shown: dcc.Graph, dcc.Store, dcc.Interval, dcc.Upload, dcc.Download, dcc.Location,
    # dcc.Loading, dcc.Markdown, dash_table.DataTable; and add-ons such as dash-ag-grid
], style={"maxWidth": "760px", "margin": "auto", "fontFamily": "sans-serif"})


@callback(Output("echo", "children"),
          Input("dropdown", "value"), Input("multi", "value"), Input("checklist", "value"),
          Input("radio", "value"), Input("slider", "value"), Input("range", "value"),
          Input("text", "value"), Input("date", "date"), Input("tabs", "value"))
def echo(*values):
    names = ["dropdown", "multi", "checklist", "radio", "slider", "range", "text", "date", "tabs"]
    return "\n".join(f"{n:<10} = {v!r}" for n, v in zip(names, values))


if __name__ == "__main__":
    app.run(debug=True)
