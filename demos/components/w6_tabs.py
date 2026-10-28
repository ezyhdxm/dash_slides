"""dcc.Tabs: the app gets which tab is open."""
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)
app.layout = html.Div([
    dcc.Tabs(id="view", value="chart", children=[
        dcc.Tab(label="Chart", value="chart"),
        dcc.Tab(label="Table", value="table"),
        dcc.Tab(label="Notes", value="notes"),
    ]),
    html.Div(id="page"),
])

@app.callback(Output("page", "children"), Input("view", "value"))
def show(tab):
    return html.P(f"Showing the {tab} tab")  # what the tab shows

if __name__ == "__main__":
    app.run(debug=True)
