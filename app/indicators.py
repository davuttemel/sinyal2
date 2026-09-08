import numpy as np
import pandas as pd


def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False).mean()


def stoch_rsi(close: pd.Series, length: int = 14, smooth_k: int = 3, smooth_d: int = 3):
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(length).mean()
    loss = (-delta.clip(upper=0)).rolling(length).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    lo = rsi.rolling(length).min()
    hi = rsi.rolling(length).max()
    stoch = 100 * (rsi - lo) / (hi - lo).replace(0, np.nan)
    k = stoch.rolling(smooth_k).mean()
    d = k.rolling(smooth_d).mean()
    return k, d


def wavetrend(df: pd.DataFrame, channel_length: int = 10, average_length: int = 21):
    ap = (df.high + df.low + df.close) / 3
    esa = ap.ewm(span=channel_length, adjust=False).mean()
    de = (ap - esa).abs().ewm(span=channel_length, adjust=False).mean()
    ci = (ap - esa) / (0.015 * de.replace(0, np.nan))
    wt1 = ci.ewm(span=average_length, adjust=False).mean()
    wt2 = wt1.rolling(4).mean()
    return wt1, wt2


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy().sort_index()
    out["ema20"] = ema(out.close, 20)
    out["vol20"] = out.volume.rolling(20).mean()
    out["vol_ratio"] = out.volume / out.vol20.replace(0, np.nan)
    out["stoch_k"], out["stoch_d"] = stoch_rsi(out.close)
    out["wt1"], out["wt2"] = wavetrend(out)
    return out


def cross_up(a: pd.Series, b: pd.Series) -> bool:
    return len(a) >= 2 and a.iloc[-2] <= b.iloc[-2] and a.iloc[-1] > b.iloc[-1]
