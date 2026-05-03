# BLM-0482 | Takım 11 | MQTT Tabanlı Telemetry Simülasyonu

**Takım No:** 11

Bu depo, BLM-0482 ödevi kapsamında takım 11 için hazırlanmış MQTT tabanlı telemetry simülasyonunu içerir. Çözüm; publisher, yerel MQTT altyapısı, subscriber ve yönetim arayüzünden oluşur.

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
MQTT altyapısı üzerinden periyodik olarak üretilen telemetry verilerini yayınlamak, bu verileri dinleyip veritabanına kaydetmek ve tek sayfalık bir arayüzde grafik + istatistik olarak sunmak.

## Senaryo
Takım 11 için hazırlanan çözümde sıcaklık, nem ve ışık miktarı sensör verileri `11/telemetry` topic'i üzerinden izlenir. Arayüzde her sensör için zaman serisi grafiği, minimum, maksimum, ortalama ve varyans değerleri ayrı ayrı gösterilir.

## Dosya Yapısı
- `publisher.py` — Periyodik veri üreten ve `11/telemetry` topic'ine yayın yapan betik
- `subscriber.py` — MQTT'den gelen telemetry verisini dinleyip veritabanına kaydeden betik
- `app.py` — Flask tabanlı yönetim arayüzü ve grafik API'si
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
python publisher.py
```

Subscriber (örnek):

```bash
python subscriber.py
```

Web arayüzü (örnek):

```bash
python app.py
```

Not: Publisher, subscriber ve web arayüzü aynı broker adresini kullanmalıdır. Topic doğrudan `11/telemetry` olarak ayarlanmıştır.

## Veritabanı ve Analiz
- Subscriber aldığı JSON verilerini SQLite veritabanına kaydeder (`sensor_verileri.db`).
- Her sensör için ayrı zaman serisi grafiği oluşturulur.
- Her grafiğin yanında ilgili sensör verilerinin minimum, maksimum, ortalama ve varyans değerleri gösterilir.

## Görsel Tasarım
Tek sayfada sensör analiz sonuçları alt alta gösterilecek şekilde tasarlanmıştır. `templates/index.html` dosyası modern dark mode bir arayüz sunar.

## Değerlendirme
- Proje raporu (e-kampüs) teslimi gereklidir.
- Haberleşme topic'i ve JSON formatı raporda belirtilen kurallara uygun olmalıdır.
- Tüm telemetry verileri JSON formatında iletilmelidir.

---
Geliştirici: Ahmet
