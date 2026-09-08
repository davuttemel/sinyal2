from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class FlowSnapshot:
    # Daily signed-money-flow values, oldest -> newest.
    money_flow: list[float] = field(default_factory=list)
    institutional_pct: Optional[float] = None
    retail_pct: Optional[float] = None
    institutional_cost: Optional[float] = None
    institutional_pct_prev: Optional[float] = None
    flow_source: str = "unknown"


@dataclass
class KapItem:
    published_at: datetime
    title: str
    category: str = "unknown"
    sentiment: int = 0


@dataclass
class Candidate:
    symbol: str
    score: float
    price: float
    volume_ratio: float
    institutional_pct: Optional[float]
    institutional_cost: Optional[float]
    reasons: list[str]
    kap: list[KapItem] = field(default_factory=list)
