import sqlite3
import json
import time
import paho.mqtt.client as mqtt

BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "11/telemetry"
DB_PATH = "sensor_verileri.db"


def veritabani_kur():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS olcumler
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  zaman TEXT,
                  sicaklik REAL,
                  nem REAL,
                  isik REAL)''')
    conn.commit()
    conn.close()


def on_connect(client, userdata, flags, rc):
    print(f"MQTT Broker'a bağlanıldı! Kanala abone olunuyor: {TOPIC}")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    try:
        veri = json.loads(msg.payload.decode())
        zaman = veri.get("timestamp")
        values = veri.get("values", {})
        sicaklik = values.get("sicaklik", 0)
        nem = values.get("nem", 0)
        isik = values.get("isik", 0)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "INSERT INTO olcumler (zaman, sicaklik, nem, isik) VALUES (?, ?, ?, ?)",
            (zaman, sicaklik, nem, isik),
        )
        conn.commit()
        conn.close()

        print(f"MQTT'den bilgi alındı -> Sıcaklık: {sicaklik} | Nem: {nem} | Işık: {isik}")
    except Exception as e:
        print("MQTT mesaj işleme hatası:", e)


def mqtt_baslat():
    veritabani_kur()
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Sunucu_Subscriber")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(BROKER, PORT)
    mqtt_client.loop_start()
    return mqtt_client


if __name__ == "__main__":
    mqtt_baslat()
    print("Subscriber çalışıyor. MQTT mesajları bekleniyor...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Subscriber durduruldu.")
