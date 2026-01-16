import os
import json
import time
import signal
import sys
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__, static_folder='static', static_url_path='/static')

# --- 信号を受け取ったら即座に終了する設定 ---
def signal_handler(sig, frame):
    print('\nサーバーを終了します (SIGTERM/SIGINT受信)')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# --- 設定とファイルパス ---
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

POSTS_FILE = 'posts.json'
USERS_FILE = 'users.json'  # 追加：ユーザー保存用ファイル

# --- データ管理用関数 ---
def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(POSTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

# --- 投稿関連 API ---
@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(load_posts())

@app.route('/api/posts', methods=['POST'])
def update_posts():
    posts = request.json
    save_posts(posts)
    return jsonify({"status": "success"})

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files['image']
    today_folder = datetime.now().strftime('%Y-%m-%d')
    target_dir = os.path.join(UPLOAD_FOLDER, today_folder)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    filename = f"{int(time.time())}_{file.filename}"
    save_path = os.path.join(target_dir, filename)
    file.save(save_path)
    return jsonify({"url": f"/static/uploads/{today_folder}/{filename}"})

# --- ユーザー認証 API (新規追加) ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    users = load_users()
    if any(u['id'] == data['id'] for u in users):
        return jsonify({"status": "error", "message": "このIDは既に使用されています"}), 400
    
    users.append({
        "id": data['id'],
        "password": data['password'], # 本来は暗号化推奨
        "role": "user"
    })
    save_users(users)
    return jsonify({"status": "success"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    users = load_users()
    user = next((u for u in users if u['id'] == data['id'] and u['password'] == data['password']), None)
    
    if user:
        return jsonify({"status": "success", "user": user})
    else:
        return jsonify({"status": "error", "message": "IDまたはパスワードが正しくありません"}), 401

# --- 静的ファイル配信 ---
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def send_static(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)