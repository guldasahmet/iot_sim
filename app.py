from flask import Flask, render_template, jsonify
import sqlite3
import json
import paho.mqtt.client as mqtt

app = Flask(__name__)

# --- 1. VERİTABANI KURULUMU ---
def veritabani_kur():
    conn = sqlite3.connect('sensor_verileri.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS olcumler
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  zaman TEXT,
                  sicaklik REAL,
                  nem REAL,
                  isik REAL)''')
    conn.commit()
    conn.close()

veritabani_kur()

# --- 2. MQTT SUBSCRIBER AYARLARI ---
BROKER = "127.0.0.1"
TOPIC = "btu_01/telemetry"

def on_connect(client, userdata, flags, rc):
    print(f"MQTT Broker'a bağlanıldı! Kanala abone olunuyor: {TOPIC}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        # Gelen MQTT mesajını JSON olarak çöz
        veri = json.loads(msg.payload.decode())
        
        zaman = veri['timestamp']
        sicaklik = veri['values']['sicaklik']
        nem = veri['nem']
        isik = veri['isik']

        # Veritabanına kaydet
        conn = sqlite3.connect('sensor_verileri.db')
        c = conn.cursor()
        c.execute("INSERT INTO olcumler (zaman, sicaklik, nem, isik) VALUES (?, ?, ?, ?)", 
                  (zaman, sicaklik, nem, isik))
        conn.commit()
        conn.close()
        
        print(f"MQTT'den BİLGİ ALINDI -> Sıcaklık: {sicaklik} | Nem: {nem} | Işık: {isik}")
    except Exception as e:
        print("MQTT Mesaj işleme hatası:", e)

# MQTT istemcisini başlat ve arka planda çalıştır
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Sunucu_Subscriber")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(BROKER, 1883)
mqtt_client.loop_start() # Bu komut MQTT dinleme işlemini Flask'ı bloklamadan arka planda yürütür

# --- 3. WEB ARAYÜZÜ VE API ---
@app.route('/', methods=['GET'])
def ana_sayfa():
    return render_template('index.html')

@app.route('/api/veriler', methods=['GET'])
def verileri_getir():
    try:
        conn = sqlite3.connect('sensor_verileri.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM (SELECT * FROM olcumler ORDER BY id DESC LIMIT 50) ORDER BY id ASC")
        kayitlar = [dict(row) for row in c.fetchall()]
        conn.close()
        return jsonify(kayitlar), 200
    except Exception as e:
        return jsonify({"hata": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False) # use_reloader=False MQTT ile çakışmayı önler