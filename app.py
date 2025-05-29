from flask import Flask, render_template, abort
import requests

app = Flask(__name__)

@app.route("/")
def index():
    response = requests.get("https://valorant-api.com/v1/playercards")
    data = response.json()

    cards_data = data['data'][:1000]
    cards = []
    for card in cards_data:
        cards.append({
            'uuid': card['uuid'],
            'name': card['displayName'],
            'image': card['largeArt'],
            'description': card.get('description', 'No description available.') 
        })
    return render_template("index.html", cards=cards)

@app.route("/card/<uuid>")
def valorant_detail(uuid):
    response = requests.get(f"https://valorant-api.com/v1/playercards/{uuid}")
    if response.status_code != 200:
        abort(404)
    card = response.json()['data']
    card_info = {
        'name': card['displayName'],
        'image': card['largeArt'],
        'wide_image': card['wideArt'],
        'small_image': card['smallArt'],
        'description': card.get('description', 'No description available.') 
    }
    return render_template("valorant.html", card=card_info)

if __name__ == '__main__':
    app.run(debug=True)