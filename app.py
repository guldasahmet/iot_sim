from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)


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