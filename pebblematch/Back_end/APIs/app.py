#!/usr/bin/python3

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "pebble2023"

jwt = JWTManager(app)

@app.route("/resource", methods=["GET"])
def get_resource():
    return "Data"

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username != "admin" or password != "password":
        return jsonify(msg="Invalid username or password!"), 401

    return "Access Token"


if __name__ == "__main__":
    app.run(debug=True)