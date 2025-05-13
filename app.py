from flask import Flask, render_template, abort
import requests

app = Flask(__name__)

@app.route("/")
def index():
    response = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php")
    data = response.json()
    cards_data = data['data'][:1000]
    yugioh = []
    for card in cards_data:
        yugioh.append({
            'name': card['name'],
            'image': card['card_images'][0]['image_url']
        })
    return render_template("index.html", yugioh=yugioh)

@app.route("/yugioh/<int:id>")
def yugioh_detail(id):
    response = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={id}")
    data = response.json()
    if 'data' not in data or len(data['data']) == 0:
        abort(404)
    card = data['data'][0]
    card_info = {
        'name': card['name'],
        'image': card['card_images'][0]['image_url'],
        'desc': card.get('desc', 'No description available.'),
        'type': card.get('type', 'Unknown')
    }

    return render_template("detail.html", card=card_info)

if __name__ == '__main__':
    app.run(debug=True)
