# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係をコピーしてインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 必要なファイルをコピー
COPY src ./src
COPY .env ./

# スクリプトを実行
CMD ["python", "src/news_to_slack.py"]
