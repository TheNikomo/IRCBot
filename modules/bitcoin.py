import requests

def sendBasicPrices(c, nick, destination):
    euro = u'\u20ac'
    try:
        data_request = requests.get("http://nikomo.fi/markets.json").json()
    except requests.exceptions.RequestException:
        c.privmsg(destination, "Unable to get price data, %s" % nick)
        return

    USDdata = list(filter(lambda x:x["symbol"]=="bitstampUSD", data_request))
    EURdata = list(filter(lambda x:x["symbol"]=="krakenEUR", data_request))

    USDcur = round(USDdata[0]['close'], 2)
    EURcur = round(EURdata[0]['close'], 2)

    USD = "$" + str(USDcur)
    EUR = str(EURcur) + euro

    data = dict([('USD', USD), ('EUR', EUR)])

    message = nick + ": Bitcoin - Current: %s, %s - \"!bitcoin more\" for more information" % (data['USD'], data['EUR'])
    c.privmsg(destination, message)

def sendAdvancedPrices(c, nick, destination):
    euro=u'\u20ac'

    try:
        data_request = requests.get("http://nikomo.fi/markets.json").json()
    except requests.exceptions.RequestException:
        c.privmsg(destination, "Unable to get price data, %s" % nick)
        return

    try:
        prices_request = requests.get("http://nikomo.fi/weighted_prices.json").json()
    except requests.exceptions.RequestException:
        c.privmsg(destination, "Unable to get price data, %s" % nick)
        return

    USDmarket = list(filter(lambda x:x["symbol"]=="bitstampUSD", data_request))
    EURmarket = list(filter(lambda x:x["symbol"]=="krakenEUR", data_request))

    USD7d = "$" + str(prices_request['USD']['7d'])
    USD30d = "$" + str(prices_request['USD']['30d'])
    USD24h = "$" + str(prices_request['USD']['24h'])

    EUR7d = str(prices_request['EUR']['7d']) + euro
    EUR30d = str(prices_request['EUR']['30d']) + euro 
    EUR24h = str(prices_request['EUR']['24h'] )+ euro

    USDlow = "$" + str(round(USDmarket[0]['low'], 2))
    USDavg = "$" + str(round(USDmarket[0]['avg'], 2))
    USDhigh = "$" + str(round(USDmarket[0]['high'], 2))

    EURlow = "%.2f%s" % (round(EURmarket[0]['low'], 2), euro)
    EURavg = "%.2f%s" % (round(EURmarket[0]['avg'], 2), euro)
    EURhigh = "%.2f%s" % (round(EURmarket[0]['high'], 2), euro)

    EUR = dict([("low", EURlow), ("avg", EURavg), ("high", EURhigh), ("24h", EUR24h), ("7d", EUR7d), ("30d", EUR30d)])
    USD = dict([("low", USDlow), ("avg", USDavg), ("high", USDhigh), ("24h", USD24h), ("7d", USD7d), ("30d", USD30d)])

    data = dict([("EUR", EUR),("USD",USD)])

    c.privmsg(destination, nick + ": Bitcoin prices - USD from Bitstamp, EUR from Kraken")
    c.privmsg(destination, "Low: %s, %s - Average: %s, %s - High: %s, %s" % (data["USD"]["low"], data["EUR"]["low"], data["USD"]["avg"], data["EUR"]["avg"], data["USD"]["high"], data["EUR"]["high"], ))
    c.privmsg(destination, "24hr: %s, %s - 7d: %s, %s - 30d: %s, %s" % (data["USD"]["24h"], data["EUR"]["24h"], data["USD"]["7d"], data["EUR"]["7d"], data["USD"]["30d"], data["EUR"]["30d"], ))
