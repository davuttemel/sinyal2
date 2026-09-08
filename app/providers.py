from abc import ABC, abstractmethod
from dataclasses import dataclass
import pandas as pd

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
    base_url: str
    api_key: str


class MatriksProvider(MarketDataProvider):
    """Adapter boundary for the licensed Matriks REST API.

    Endpoint paths are intentionally not hard-coded until the customer's
    subscribed API package/documentation is known. Matriks offers REST API,
    graphical bars, trades, news and AKD/cost data; exact service names and
    payloads depend on the contracted package.
    """

    def __init__(self, config: ProviderConfig):
        self.config = config

    def symbols(self) -> list[str]:
        raise NotImplementedError("Connect symbols() to the subscribed Matriks endpoint")

    def daily(self, symbol: str) -> pd.DataFrame:
        raise NotImplementedError("Connect daily() to the subscribed Matriks bar endpoint")

    def flow(self, symbol: str) -> FlowSnapshot:
        raise NotImplementedError("Connect flow() to AKD/flow endpoint")

    def kap(self, symbol: str) -> list[KapItem]:
        raise NotImplementedError("Connect kap() to KAP API/provider")
