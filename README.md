# BLM-0482 — Nesnelerin İnterneti Simülasyon Ödevi

**Konu:** Topraklı Tarımda Isıtma Sistemi

**Takım No:** 11

Bu depo, takım 11 için hazırlanan topraklı tarımda ısıtma sistemi simülasyonunu içerir. Proje; sensör verisi üreten publisher, yerel MQTT altyapısı ve veriyi alan, kaydeden ve analiz eden subscriber / web arayüzü bileşenlerinden oluşur.

## Proje Kapsamı
Kullanılan MQTT topic formatı:

```
11/telemetry
```

Gönderilen telemetry verileri JSON formatında olmalıdır. Örnek:

```json
{
	"sensor_id": "temp_01",
	"values": {
		"sicaklik": 24.5,
		"nem": 65,
		"isik": 450
	},
	"unit": "metric",
	"timestamp": "2026-03-16T10:00:00Z"
}
```

Ölçülen / üretilecek nicelikler:
- Sıcaklık (sicaklik)
- Nem (nem)
- Işık miktarı (isik)

## Proje Amacı
Topraklı tarım uygulamalarında ısıtma aksiyonunun otonom yönetimini modellemek; bitkinin ihtiyaç duyacağı sıcaklığı ortam sıcaklığına bağlı olarak ayarlamak ve bu süreci MQTT tabanlı telemetry akışıyla izlemek.

## Senaryo
Sistemde üç farklı bitki seçimi dikkate alınmalıdır:
- Marul
- Nane
- Fesleğen

Seçilen bitkiye göre ısıtma rejimi değişmelidir. Arayüzde sensörler için zaman serisi grafikleri, en düşük / en yüksek / ortalama / varyans değerleri ve tek sayfalık gösterim sağlanır.

## Dosya Yapısı
- `app.py` — MQTT subscriber + Flask tabanlı yönetim arayüzü
- `publsiher.py` — Periyodik veri üreten ve `11/telemetry` topic'ine yayın yapan betik
- `templates/index.html` — Dark mode yönetim arayüzü
- `sensor_verileri.db` — SQLite veritabanı

## Gereksinimler
- Python 3.8+
- Önerilen paketler: `paho-mqtt`, `flask`, `pandas`, `matplotlib`

Örnek kurulum:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install paho-mqtt flask pandas matplotlib
```

## Yerel MQTT Sunucusu (öneri)
Yerel MQTT sunucusu için Eclipse Mosquitto kullanılabilir.

Docker ile hızlı başlatma:

```bash
docker run -d --name mosquitto -p 1883:1883 eclipse-mosquitto
```

Ya da işletim sisteminize uygun Mosquitto kurulumu yapabilirsiniz.

## Çalıştırma

Publisher (örnek):

```bash
python publsiher.py
```

Subscriber / arayüz (örnek):

```bash
python app.py
```

Not: Publisher ve subscriber aynı broker adresini kullanmalıdır. Topic doğrudan `11/telemetry` olarak ayarlanmıştır.

## Veritabanı ve Analiz
- Subscriber aldığı JSON verilerini SQLite veritabanına kaydeder (`sensor_verileri.db`).
- Her sensör için ayrı zaman serisi grafiği oluşturulur.
- Her grafiğin yanında ilgili sensör verilerinin minimum, maksimum, ortalama ve varyans değerleri gösterilir.

## Görsel Tasarım
Tek sayfada sensör analiz sonuçları alt alta gösterilecek şekilde tasarlanmıştır. `templates/index.html` dosyası modern dark mode bir arayüz sunar.

## Değerlendirme
- Proje raporu (e-kampüs) teslimi gereklidir.
- Haberleşme topic'i ve JSON formatı raporda belirtilen kurallara uygun olmalıdır.
- Bitki seçimine göre ısıtma rejimi farklılaştırılmalıdır.

---
Geliştirici: Ahmet
