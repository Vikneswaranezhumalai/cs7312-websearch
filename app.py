from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")  # set in Render later
BING_URL = "https://api.bing.microsoft.com/v7.0/search"

@app.route('/search')
def search():
    query = request.args.get('q')
    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    params = {"q": query, "count": 10}
    response = requests.get(BING_URL, headers=headers, params=params)
    results = response.json().get("webPages", {}).get("value", [])
    return render_template("results.html", query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)
