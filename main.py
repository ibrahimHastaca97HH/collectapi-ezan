from flask import Flask, request, jsonify
import http.client
import os

app = Flask(__name__)

API_KEY = os.getenv("COLLECTAPI_KEY", "your_token")

@app.route('/api/collectapi', methods=['GET'])
def get_prayer_times():
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
        return jsonify({"status": True, "data": data.decode("utf-8")})
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
