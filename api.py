import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth

from main import get_random_bookmarks, get_random_bookmarks_in_last_days

api = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')
CORS(api)

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

tokens = {
    os.getenv('TOKEN'): "api-key"
}


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@auth.error_handler
def auth_error(status):
    return jsonify({"error": status, "message": "Unauthorized"})


@api.route('/health')
def hello_world():
    return jsonify({"server status": "UP"})


@api.route('/latest', methods=['POST'])
@auth.login_required
def latest_raindrops():

    return jsonify({"message": "hello world", "body": request.get_json()})


@api.route('/random/<number>', methods=['GET'])
@auth.login_required
def random_raindrops(number):
    return jsonify(get_random_bookmarks(int(number)))


@api.route('/random/<number>/days/<days>', methods=['GET'])
@auth.login_required
def random_recent_raindrops(number, days):
    return jsonify(get_random_bookmarks_in_last_days(int(number), int(days)))


if __name__ == '__main__':
    api.run(port=5000)
