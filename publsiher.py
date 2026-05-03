import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

# --- AYARLAR ---
BROKER = "127.0.0.1" # Yerel MQTT Broker adresi
PORT = 1883
TOPIC = "btu_01/telemetry" # Ödevde istenen topic formatı

# MQTT İstemcisini oluştur
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Simulasyon_Publisher")
client.connect(BROKER, PORT)

print(f"{BROKER}:{PORT} MQTT Broker'ına bağlanıldı.")
print(f"{TOPIC} kanalına veri gönderimi başlıyor...\n")

try:
    while True:
        # Rastgele sensör verileri üret
        sanal_sicaklik = round(random.uniform(15.0, 30.0), 1)
        sanal_nem = random.randint(40, 80)
        sanal_isik = random.randint(200, 800)
        zaman = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        # Proje evrakındaki JSON formatı
        veri_paketi = {
            "sensor_id": "temp_01",
            "values": {
                "sicaklik": sanal_sicaklik
            },
            "nem": sanal_nem,
            "isik": sanal_isik,
            "unit": "metric",
            "timestamp": zaman
        }

        # Veriyi JSON formatına çevir ve MQTT üzerinden yayınla (publish)
        payload = json.dumps(veri_paketi)
        client.publish(TOPIC, payload)
        
        print(f"[BAŞARILI] Yayınlandı: Sıcaklık={sanal_sicaklik}°C, Nem=%{sanal_nem}, Işık={sanal_isik}")

        # 5 saniyede bir gönder (Ödevde periyodik dendiği için bekleme süresini test için 2 sn yapabilirsin)
        time.sleep(2)

except KeyboardInterrupt:
    client.disconnect()
    print("\nVeri gönderimi durduruldu.")