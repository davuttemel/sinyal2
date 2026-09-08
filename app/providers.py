from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd
import yfinance as yf
from yfinance import EquityQuery

from .models import FlowSnapshot, KapItem


class MarketDataProvider(ABC):
    @abstractmethod
    def symbols(self) -> list[str]: ...

    @abstractmethod
    def daily(self, symbol: str) -> pd.DataFrame: ...

    @abstractmethod
    def flow(self, symbol: str) -> FlowSnapshot: ...

    @abstractmethod
    def kap(self, symbol: str) -> list[KapItem]: ...


@dataclass
class ProviderConfig:
    base_url: str = ""
    api_key: str = ""


class YahooProvider(MarketDataProvider):
    """API-free research provider using Yahoo Finance/yfinance.

    Yahoo identifies Borsa Istanbul equities with the .IS suffix. The provider
    deliberately labels its signed-volume calculation as a proxy; it is not
    broker-level AKD or institutional money flow.
    """

    def symbols(self) -> list[str]:
        query = EquityQuery("and", [
            EquityQuery("eq", ["region", "tr"]),
            EquityQuery("eq", ["exchange", "IST"]),
        ])
        response = yf.screen(query, size=250, sortField="dayvolume", sortAsc=False)
        quotes = response.get("quotes", [])
        symbols = []
        for quote in quotes:
            symbol = str(quote.get("symbol", ""))
            if symbol.endswith(".IS"):
                symbols.append(symbol.removesuffix(".IS"))
        return sorted(set(symbols))

    @staticmethod
    def _ticker(symbol: str) -> str:
        return symbol if symbol.endswith(".IS") else f"{symbol}.IS"

    def daily(self, symbol: str) -> pd.DataFrame:
        data = yf.Ticker(self._ticker(symbol)).history(
            period="2y",
            interval="1d",
            auto_adjust=False,
            repair=True,
        )
        if data.empty:
            raise ValueError("Yahoo Finance günlük veri döndürmedi")
        data = data.rename(columns={c: c.lower() for c in data.columns})
        required = ["open", "high", "low", "close", "volume"]
        missing = [c for c in required if c not in data.columns]
        if missing:
            raise ValueError(f"Eksik OHLCV alanları: {missing}")
        return data[required].dropna()

    def flow(self, symbol: str) -> FlowSnapshot:
        data = self.daily(symbol).tail(20).copy()
        spread = (data.high - data.low).replace(0, pd.NA)
        clv = ((2 * data.close - data.high - data.low) / spread).fillna(0)
        money_flow = (clv * data.volume).tolist()
        return FlowSnapshot(
            money_flow=money_flow,
            flow_source="signed_volume_proxy",
        )

    def kap(self, symbol: str) -> list[KapItem]:
        # Do not pretend Yahoo news is KAP data.
        return []


class MatriksProvider(MarketDataProvider):
    """Placeholder for a future licensed Matriks integration."""

    def __init__(self, config: ProviderConfig):
        self.config = config

    def symbols(self) -> list[str]:
        raise NotImplementedError("Matriks API credentials/package are not configured")

    def daily(self, symbol: str) -> pd.DataFrame:
        raise NotImplementedError

    def flow(self, symbol: str) -> FlowSnapshot:
        raise NotImplementedError

    def kap(self, symbol: str) -> list[KapItem]:
        raise NotImplementedError
