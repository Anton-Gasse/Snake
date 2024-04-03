from flask import Flask, send_file, request
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from stable_baselines3 import PPO
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)

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


@socketio.on('connect')
def connect():
    print('Connected')


@socketio.on('disconnect')
def disconnect():
    print('Disconnected')


@socketio.on('prediction')
def prediction(obs):
    if model == None:
        return "Currently no trained model available", 404
    else:
        prediction, _ = model.predict(tuple(eval(obs['obs'])))
        prediction = {'prediction': int(prediction)}
        emit("update", json.dumps(prediction, ensure_ascii=False))


if __name__ == '__main__':
    #context = ('./backend/ssl_keys/cert.pem', './backend/ssl_keys/key.pem')#certificate and key files
    cors = CORS(app, resources={r'*': {"origins": '*'}})
    
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, ssl_context='adhoc', host="0.0.0.0", port=443)
