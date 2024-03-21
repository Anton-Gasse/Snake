from flask import Flask, send_file, request
from flask_cors import CORS, cross_origin
from stable_baselines3 import PPO
import json
import os

app = Flask(__name__)

model = PPO.load(os.path.join("backend", "snake-rl", "models", "first_model.zip"))

@app.route('/')
def game():
    with open(os.path.join("frontend", "build", "web", "index.html"), "r", encoding='utf-8') as s:
        return s.read()

@app.route('/frontend.apk')
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def test_build():
    return send_file(os.path.join("..", "frontend", "build", "web", "frontend.apk"))


@app.route('/favicon.png')
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def favicon():
    return send_file(os.path.join("..", "frontend", "build", "web", "favicon.png"))


@app.route('/prediction', methods=['POST'])
def prediction():
    obs = request.get_json()['obs']
    if model == None:
        return "Currently no trained model available", 404
    else:
        prediction, _ = model.predict(obs)
        prediction = {'prediction': int(prediction)}
        return json.dumps(prediction, ensure_ascii=False)

if __name__ == '__main__':
    #context = ('./ssl_keys/cert.pem', './ssl_keys/key.pem')#certificate and key files
    cors = CORS(app, resources={r'*': {"origins": '*'}})
    
    app.run(debug=True, ssl_context='adhoc', host="0.0.0.0", port=443)
