from flask import Flask, request, jsonify
import http.client
import os
from datetime import datetime

app = Flask(__name__)

# Ortam değişkeninden API anahtarını al (Render gibi ortamlarda güvenli kullanım)
API_KEY = os.getenv("COLLECTAPI_KEY", "your_token")  # Buraya kendi API key'ini gir ya da ortam değişkeni kullan

@app.route("/")
def home():
    return "API is working!"

@app.route("/pray/<city>", methods=["GET"])
def get_example_prayer_times(city):
    # Örnek JSON cevabı - statik veri
    example = {
        "city": city.title(),
        "date": datetime.today().strftime('%Y-%m-%d'),
        "imsak": "04:05",
        "gunes": "05:35",
        "ogle": "12:45",
        "ikindi": "16:20",
        "aksam": "19:45",
        "yatsi": "21:10"
    }
    return jsonify(example)

@app.route('/api/collectapi', methods=['GET'])
def get_prayer_times_from_collectapi():
    city = request.args.get('city', 'istanbul')

    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        'content-type': "application/json",
        'authorization': f"apikey {API_KEY}"
    }

    try:
        conn.request("GET", f"/pray/all?data.city={city}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        return jsonify({
            "status": True,
            "city": city.title(),
            "source": "collectapi.com",
            "data": data.decode("utf-8")
        })
    except Exception as e:
        return jsonify({
            "status": False,
            "error": str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
