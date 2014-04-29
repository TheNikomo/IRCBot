from pyteaser import SummarizeUrl

def readNews(c, destination, url):
    summaries = SummarizeUrl(url)
    for summary in summaries:
        try:
            c.privmsg(destination, summary.decode('utf-8'))
        except Exception, e:
            print e
