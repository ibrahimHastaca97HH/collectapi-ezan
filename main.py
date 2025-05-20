from flask import Flask, jsonify, request
import http.client
import urllib.parse
import os
import json

app = Flask(__name__)

# CollectAPI KEY'i buradan çekiyoruz (.env ile uyumlu)
API_KEY = os.getenv("COLLECTAPI_KEY", "your_token")


@app.route("/")
def home():
    return "API is working!"


# Tek vakit isteği: /pray/single?city=istanbul&vakit=Yatsı
@app.route("/pray/single", methods=["GET"])
def get_single_prayer_time():
    city = request.args.get("city", "istanbul")
    vakit = request.args.get("vakit", "Yatsı")

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
        json_data = json.loads(data)
        return jsonify({
            "status": True,
            "city": city.title(),
            "vakit": vakit.title(),
            "time": json_data.get("result", {}).get("time", "N/A")
        })
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})


# Tüm vakitler: /pray/istanbul
@app.route("/pray/<city>", methods=["GET"])
def get_prayer_times(city):
    encoded_city = urllib.parse.quote(city)

    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        'content-type': "application/json",
        'authorization': f"apikey {API_KEY}"
    }

    try:
        conn.request("GET", f"/pray/all?data.city={encoded_city}", headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        json_data = json.loads(data)

        result = json_data.get("result", [{}])[0]  # İlk günün verisi

        return jsonify({
            "status": True,
            "city": city.title(),
            "date": result.get("date", "N/A"),
            "imsak": result.get("saatler", {}).get("imsak", "N/A"),
            "gunes": result.get("saatler", {}).get("gunes", "N/A"),
            "ogle": result.get("saatler", {}).get("ogle", "N/A"),
            "ikindi": result.get("saatler", {}).get("ikindi", "N/A"),
            "aksam": result.get("saatler", {}).get("aksam", "N/A"),
            "yatsi": result.get("saatler", {}).get("yatsi", "N/A")
        })
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


