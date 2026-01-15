import os
import json
import time
import signal  # 追加：終了信号を受け取るため
import sys     # 追加：システム終了のため
from datetime import datetime  # 冒頭の import 欄に追加してください
from flask import Flask, request, jsonify

app = Flask(__name__, static_folder='static', static_url_path='/static')

# --- 信号を受け取ったら即座に終了する設定 ---
def signal_handler(sig, frame):
    print('\nサーバーを終了します (SIGTERM/SIGINT受信)')
    sys.exit(0)

# Ctrl+C や Docker stop の合図を受け取れるようにする
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
# ------------------------------------------

# 保存用フォルダの設定
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

POSTS_FILE = 'posts.json'

def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(POSTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(load_posts())

@app.route('/api/posts', methods=['POST'])
def update_posts():
    # 全データの上書き保存（削除時などに使用）
    posts = request.json
    save_posts(posts)
    return jsonify({"status": "success"})

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['image']
    
    # 1. 今日の日付でフォルダ名を作る (例: 2026-01-15)
    today_folder = datetime.now().strftime('%Y-%m-%d')
    # 2. 保存先のフルパスを作る (static/uploads/2026-01-15)
    target_dir = os.path.join(UPLOAD_FOLDER, today_folder)
    
    # 3. フォルダがまだ存在しなかったら作成する
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # 4. ファイル名の重複防止
    filename = f"{int(time.time())}_{file.filename}"
    save_path = os.path.join(target_dir, filename)
    
    # 5. 保存
    file.save(save_path)
    
    # 6. ブラウザから見えるURLを返す (日付フォルダを含める)
    return jsonify({"url": f"/static/uploads/{today_folder}/{filename}"})

@app.route('/')
def index():
    # 最初のページを表示する
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def send_static(path):
    # index.html 以外のファイル (list.html, post.html など) を表示する
    return app.send_static_file(path)

if __name__ == '__main__':
    # hostを0.0.0.0にすることで、ngrokや外部からの接続を許可します
    app.run(host='0.0.0.0', port=5000)