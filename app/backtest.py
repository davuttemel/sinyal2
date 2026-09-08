"""Simple weekly signal backtest for OHLCV data.

The backtester deliberately uses only information available on each signal
bar. It is intended for research, not live trading execution.
"""

from dataclasses import dataclass

import pandas as pd

from .indicators import cross_up, enrich


@dataclass
class Trade:
    entry_date: object
    entry_price: float
    exit_date: object
    exit_price: float
    return_pct: float
    reason: str


def generate_signal(df: pd.DataFrame) -> bool:
    x = enrich(df)
    if len(x) < 60:
        return False
    last = x.iloc[-1]
    stoch_buy = last.stoch_k <= 20 and cross_up(x.stoch_k, x.stoch_d)
    wt_buy = cross_up(x.wt1, x.wt2)
    volume_ok = last.vol_ratio >= 1.5
    return bool(stoch_buy and wt_buy and volume_ok)


def run(df: pd.DataFrame, holding_days: int = 10) -> list[Trade]:
    """Run a conservative one-position-at-a-time backtest.

    Entry is next bar open after a weekly signal check. Exit occurs on the
    first of: holding_days elapsed, WaveTrend bearish cross, or Stoch RSI
    bearish cross from above 80. No future information is used at entry.
    """
    if len(df) < 70:
        return []

    data = df.copy().sort_index()
    trades: list[Trade] = []
    i = 60

    while i < len(data) - 1:
        # Evaluate only once per week (Monday-Friday bars: every 5 bars).
        window = data.iloc[: i + 1]
        if not generate_signal(window):
            i += 1
            continue

        entry_i = i + 1
        entry = data.iloc[entry_i]
        entry_price = float(entry.open)
        exit_i = min(entry_i + holding_days, len(data) - 1)
        reason = "time"

        enriched = enrich(data.iloc[: exit_i + 1])
        for j in range(entry_i + 1, exit_i + 1):
            prev = enriched.iloc[j - 1]
            cur = enriched.iloc[j]
            if prev.wt1 >= prev.wt2 and cur.wt1 < cur.wt2:
                exit_i = j
                reason = "wavetrend_reversal"
                break
            if prev.stoch_k >= prev.stoch_d and cur.stoch_k < cur.stoch_d and prev.stoch_k > 80:
                exit_i = j
                reason = "stoch_reversal"
                break

        exit_bar = data.iloc[exit_i]
        exit_price = float(exit_bar.close)
        ret = (exit_price / entry_price - 1.0) * 100
        trades.append(
            Trade(
                entry_date=data.index[entry_i],
                entry_price=entry_price,
                exit_date=data.index[exit_i],
                exit_price=exit_price,
                return_pct=ret,
                reason=reason,
            )
        )
        i = exit_i + 1

    return trades


def summary(trades: list[Trade]) -> dict[str, float]:
    if not trades:
        return {"trades": 0.0, "win_rate": 0.0, "avg_return_pct": 0.0, "total_return_pct": 0.0}
    returns = pd.Series([t.return_pct for t in trades], dtype=float)
    return {
        "trades": float(len(trades)),
        "win_rate": float((returns > 0).mean() * 100),
        "avg_return_pct": float(returns.mean()),
        "total_return_pct": float(((1 + returns / 100).prod() - 1) * 100),
    }
