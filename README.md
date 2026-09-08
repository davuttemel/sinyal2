# BIST Weekly Signal Bot

Borsa İstanbul için haftada en fazla 2–3 yüksek kaliteli aday üretmek ve Telegram'a göndermek üzere tasarlanmış açık kaynak tarayıcı.

## Strateji

Sistem tek bir indikatöre göre işlem üretmez. Adayları şu katmanlarla değerlendirir:

- Stoch RSI: 0–20 bölgesinden yukarı AL kesişimi
- WaveTrend: aynı gün AL kesişimi
- 2–3 günlük pozitif para akışı
- Günlük hacim / 20 günlük ortalama hacim
- 20 EMA trend filtresi
- Kurumsal / bireysel yatırımcı oranı
- Kurumsal ortalama maliyet ile mevcut fiyat ilişkisi
- KAP bildirimleri ve haber filtresi
- Sonuçta 0–3 aday; yeterli kalite yoksa işlem yok

### Skor

| Kriter | Puan |
|---|---:|
| Stoch RSI 0–20 AL | +2 |
| WaveTrend AL | +2 |
| Güçlü 3 günlük para akışı | +2 |
| Hacim >= 1.5× 20G ortalama | +2 |
| Para akışında süreklilik | +1 |
| Fiyat > 20 EMA | +1 |
| Kurumsal oran >= %80 | +1 |
| Fiyat kurumsal maliyetin altında | +1 |

Minimum kalite skoru varsayılan olarak 7'dir.

## Veri yaklaşımı

Borsa İstanbul, gerçek zamanlı/gecikmeli/gün sonu verilerin lisanslı veri dağıtıcılar üzerinden yayımlandığını belirtiyor. Kurumsal/bireysel yatırımcı oranı da MKK verileri arasında yer alıyor. KAP'ın resmi Veri Yayın Servisi REST API'si bildirim listesi ve detaylarına erişim sağlıyor. Bu nedenle proje, kritik verileri uyduran bir scraper yerine `MarketDataProvider` arayüzü üzerinden gerçek veri sağlayıcısına bağlanacak şekilde ayrıştırılmıştır.

> Resmi KAP REST entegrasyonu abonelik/kimlik doğrulama gerektirebilir. Kurumsal oran ve maliyet verileri için MKK/BIST lisanslı veri erişimi gerekir. Gecikmeli veya eksik veriyi gerçek sinyal gibi göstermeyin.

## Çalıştırma

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.main
```

Telegram için GitHub Actions Secrets bölümüne `TELEGRAM_BOT_TOKEN` ve `TELEGRAM_CHAT_ID` eklenir.

## Haftalık otomasyon

`.github/workflows/weekly.yml` Pazartesi sabahı taramayı çalıştırır. GitHub Actions UTC kullandığı için Türkiye yaz/kış saati değişiminde cron saatini kontrol edin.

## Uyarı

Bu proje yatırım tavsiyesi değildir. Sinyaller araştırma, izleme ve backtest amacıyla kullanılmalıdır.
