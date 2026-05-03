# iot_sim

Basit bir IoT veri simülasyonu ve MQTT yayınlayıcısı.

## İçerik
- `app.py` — Web arayüzü / uygulama başlangıcı.
- `publsiher.py` — MQTT ile veri yayınlayan betik.
- `templates/index.html` — Basit frontend.
- `sensor_verileri.db` — Örnek veritabanı (SQLite).

## Gereksinimler
- Python 3.8 veya daha yeni
- Gerekirse MQTT için `paho-mqtt` paketini yükleyin:

```bash
pip install -r requirements.txt
# veya
pip install paho-mqtt
```

## Çalıştırma

1. Sanal ortam oluşturun (önerilir):

```bash
python -m venv .venv
.
# Windows PowerShell için: .venv\Scripts\Activate.ps1
# Linux/macOS için: source .venv/bin/activate
```

2. Gerekli paketleri yükleyin.

3. Uygulamayı başlatın:

```bash
python app.py
```

4. `publsiher.py` MQTT yayını testi için ayrı çalıştırılabilir.

## Notlar
- Veritabanı dosyası `sensor_verileri.db` çalıştırma sırasında yerel verileri içerir.
- Değişiklik yapmak isterseniz, branch ve commit mesajı konusunda bana talimat verin — ben push'layabilirim.

---
Geliştirici: Ahmet
