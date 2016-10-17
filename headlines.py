import datetime
import feedparser
from flask import Flask, render_template, request, make_response, redirect
import json
from keys import WEATHER_URL
import urllib2
import urllib

app = Flask(__name__)

# links for rss feeds
RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
}

# default publication and city
DEFAULTS = {'publication': 'bbc',
            'city': 'Nairobi, KE'}


# main page
@app.route('/')
def home():
    publication = get_value_with_fallback('publication')
    articles = get_news(publication)
    city = get_value_with_fallback('city')
    weather = get_weather(city)

    for i in range(len(articles)):
        a = articles[i].get('media_content') or articles[i].get('media_thumbnail')
        if a is None:
            continue
        else:
            articles[i]['image'] = a[0]['url']

    response = make_response(render_template('index.html', articles=articles, weather=weather))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie('publication', publication, expires=expires)
    response.set_cookie('city', city, expires=expires)
    return response


# reads the xml data provided by the rss feeds and converts it to json
def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


# retreives data from weather api
def get_weather(query):
    # escapes special charachters in url
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    # opens the url provided and reads it
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {
            'description': parsed['weather'][0]['description'],
            'temperature': parsed['main']['temp'],
            'city': parsed['name'],
            'country': parsed['sys']['country']
        }
    return weather


# provides a fallback for all requests made by user, if no request made fallbacks to DEFAULTS
def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]

x = feedparser.parse(RSS_FEEDS['bbc'])
print x

if __name__ == '__main__':
    app.run(debug=True)
