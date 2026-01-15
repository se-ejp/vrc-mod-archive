import json
import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='static')

# 保存先ファイル名
DATA_FILE = 'posts.json'

# ★追加：起動時に posts.json がなければ空のリストで作る
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

# データを取得するAPI
@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        print(f"Error reading {DATA_FILE}: {e}")
        return jsonify([])  # エラー時は空リストを返す

# データを保存するAPI
@app.route('/api/posts', methods=['POST'])
def save_posts():
    try:
        data = request.json
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"Error saving {DATA_FILE}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)