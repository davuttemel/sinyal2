import requests

from .models import Candidate


def send(text: str, token: str, chat_id: str) -> None:
    if not token or not chat_id:
        raise RuntimeError("Telegram credentials missing")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        },
        timeout=20,
    )
    response.raise_for_status()


def format_pick(pick: Candidate) -> str:
    lines = [
        f"🟢 <b>{pick.symbol}</b>",
        f"Skor: <b>{pick.score:.1f}</b>",
        f"Fiyat: {pick.price:.2f}",
        f"Hacim: {pick.volume_ratio:.2f}x (20G)",
    ]

    if pick.institutional_pct is not None:
        lines.append(f"Kurumsal: %{pick.institutional_pct:.1f}")
    if pick.institutional_cost is not None:
        lines.append(f"Kurumsal maliyet: {pick.institutional_cost:.2f}")

    if pick.reasons:
        lines.append("Nedenler:")
        lines.extend(f"• {reason}" for reason in pick.reasons)

    if pick.kap:
        lines.append("KAP:")
        for item in pick.kap[:3]:
            lines.append(f"• {item.title}")

    return "\n".join(lines)


def format_report(picks: list[Candidate]) -> str:
    header = "📊 <b>BIST HAFTALIK SİNYAL</b>"

    if not picks:
        return (
            f"{header}\n\n"
            "⚪ Bu hafta işlem kriterlerini karşılayan yeterli kalitede "
            "hisse bulunamadı.\n"
            "İşlem yok."
        )

    body = "\n\n".join(format_pick(pick) for pick in picks)
    footer = (
        "\n\n<i>Bu mesaj yatırım tavsiyesi değildir. "
        "Sistem teknik, para akışı, kurumsal veri ve KAP filtrelerini "
        "birlikte değerlendirir.</i>"
    )
    return f"{header}\n\n{body}{footer}"
