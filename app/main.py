import os

from dotenv import load_dotenv

from .providers import MatriksProvider, ProviderConfig
from .scoring import score


def main() -> None:
    load_dotenv()
    provider = MatriksProvider(
        ProviderConfig(
            base_url=os.getenv("MATRIKS_API_BASE_URL", ""),
            api_key=os.getenv("MATRIKS_API_KEY", ""),
        )
    )
    candidates = []
    for symbol in provider.symbols():
        df = provider.daily(symbol)
        flow = provider.flow(symbol)
        kap = provider.kap(symbol)
        candidate = score(symbol, df, flow, kap)
        if candidate and candidate.score >= float(os.getenv("MIN_SCORE", "7")):
            candidates.append(candidate)

    candidates.sort(key=lambda c: c.score, reverse=True)
    picks = candidates[: int(os.getenv("MAX_PICKS", "3"))]

    if not picks:
        print("BIST haftalık tarama: işlem yok.")
        return

    for pick in picks:
        print(f"{pick.symbol}: {pick.score} | {pick.price} | {', '.join(pick.reasons)}")


if __name__ == "__main__":
    main()
