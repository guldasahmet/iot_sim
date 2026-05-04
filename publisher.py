import paho.mqtt.client as mqtt
import json
import time
import random
import math
from datetime import datetime

BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "11/telemetry"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Simulasyon_Publisher")
client.connect(BROKER, PORT)

print(f"{BROKER}:{PORT} MQTT Broker'ına bağlanıldı.")
print(f"{TOPIC} kanalına gerçekçi günlük periyotlarla veri gönderimi başlıyor...\n")

sanal_sensorler = [f"temp_{i:03d}" for i in range(1, 101)]

# Her sensörün anlık durumunu hafızada tutuyoruz (Random Walk referansı)
sensor_durumlari = {}
for sid in sanal_sensorler:
    sensor_durumlari[sid] = {
        "sicaklik": random.uniform(12.0, 18.0),
        "nem": random.uniform(50.0, 70.0),
        "isik": 0.0
    }

def baz_degerleri_hesapla(saat, dakika):
    zaman_kesri = (saat + dakika / 60.0) / 24.0
    
    # Sıcaklık: ~05:00'te en soğuk, ~14:00'te en sıcak olacak sinüs dalgası
    hedef_sicaklik = 20.0 + 10.0 * math.sin(2 * math.pi * (zaman_kesri - 0.33))
    
    # Nem: Sıcaklık arttıkça nem düşer (ters orantılı)
    hedef_nem = 65.0 - 20.0 * math.sin(2 * math.pi * (zaman_kesri - 0.33))
    
    # Işık: 06:00 - 19:00 arası güneş ışığı simülasyonu, öğlen zirve yapar
    gunduz_mu = 6.0 <= (saat + dakika / 60.0) <= 19.0
    if gunduz_mu:
        hedef_isik = 500.0 + 500.0 * math.sin(math.pi * ((saat + dakika / 60.0) - 6.0) / 13.0)
    else:
        hedef_isik = 0.0
        
    return hedef_sicaklik, hedef_nem, hedef_isik

try:
    while True:
        simdi = datetime.utcnow()
        zaman_str = simdi.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Günün o saatindeki olması gereken "ideal" değerleri hesapla
        hedef_sic, hedef_nem, hedef_isik = baz_degerleri_hesapla(simdi.hour, simdi.minute)
        
        for sid in sanal_sensorler:
            durum = sensor_durumlari[sid]
            
            # Yeni Değer = Eski Değer + Hedefe Çekim Oranı + Rastgele Gürültü (Random Walk)
            durum["sicaklik"] += 0.05 * (hedef_sic - durum["sicaklik"]) + random.uniform(-0.15, 0.15)
            durum["nem"] += 0.05 * (hedef_nem - durum["nem"]) + random.uniform(-0.8, 0.8)
            durum["isik"] += 0.15 * (hedef_isik - durum["isik"]) + random.uniform(-15.0, 15.0)
            
            # Fiziksel sınırları koruma
            durum["nem"] = max(0.0, min(100.0, durum["nem"]))
            durum["isik"] = max(0.0, min(1200.0, durum["isik"]))
            
            veri_paketi = {
                "sensor_id": sid,
                "values": {
                    "sicaklik": round(durum["sicaklik"], 2),
                    "nem": int(durum["nem"]),
                    "isik": int(durum["isik"])
                },
                "unit": "metric",
                "timestamp": zaman_str
            }
            
            client.publish(TOPIC, json.dumps(veri_paketi))
            
        print(f"[BAŞARILI] {zaman_str} - 100 sensör güncellendi. Referans: Sicaklik={round(hedef_sic,1)}°C, Isik={int(hedef_isik)}")
        time.sleep(1)

except KeyboardInterrupt:
    client.disconnect()
    print("\nVeri gönderimi durduruldu.")