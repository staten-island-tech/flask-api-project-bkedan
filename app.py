from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():

    response = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php")
    data = response.json()

    cards_data = data['data'][:20]

    yugioh = []
    for card in cards_data:
        yugioh.append({
            'name': card['name'],
            'id': card['id'],
            'image': card['card_images'][0]['image_url']
        })

    return render_template("index.html", yugioh=yugioh)

@app.route("/yugioh/<int:id>")
def yugioh_detail(id):
    response = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={id}")
    data = response.json()
    
    if 'data' not in data:
        return "Card not found", 404

    card = data['data'][0]


    name = card.get('name')
    type_ = card.get('type')
    desc = card.get('desc')
    atk = card.get('atk', 'N/A')
    def_ = card.get('def', 'N/A')
    level = card.get('level', 'N/A')
    image_url = card['card_images'][0]['image_url']

    return render_template("yugioh.html", card={
        'name': name,
        'type': type_,
        'desc': desc,
        'atk': atk,
        'def': def_,
        'level': level,
        'image': image_url
    })

if __name__ == '__main__':
    app.run(debug=True)
