"""dcc.DatePickerSingle (one date) and dcc.DatePickerRange (two)."""
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)
app.layout = html.Div([
    dcc.DatePickerSingle(
        id="asof",
        date="2026-10-27",
    ),
    dcc.DatePickerRange(
        id="window",
        start_date="2026-10-05",
        end_date="2026-10-16",
    ),
    html.Pre(id="out"),
])

@app.callback(Output("out", "children"), Input("asof", "date"),
              Input("window", "start_date"), Input("window", "end_date"))
def show(asof, start, end):
    return f"as of {asof}\nwindow {start} to {end}"  # dates are text

if __name__ == "__main__":
    app.run(debug=True)
