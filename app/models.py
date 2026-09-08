from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class FlowSnapshot:
    # Daily net money-flow values, oldest -> newest.
    money_flow: list[float] = field(default_factory=list)
    institutional_pct: Optional[float] = None
    retail_pct: Optional[float] = None
    institutional_cost: Optional[float] = None
    institutional_pct_prev: Optional[float] = None

@dataclass
class KapItem:
    published_at: datetime
    title: str
    category: str = "unknown"
    sentiment: int = 0  # -1 negative, 0 neutral, +1 positive

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
