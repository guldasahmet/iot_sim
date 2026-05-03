# BLM-0482 — Nesnelerin İnterneti Simülasyon Ödevi

Bu depo, ders ödevi kapsamında geliştirilen IoT simülasyon projesini içerir. Proje; simülasyon veri üreticisi (publisher), yerel MQTT sunucusu kurulumu ve analiz/depolama (subscriber) bileşenlerinden oluşur.

## Proje Kapsamı
Takımın kullanacağı MQTT topic formatı:

```
<takim_no>/telemetry
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

## Dosya Yapısı
- `app.py` — Basit web arayüzü (opsiyonel)
- `publsiher.py` — Periyodik veri üreten ve `takim_no/telemetry` topic'ine yayın yapan betik
- `subscriber.py` — (opsiyonel, örnek) topic'i dinleyip veritabanına kaydeden betik
- `templates/index.html` — Frontend
- `sensor_verileri.db` — SQLite veritabanı (örnek)

## Gereksinimler
- Python 3.8+
- Önerilen paketler: `paho-mqtt`, `flask` (web için), `pandas`, `matplotlib`, `sqlite3` (standart)

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
python publsiher.py --team 01
```

Subscriber (örnek):

```bash
python subscriber.py --team 01
```

Bu komutlar betiklerinizdeki argüman isimlerine göre uyarlanmalıdır (`--team` yerine `TAKIM_NO` environment değişkeni de kullanılabilir).

## Veritabanı ve Analiz
- Subscriber aldığı JSON verilerini SQLite veritabanına kaydeder (`sensor_verileri.db`).
- Her sensör için ayrı zaman serisi grafiği oluşturulacaktır.
- Her grafiğin yanında ilgili sensör verilerinin minimum, maksimum, ortalama ve varyans değerleri gösterilecektir.

## Görsel Tasarım
Tek sayfada sensör analiz sonuçları alt alta gösterilecek şekilde tasarlanmalıdır. `templates/index.html` örnek bir yerleşim sunar; istenirse Flask üzerinden dinamik olarak veriler render edilebilir.

## Değerlendirme
- Proje raporu (e-kampüs) teslimi gereklidir.
- Haberleşme topic'i ve JSON formatı raporda belirtilen kurallara uygun olmalıdır.

---
Geliştirici: Ahmet
