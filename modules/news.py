from pyteaser import SummarizeUrl
import requests
from lxml import html

def readNews(c, destination, url):
    website = html.parse(url)
    title = website.find(".//title").text

    try:
        summaries = SummarizeUrl(url)
    except Exception, e:
        print e
        return

    c.privmsg(destination, title)

    i = 0
    try:
        for summary in summaries:
            if i < 2:
                try:
                    c.privmsg(destination, summary.decode('utf-8'))
                    i = i + 1
                except Exception, e:
                    print e
    except Exception, e:
        print e