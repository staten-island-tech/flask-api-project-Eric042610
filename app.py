from flask import Flask, render_template
import requests

app = Flask(__name__)

POKEMON_API_URL = "https://pokeapi.co/api/v2/pokemon"

@app.route("/")
def index():
    try:
        response = requests.get(f"{POKEMON_API_URL}?limit=150")
        response.raise_for_status()
        data = response.json()
        pokemon_list = data['results']

        pokemons = []
        for pokemon in pokemon_list:
            url = pokemon['url']
            id = url.strip("/").split("/")[-1]
            # Use official artwork
            image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png"
            pokemons.append({
                'name': pokemon['name'].capitalize(),
                'id': id,
                'image': image_url
            })

        return render_template("index.html", pokemons=pokemons)
    except requests.RequestException as e:
        return f"Error fetching Pokémon data: {e}", 500

@app.route("/pokemon/<int:id>")
def pokemon_detail(id):
    try:
        response = requests.get(f"{POKEMON_API_URL}/{id}")
        response.raise_for_status()
        data = response.json()

        types = [t['type']['name'].capitalize() for t in data['types']]
        height = data.get('height')
        weight = data.get('weight')
        name = data.get('name').capitalize()
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png"
        stat_names = [stat['stat']['name'].capitalize() for stat in data['stats']]
        stat_values = [stat['base_stat'] for stat in data['stats']]

        return render_template("pokemon.html", pokemon={
            'name': name,
            'id': id,
            'image': image_url,
            'types': types,
            'height': height,
            'weight': weight,
            'stat_names': stat_names,
            'stat_values': stat_values
        })
    except requests.RequestException as e:
        return f"Error fetching Pokémon detail: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
