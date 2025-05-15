from flask import Flask, render_template
import requests

app = Flask(__name__)
FBI_API_URL = "https://api.fbi.gov/wanted/v1/list"
cached_people = []  # Store fetched people for quick UID lookup

@app.route("/")
def index():
    global cached_people
    try:
        response = requests.get(FBI_API_URL, params={"page": 1})
        response.raise_for_status()
        data = response.json()
        people = data.get("items", [])

        wanted_list = []
        for person in people:
            wanted_list.append({
                "name": person.get("title", "Unknown"),
                "uid": person.get("uid"),
                "details": person.get("details", ""),
                "reward_text": person.get("reward_text", ""),
                "image": person.get("images", [{}])[0].get("original", "/static/placeholder.jpg")
            })

        cached_people = wanted_list  # Store for later lookup
        return render_template("index.html", wanted=wanted_list)
    except requests.RequestException as e:
        return f"Error fetching FBI data: {e}", 500

@app.route("/wanted/<uid>")
def wanted_detail(uid):
    person = next((p for p in cached_people if p["uid"] == uid), None)
    if not person:
        return "Person not found", 404
    return render_template("detail.html", person=person)

if __name__ == "__main__":
    app.run(debug=True)
