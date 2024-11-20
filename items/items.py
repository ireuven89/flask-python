import logging
from flask import Flask, jsonify, request

import database
import s3_upload

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)


@app.route('/items/<id>', methods=['GET'])
def get_item(id):
    result = database.get_item(id)
    return jsonify({result})

@app.route('/items', methods=['GET'])
def get_items():
    name = request.args.get('name')
    result = database.get_items(name)
    return jsonify({"items": result})

@app.route('/items', methods=['POST'])
def create_items():
    items = request.json
    result = database.insert_items(items)
    return jsonify({'success': result })

@app.route('/items', methods=['PUT'])
def update_items():
    items = request.json
    result = database.update_items(items)
    return jsonify({'items': result})

@app.route('/items/<id>', methods=['DELETE'])
def delete_items(id):
    result = database.delete_item(id)
    return jsonify({'item': result})

@app.route('/hello_world', methods=['GET'])
def hello_world():
    return jsonify({"hello": "world"})


@app.route('/health', methods=['GET'])
def healthcheck():
    return jsonify({"health": "ok", "mysql": status})


@app.route('/hello_world_post', methods=['POST'])
def hello_world_post():
    body = request.json
    logging.info("object saved", body)
    return jsonify({'status': 'ok'})


@app.route('/upload', methods= ['POST'])
def upload():
     file = request.files['file']
     result = s3_upload.upload_file(file)
     return result

def items_get():
    name = request.args.get('name')


if __name__ == '__main__':
    status = database.connect_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
