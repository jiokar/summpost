# summpost : Summary Post

## What's this?
- This is a container posts RSS news summarized OpenAI API to specify slack ch.

## Requirements
- feedparser
- openai
- requests
- python-dotenv

## Usage
- Preconfigure
    - Write your interesting newssites rss url to **rss_feeds.txt**
    - Write your interesting keywords to **keywords.txt**
    - Make your **.env** file
- Deploy docker container
- Then post summarize news to your slack ch
