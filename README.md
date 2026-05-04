# BLM-0482 | Takım 11 | MQTT Tabanlı Telemetry Simülasyonu

Bu depo, BLM-0482 ödevi için hazırlanmış MQTT tabanlı telemetry simülasyonunu içerir. Çözüm; veri üreten `publisher.py`, veriyi kaydeden `subscriber.py` ve grafikli yönetim arayüzünü sunan `app.py` dosyalarından oluşur.

## Kısa Özet
Sistem, yerel bir MQTT broker üzerinden `11/telemetry` topic'i ile veri taşır. Publisher 100 sanal sensörden sıcaklık, nem ve ışık verisi üretir; subscriber bu verileri SQLite veritabanına yazar; web arayüzü ise sensör bazlı grafik ve istatistikleri gösterir.

## Veri Formatı
Gönderilen telemetry verileri JSON formatındadır. Örnek payload:

```json
{
	"sensor_id": "temp_001",
	"values": {
		"sicaklik": 24.5,
		"nem": 65,
		"isik": 450
	},
	"unit": "metric",
	"timestamp": "2026-03-16T10:00:00Z"
}
```

Üretilen ölçümler:
- Sıcaklık (`sicaklik`)
- Nem (`nem`)
- Işık miktarı (`isik`)

## Mimari
- `publisher.py` gerçekçi günlük döngüye göre veri üretir ve `11/telemetry` topic'ine yayın yapar.
- `subscriber.py` MQTT mesajlarını dinler, JSON verisini çözer ve `sensor_verileri.db` içine kaydeder.
- `app.py` Flask tabanlı API ve web arayüzünü çalıştırır.
- `templates/index.html` sensör seçimi, çizimler ve istatistik kartlarını içerir.

## Gereksinimler
- Python 3.8+
- Paketler: `paho-mqtt`, `flask`

İsteğe bağlı sanal ortam kurulumu:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install paho-mqtt flask
```

## MQTT Broker
Kod, varsayılan olarak `127.0.0.1:1883` adresindeki yerel broker'a bağlanır. Geliştirme için Eclipse Mosquitto kullanılabilir.

Docker ile hızlı başlatma:

```bash
docker run -d --name mosquitto -p 1883:1883 eclipse-mosquitto
```

## Çalıştırma Sırası
1. MQTT broker'ı başlatın.
2. Subscriber'ı çalıştırın:

```bash
python subscriber.py
```

3. Publisher'ı çalıştırın:

```bash
python publisher.py
```

4. Web arayüzünü açın:

```bash
python app.py
```

Arayüz varsayılan olarak `http://127.0.0.1:5000` adresinde çalışır. Topic değeri sabit olarak `11/telemetry` şeklinde tanımlıdır.

## Veritabanı
Subscriber, gelen kayıtları `sensor_verileri.db` dosyasında `olcumler` tablosuna ekler. Web arayüzü seçilen sensör için son 50 kaydı getirir ve sıcaklık, nem, ışık için grafik oluşturur.

## Arayüz
`templates/index.html`, koyu temalı tek sayfalık bir panel sunar. Her sensör için ayrı grafik ve minimum, maksimum, ortalama, varyans değerleri gösterilir. Sensör seçimi arayüz üzerinden yapılır.

## Repo
Uzak depo: https://github.com/guldasahmet/iot_sim

---
Geliştirici: Ahmet
