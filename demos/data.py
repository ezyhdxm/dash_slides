"""A small synthetic corporate-bond universe shared by every demo.

Deterministic (fixed seed), generated in memory: no files, no network.
    bonds    one row per bond: cusip, issuer, sector, rating, maturity, coupon, spread (bp), amount ($mm)
    history  daily spread per bond over the last year: date, cusip, spread
"""
import numpy as np
import pandas as pd

ISSUERS = {
    "Banks": ["Northbank", "Harbor Trust", "Summit Financial"],
    "Energy": ["Petra Oil", "Bluewater Gas", "Ridge Power"],
    "Tech": ["Quanta Systems", "Nimbus Cloud", "Vertex Chips"],
    "Consumer": ["Maple Foods", "Urban Retail", "Crest Beverages"],
}
RATING_SPREAD = {"AA": 60, "A": 95, "BBB": 150, "BB": 290}
SECTOR_SPREAD = {"Banks": 10, "Energy": 35, "Tech": -5, "Consumer": 0}


def make_bonds(seed=7):
    rng = np.random.default_rng(seed)
    rows = []
    for sector, issuers in ISSUERS.items():
        for issuer in issuers:
            rating = rng.choice(list(RATING_SPREAD), p=[0.15, 0.35, 0.35, 0.15])
            for maturity in rng.choice([2, 3, 5, 7, 10, 20, 30], size=5, replace=False):
                spread = (RATING_SPREAD[rating] + SECTOR_SPREAD[sector] + 4 * maturity
                          + rng.normal(0, 12))
                rows.append({
                    "cusip": f"{issuer[:3].upper()}{int(maturity):02d}{rng.integers(100, 999)}",
                    "issuer": issuer,
                    "sector": sector,
                    "rating": rating,
                    "maturity": int(maturity),
                    "coupon": round(2.0 + spread / 100 + rng.normal(0, 0.3), 2),
                    "spread": round(float(spread), 1),
                    "amount": int(rng.choice([250, 500, 750, 1000, 1500])),
                })
    return pd.DataFrame(rows).sort_values(["sector", "issuer", "maturity"], ignore_index=True)


def make_history(bonds, days=260, seed=11):
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(end="2026-09-30", periods=days)
    market = np.cumsum(rng.normal(0, 1.2, days))          # a common market factor
    frames = []
    for b in bonds.itertuples():
        own = np.cumsum(rng.normal(0, 1.5, days))
        path = b.spread + market + own - (market[-1] + own[-1])   # ends at today's spread
        frames.append(pd.DataFrame({"date": dates, "cusip": b.cusip, "spread": path.round(1)}))
    return pd.concat(frames, ignore_index=True)


bonds = make_bonds()
history = make_history(bonds)

if __name__ == "__main__":
    print(bonds.head(), "\n", len(bonds), "bonds;", len(history), "history rows")
