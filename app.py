from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)


def veritabani_kur():
    conn = sqlite3.connect('sensor_verileri.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS olcumler
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  zaman TEXT,
                  sensor_id TEXT,
                  sicaklik REAL,
                  nem REAL,
                  isik REAL)''')
    conn.commit()
    conn.close()


# --- 3. WEB ARAYÜZÜ VE API ---
@app.route('/', methods=['GET'])
def ana_sayfa():
    return render_template('index.html')

@app.route('/api/veriler', methods=['GET'])
def verileri_getir():
    # Artık her zaman bir sensör id seçili gelecek
    sensor_id = request.args.get('sensor_id')
    
    if not sensor_id:
        return jsonify({"hata": "sensor_id parametresi gerekli"}), 400

    try:
        conn = sqlite3.connect('sensor_verileri.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        # Sadece seçilen sensöre ait son 50 veriyi getir
        c.execute("SELECT * FROM (SELECT * FROM olcumler WHERE sensor_id = ? ORDER BY id DESC LIMIT 50) ORDER BY id ASC", (sensor_id,))
            
        kayitlar = [dict(row) for row in c.fetchall()]
        conn.close()
        return jsonify(kayitlar), 200
    except Exception as e:
        return jsonify({"hata": str(e)}), 500

if __name__ == '__main__':
    veritabani_kur()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)