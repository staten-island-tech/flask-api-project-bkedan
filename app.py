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