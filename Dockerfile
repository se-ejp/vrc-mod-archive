# 軽量版のPythonイメージを使用
FROM python:3.9-slim

# 作業ディレクトリを作成
WORKDIR /app

# --- [ここが爆速のポイント] ---
# 先にライブラリのインストールだけを済ませる
# これにより、app.pyを書き換えてもpip installは実行されず、キャッシュが使われます
RUN pip install flask

# その後にプログラム全体をコピー
# docker-compose.ymlでボリューム設定をしているなら、
# ビルド時にも最新の状態をコピーしておくと確実です
COPY . .

# 5000番ポートを使う
EXPOSE 5000

# プログラムを実行
CMD ["python", "app.py"]