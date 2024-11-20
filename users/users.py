from flask import Flask, render_template, request, redirect, url_for, jsonify

import database
app = Flask(__name__)

@app.route("/users/<id>", methods=["GET"])
def get_user(id):
    results = database.get_user(id)
    return jsonify({"users": results})

@app.route("/users", methods=["GET"])
def get_users():
    name = request.args.get('name')
    results = database.get_users(name)
    return jsonify({"users": results})

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    results = database.create_users(data)
    return jsonify({"users": results})

@app.route("/users", methods=["PUT"])
def update_user():
    data = request.get_json()
    results = database.update_users(data["username"], data["email"], data["password"])
    return jsonify(results)

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    results = database.delete_users(id)
    return jsonify(results)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"health": "ok", "mysql": status})


if __name__ == '__main__':
    status = database.connect_db()
    app.run(port=3000, host='0.0.0.0', debug=True)