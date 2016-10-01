import feedparser
from flask import Flask, render_template

app = Flask(__name__)

RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'nation': 'http://www.nation.co.ke/latestrss.rss'
}


@app.route('/')
@app.route('/<publication>')
def get_news(publication='nation'):
    feed = feedparser.parse(RSS_FEEDS[publication])
    print feed
    return render_template('index.html', articles=feed['entries'])


if __name__ == '__main__':
    app.run(debug=True)
