"""The showcase: a small bond-monitor app using everything from the talk, plus a few extras.

Run:  pip install dash-ag-grid   (once)
      python 06_full_app.py   ->  http://127.0.0.1:8050

  * filters in the sidebar drive KPIs, a scatter, a sector chart and a grid (one callback, many outputs)
  * click a bond on the scatter OR select a row in the grid -> its spread history (ctx.triggered_id)
  * "Live" switch: a dcc.Interval ticks every 2 s and the server re-prices (simulated)
  * download the filtered bonds as CSV (dcc.Download)
  * assets/style.css is picked up automatically
"""
import threading

import numpy as np
from dash import Dash, html, dcc, callback, Output, Input, State, ctx, no_update
import dash_ag_grid as dag
import plotly.express as px
from data import bonds, history

app = Dash(__name__, title="Bond monitor")
SECTORS = sorted(bonds.sector.unique())
RATINGS = ["AA", "A", "BBB", "BB"]
# The dev server runs callbacks in threads; build Plotly figures one at a time to be safe.
FIGS = threading.Lock()


def live_spreads(tick):
    """Today's spreads, nudged by a deterministic random move per tick (a stand-in for a live feed)."""
    if not tick:
        return bonds.spread
    move = np.random.default_rng(tick).normal(0, 3, len(bonds))
    return (bonds.spread + move).round(1)


def filtered(sectors, ratings, mat, tick):
    d = bonds.assign(spread=live_spreads(tick))
    return d[d.sector.isin(sectors) & d.rating.isin(ratings) & d.maturity.between(*mat)]


def kpi(label, id_):
    return html.Div([html.Div(label, className="label"), html.Div(id=id_, className="value")], className="kpi")


app.layout = html.Div([
    html.Div([
        html.Div("Bond monitor", className="title"),
        html.H3("Sector"),
        dcc.Checklist(SECTORS, SECTORS, id="sectors"),
        html.H3("Rating"),
        dcc.Dropdown(RATINGS, RATINGS, multi=True, id="ratings"),
        html.H3("Maturity (years)"),
        dcc.RangeSlider(2, 30, value=[2, 30], marks={2: "2", 10: "10", 20: "20", 30: "30"}, id="maturity"),
        html.H3("Live prices"),
        dcc.RadioItems(["Off", "Live"], "Off", id="live", inline=True),
        dcc.Interval(id="tick", interval=2000, disabled=True),
        html.Button("Download CSV", id="download-btn", className="btn"),
        dcc.Download(id="download"),
        html.P("Click a point or select a grid row to see its history.", className="hint"),
    ], className="side"),
    html.Div([
        html.P(id="asof", className="sub"),
        html.Div([kpi("Bonds", "k-count"), kpi("Issuers", "k-issuers"), kpi("Avg spread (bp)", "k-spread"),
                  kpi("Notional ($bn)", "k-amount")], className="kpis"),
        html.Div([dcc.Graph(id="scatter"), dcc.Graph(id="detail")], className="two"),
        dcc.Tabs([
            dcc.Tab(label="Bonds", children=dag.AgGrid(
                id="grid",
                columnDefs=[{"field": c} for c in ["cusip", "issuer", "sector", "rating", "maturity", "coupon",
                                                   "spread", "amount"]],
                defaultColDef={"sortable": True, "filter": True, "flex": 1},
                dashGridOptions={"rowSelection": "single", "animateRows": True},
                getRowId="params.data.cusip",
                style={"height": "300px"})),
            dcc.Tab(label="By sector", children=dcc.Graph(id="sector-chart")),
        ]),
    ], className="main"),
], className="shell")


@callback(Output("k-count", "children"), Output("k-issuers", "children"), Output("k-spread", "children"),
          Output("k-amount", "children"), Output("scatter", "figure"), Output("grid", "rowData"),
          Output("sector-chart", "figure"), Output("asof", "children"),
          Input("sectors", "value"), Input("ratings", "value"), Input("maturity", "value"),
          Input("tick", "n_intervals"))
def refresh(sectors, ratings, mat, tick):
    d = filtered(sectors, ratings, mat, tick)
    with FIGS:
        scatter, bars = sector_figures(d)
    asof = "Live: tick %d" % tick if tick else "Close of 2026-09-30"
    return (len(d), d.issuer.nunique(), f"{d.spread.mean():.0f}" if len(d) else "–",
            f"{d.amount.sum() / 1000:.1f}", scatter, d.to_dict("records"), bars, asof)


def sector_figures(d):
    scatter = px.scatter(d, x="maturity", y="spread", color="sector", size="amount", hover_name="issuer",
                         custom_data=["cusip"], height=340, title="Spread vs maturity (click a bond)",
                         category_orders={"sector": SECTORS})
    scatter.update_layout(margin=dict(l=40, r=10, t=50, b=40), uirevision="keep")
    by = d.groupby(["sector", "rating"], as_index=False).spread.mean()
    bars = px.bar(by, x="sector", y="spread", color="rating", barmode="group", height=320,
                  category_orders={"rating": RATINGS}, title="Average spread by sector and rating")
    return scatter, bars


@callback(Output("detail", "figure"), Input("scatter", "clickData"), Input("grid", "selectedRows"))
def detail(click, rows):
    if ctx.triggered_id == "grid" and rows:                 # which Input fired this call?
        cusip = rows[0]["cusip"]
    elif ctx.triggered_id == "scatter" and click:
        cusip = click["points"][0]["customdata"][0]
    else:
        cusip = bonds.sort_values("spread").cusip.iloc[-1]   # start on the widest bond
    b = bonds.set_index("cusip").loc[cusip]
    with FIGS:
        fig = px.line(history[history.cusip == cusip], x="date", y="spread", height=340,
                      title=f"{b.issuer} {b.maturity}y {b.rating}: one-year spread")
        fig.update_layout(margin=dict(l=40, r=10, t=50, b=40))
    return fig


@callback(Output("tick", "disabled"), Input("live", "value"))
def toggle_live(mode):
    return mode != "Live"


@callback(Output("download", "data"), Input("download-btn", "n_clicks"),
          State("sectors", "value"), State("ratings", "value"), State("maturity", "value"),
          State("tick", "n_intervals"), prevent_initial_call=True)
def download(_, sectors, ratings, mat, tick):
    d = filtered(sectors, ratings, mat, tick)
    return dcc.send_data_frame(d.to_csv, "bonds.csv", index=False)


if __name__ == "__main__":
    app.run(debug=True)
