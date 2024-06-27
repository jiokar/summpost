import feedparser
import requests
import os
from openai import OpenAI
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# OpenAI APIキーとSlackのWebhook URL
client = OpenAI(
    api_key = os.getenv('OPENAI_API_KEY')
)
slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')

# ファイルからRSSフィードとキーワードを読み込む
def load_list_from_file(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file if line.strip()]

rss_feeds = load_list_from_file('src/rss_feeds.txt')
keywords = load_list_from_file('src/keywords.txt')

# 過去に確認したニュースURLを読み込む
def load_seen_articles(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return set(line.strip() for line in file if line.strip())
    return set()

# 確認済みのニュースURLを保存する
def save_seen_articles(filepath, articles):
    with open(filepath, 'a') as file:
        for article in articles:
            file.write(article + '\n')

seen_articles_filepath = 'src/seen_articles.txt'
seen_articles = load_seen_articles(seen_articles_filepath)

# ニュース記事の取得とキーワードフィルタリング
def fetch_news(rss_feeds, keywords, seen_articles):
    new_articles = []
    for feed in rss_feeds:
        d = feedparser.parse(feed)
        for entry in d.entries:
            if entry.link not in seen_articles:
                content = entry.get('summary', entry.get('description', ''))
                for keyword in keywords:
                    if keyword.lower() in entry.title.lower() or keyword.lower() in content.lower():
                        new_articles.append({
                            'title': entry.title,
                            'link': entry.link,
                            'summary': content,
                            'source': d.feed.title
                        })
                        seen_articles.add(entry.link)
    return new_articles

# OpenAI APIを使用して要約を生成
def summarize_article(article):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"以下のニュース記事を300文字以内で要約してください。\n\nタイトル: {article['title']}\n\n{article['summary']}"}
        ],
        stream=True,
    )
    summary =""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            summary += chunk.choices[0].delta.content
    return summary

# Slackに投稿
def post_to_slack(article, summary):
    attachments = [
        {
            "fallback": "New article from RSS feed",
            "color": "#36a64f",
            "author_name": article['source'],
            "title": article['title'],
            "title_link": article['link'],
            "text": summary
        }
    ]
    message = {
        "attachments": attachments
    }
    print("message=",message,"\n")
    response = requests.post(slack_webhook_url, json=message)
    if response.status_code != 200:
        raise Exception(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

# メイン処理
def main():
    articles = fetch_news(rss_feeds, keywords, seen_articles)
    for article in articles:
        summary = summarize_article(article)
        post_to_slack(article, summary)
#        post_to_slack(summary, article['link'])
    save_seen_articles(seen_articles_filepath, [article['link'] for article in articles])

if __name__ == "__main__":
    main()
