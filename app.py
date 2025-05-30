from flask import Flask, render_template, abort
import requests

app = Flask(__name__)

@app.route("/")
def index():
    response = requests.get("https://api.sampleapis.com/simpsons/episodes")
    if response.status_code != 200:
        abort(500, "Failed to fetch episode data")

    data = response.json()
    raw_episodes = data[:10000]  


    episodes = []
    for ep in raw_episodes:
        episodes.append({
            'id': ep.get('id'),
            'title': ep.get('name', 'Untitled'),
            'season': ep.get('season', 'Unknown'),
            'episode': ep.get('episode', 'Unknown'),
            'description': ep.get('description', 'No description available.'),
            'thumbnail': ep.get('thumbnailUrl', '/static/images/placeholder.jpg')
        })
    return render_template("index.html", episodes=episodes)
@app.route("/episode/<int:episode_id>")
def episode_detail(episode_id):
    response = requests.get("https://api.sampleapis.com/simpsons/episodes")
    if response.status_code != 200:
        abort(500, "Failed to fetch episode data")

    episodes = response.json()
    episode = next((ep for ep in episodes if ep.get('id') == episode_id), None)

    if episode is None:
        abort(404, "Episode not found")

    return render_template("episode.html", episode=episode)

if __name__ == '__main__':
    app.run(debug=True)