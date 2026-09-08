from .indicators import cross_up, enrich
from .models import Candidate, FlowSnapshot, KapItem


def score(symbol: str, df, flow: FlowSnapshot, kap: list[KapItem] | None = None) -> Candidate | None:
    kap = kap or []
    x = enrich(df)
    if len(x) < 60:
        return None
    last = x.iloc[-1]
    points = 0.0
    reasons: list[str] = []

    if last.stoch_k <= 20 and cross_up(x.stoch_k, x.stoch_d):
        points += 2
        reasons.append("Stoch RSI 0–20 AL kesişimi")
    if cross_up(x.wt1, x.wt2):
        points += 2
        reasons.append("WaveTrend AL kesişimi")

    flows = flow.money_flow[-3:]
    positive_days = sum(v > 0 for v in flows)
    if positive_days == 3:
        points += 1 if flow.flow_source == "signed_volume_proxy" else 2
        label = "3/3 gün pozitif para akışı"
        if flow.flow_source == "signed_volume_proxy":
            label += " (hacim proxy)"
        reasons.append(label)
    elif positive_days == 2:
        points += 0.5 if flow.flow_source == "signed_volume_proxy" else 1
        reasons.append("2/3 gün pozitif para akışı")
    elif positive_days == 0:
        points -= 1 if flow.flow_source == "signed_volume_proxy" else 2
        reasons.append("3/3 gün negatif para akışı")

    if last.vol_ratio >= 2.0:
        points += 2
        reasons.append(f"Çok güçlü hacim ({last.vol_ratio:.2f}x)")
    elif last.vol_ratio >= 1.5:
        points += 1.5
        reasons.append(f"Güçlü hacim ({last.vol_ratio:.2f}x)")

    if last.close > last.ema20:
        points += 1
        reasons.append("Fiyat 20 EMA üzerinde")

    if flow.institutional_pct is not None and flow.institutional_pct >= 80:
        points += 1
        reasons.append(f"Kurumsal oran %{flow.institutional_pct:.1f}")

    if flow.institutional_cost and last.close < flow.institutional_cost:
        discount = (flow.institutional_cost - last.close) / flow.institutional_cost
        if discount <= 0.05:
            points += 1
            reasons.append(f"Fiyat kurumsal maliyetin %{discount*100:.1f} altında")
        elif discount <= 0.10:
            points += 0.5
            reasons.append(f"Fiyat kurumsal maliyetin %{discount*100:.1f} altında")

    kap_sentiment = sum(item.sentiment for item in kap)
    if kap_sentiment > 0:
        points += 1
        reasons.append("Son KAP akışı pozitif")
    elif kap_sentiment < 0:
        points -= 2
        reasons.append("Son KAP akışı negatif")

    return Candidate(
        symbol=symbol,
        score=round(points, 2),
        price=float(last.close),
        volume_ratio=float(last.vol_ratio),
        institutional_pct=flow.institutional_pct,
        institutional_cost=flow.institutional_cost,
        reasons=reasons,
        kap=kap,
    )
