from flask import Flask, render_template, request
import requests

app = Flask(__name__)
FBI_API_URL = "https://api.fbi.gov/wanted/v1/list"
cached_people = []

def format_person(person):
    return {
        "name": person.get("title", "Unknown"),
        "uid": person.get("uid", "Unknown"),
        "details": person.get("details", "Unknown."),
        "reward_text": person.get("reward_text", "Unknown"),
        "image": person.get("images", [{}])[0].get("original", "/static/placeholder.jpg")
    }

@app.route("/")
def index():
    global cached_people
    search = request.args.get("search", "")

    try:
        response = requests.get(FBI_API_URL)
        data = response.json()
        people = data.get("items", [])

        wanted_list = [format_person(p) for p in people]

        if search:
            wanted_list = [p for p in wanted_list if search.lower() in p["name"].lower()]

        wanted_list.sort(key=lambda x: x["name"])
        cached_people = wanted_list

        return render_template("index.html", wanted=wanted_list, search_text=search)
    except:
        return "Sorry, something went wrong.", 500

@app.route("/wanted/<uid>")
def wanted_detail(uid):
    for person in cached_people:
        if person["uid"] == uid:
            return render_template("detail.html", person=person)
    return "Person not found.", 404

if __name__ == "__main__":
    app.run(debug=True)