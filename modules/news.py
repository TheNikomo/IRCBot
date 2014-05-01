from pyteaser import SummarizeUrl
import requests
from lxml import html

def readNews(c, destination, url):
    website = html.parse(url)
    title = website.find(".//title").text
    summaries = SummarizeUrl(url)

    c.privmsg(destination, title)

    i = 0
    for summary in summaries:
        if i < 2:
            try:
                c.privmsg(destination, summary.decode('utf-8'))
                i = i + 1
            except Exception, e:
                print e
