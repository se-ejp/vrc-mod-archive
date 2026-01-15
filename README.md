# VRC改変アーカイブ

VRChatのアバター改変記録を保存・閲覧するためのツールです。
Dockerを使用して、誰でも同じ環境で動かすことができます。

## 構成
- **Frontend**: HTML / CSS / JavaScript (staticフォルダ内)
- **Backend**: Python Flask (データをJSONで保存)
- **Environment**: Docker

## 使い方（起動方法）

このフォルダで以下のコマンドを実行してください。

### 1. イメージの作成（初回・変更時のみ）
```bash
docker build -t vrc-archive .