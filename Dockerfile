# Pythonの入った箱をベースにする
FROM python:3.9-slim

# 作業するフォルダを決める
WORKDIR /app

# 必要なプログラムをコピー
COPY app.py .
COPY static/ ./static/

# 必要なライブラリをインストール
RUN pip install flask

# 5000番ポートを使う
EXPOSE 5000

# プログラムを実行
CMD ["python", "app.py"]