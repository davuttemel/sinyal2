# BIST Weekly Signal Bot

Borsa İstanbul için haftada en fazla 2–3 yüksek kaliteli aday üretmek ve Telegram'a göndermek üzere tasarlanmış açık kaynak tarayıcı.

## Strateji

Sistem tek bir indikatöre göre işlem üretmez. Adayları şu katmanlarla değerlendirir:

- Stoch RSI: 0–20 bölgesinden yukarı AL kesişimi
- WaveTrend: aynı gün AL kesişimi
- 2–3 günlük pozitif para akışı
- Günlük hacim / 20 günlük ortalama hacim
- 20 EMA trend filtresi
- Kurumsal / bireysel yatırımcı oranı (lisanslı veri bulunursa)
- Kurumsal ortalama maliyet ile mevcut fiyat ilişkisi (lisanslı veri bulunursa)
- KAP bildirimleri (resmi API erişimi bulunursa)
- Sonuçta 0–3 aday; yeterli kalite yoksa işlem yok

## API yokken çalışma modu

Varsayılan tarayıcı Yahoo Finance/yfinance üzerinden BIST günlük OHLCV verisini kullanır. Yahoo'da Borsa İstanbul hisseleri `.IS` sembol uzantısıyla bulunur. yfinance geçmiş günlük fiyat/hacim verisini Python üzerinden indirebilir.

Para akışı tarafında API'siz mod, gerçek AKD/kurumsal para akışı yerine **signed-volume proxy** kullanır. Bu değer kesin kurumsal para girişi olarak yorumlanmaz ve puanı daha düşük tutulur.

KAP tarafında resmi KAP REST servisi kullanılmadığı sürece sistem KAP verisi uydurmaz; bu nedenle KAP puanı nötr kalır.

## Skor

| Kriter | Puan |
|---|---:|
| Stoch RSI 0–20 AL | +2 |
| WaveTrend AL | +2 |
| 3 günlük para akışı | +1 proxy / +2 gerçek veri |
| Hacim >= 1.5× 20G ortalama | +1.5 |
| Hacim >= 2× 20G ortalama | +2 |
| Fiyat > 20 EMA | +1 |
| Kurumsal oran >= %80 | +1 |
| Fiyat kurumsal maliyetin altında | +0.5 / +1 |
| Pozitif KAP | +1 |
| Negatif KAP | -2 |

Varsayılan minimum kalite skoru: **7**.

## Veri kaynakları ve sınırlar

Borsa İstanbul, piyasa verilerinin gerçek zamanlı, gecikmeli ve gün sonu biçimlerinde lisanslı veri dağıtıcılar üzerinden yayıldığını belirtiyor. BIST ayrıca bazı tarihsel/piyasa veri ürünlerini kendi veri sayfalarında listeliyor. citeturn0search0turn0search12

KAP, şirket bildirimlerinin kamuya açık elektronik sistemi ve tarihsel arşividir. Resmi KAP REST Veri Yayın Servisi ise abonelik, yetkilendirme ve API anahtarı gerektirir. citeturn2search12turn2search24

Yahoo/yfinance tarafı araştırma amaçlı kullanılmalıdır; yfinance dokümantasyonu Yahoo verisinin kişisel kullanım şartlarına tabi olduğunu özellikle belirtiyor. citeturn3search5

Bu nedenle API'siz sürüm **araştırma/backtest/izleme** amaçlıdır; lisanslı veri erişimi olmadan kurumsal maliyet veya gerçek AKD verisi varmış gibi davranmaz.

## Çalıştırma

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.main
```

Telegram için GitHub Actions Secrets bölümüne yalnızca:

```text
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

eklenmesi yeterlidir.

## Haftalık otomasyon

`.github/workflows/weekly.yml` Pazartesi 07:30 Türkiye saati hedefiyle taramayı çalıştırır. Workflow ayrıca manuel olarak da başlatılabilir.

## Backtest

`app/backtest.py` sinyali yalnızca o tarihte mevcut barları kullanarak değerlendirir ve girişte gelecek veriyi kullanmamaya çalışır. Sonraki aşamada çoklu hisse portföy backtesti, ATR stop, işlem maliyeti ve benchmark karşılaştırması eklenecektir.

## Uyarı

Bu proje yatırım tavsiyesi değildir. Sinyaller araştırma, izleme ve backtest amacıyla kullanılmalıdır.
