from flask import Flask, jsonify, request
import http.client
import urllib.parse
import os

app = Flask(__name__)

# .env dosyasından ya da doğrudan yazılmış API Key
API_KEY = os.getenv("COLLECTAPI_KEY", "your_token")


@app.route("/")
def home():
    return "API is working!"


@app.route("/pray/single", methods=["GET"])
def get_single_prayer_time():
    city = request.args.get("city", "istanbul")
    vakit = request.args.get("vakit", "Yatsı")  # İmsak, Güneş, Öğle, İkindi, Akşam, Yatsı

    # Şehir ve vakit adlarını URL uyumlu hale getiriyoruz
    encoded_city = urllib.parse.quote(city)
    encoded_vakit = urllib.parse.quote(vakit)

    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        'content-type': "application/json",
        'authorization': f"apikey {API_KEY}"
    }

    try:
        conn.request("GET", f"/pray/single?ezan={encoded_vakit}&data.city={encoded_city}", headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        return jsonify({
            "status": True,
            "city": city.title(),
            "vakit": vakit.title(),
            "data": data
        })
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

