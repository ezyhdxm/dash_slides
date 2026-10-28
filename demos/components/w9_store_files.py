"""dcc.Store (keep data), dcc.Upload (in), dcc.Download (out)."""
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)
app.layout = html.Div([
    dcc.Upload(html.Button("Upload a file"), id="up"),
    dcc.Store(id="kept"),              # keeps data in the browser
    html.Button("Download CSV", id="btn"),
    dcc.Download(id="down"),
    html.Pre(id="out"),
])

@app.callback(Output("kept", "data"), Input("up", "filename"),
              prevent_initial_call=True)
def keep(filename):
    return {"last upload": filename}

@app.callback(Output("out", "children"), Input("kept", "data"))
def show(kept):
    return f"stored: {kept}"

@app.callback(Output("down", "data"), Input("btn", "n_clicks"),
              prevent_initial_call=True)
def download(n):
    return dcc.send_string("cusip,spread\nNOR05123,142\n", "bonds.csv")

if __name__ == "__main__":
    app.run(debug=True)
