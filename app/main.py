import os

from dotenv import load_dotenv

from .providers import YahooProvider
from .scoring import score
from .telegram import format_report, send


def main() -> None:
    load_dotenv()
    provider = YahooProvider()
    candidates = []

    for symbol in provider.symbols():
        try:
            df = provider.daily(symbol)
            flow = provider.flow(symbol)
            kap = provider.kap(symbol)
            candidate = score(symbol, df, flow, kap)
            if candidate and candidate.score >= float(os.getenv("MIN_SCORE", "7")):
                candidates.append(candidate)
        except Exception as exc:
            print(f"{symbol}: veri alınamadı: {exc}")

    candidates.sort(key=lambda c: c.score, reverse=True)
    picks = candidates[: int(os.getenv("MAX_PICKS", "3"))]

    report = format_report(picks)
    print(report)

    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    if token and chat_id:
        send(report, token, chat_id)
    else:
        print("Telegram credentials yok; bildirim gönderilmedi.")


if __name__ == "__main__":
    main()
