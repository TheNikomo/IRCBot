import requests

def basic():
    euro = u'\u20ac'
    data_request = requests.get("http://nikomo.fi/markets.json").json()

    USDdata = filter(lambda x:x["symbol"]=="bitstampUSD", data_request)
    EURdata = filter(lambda x:x["symbol"]=="krakenEUR", data_request)

    USDcur = round(USDdata[0]['close'], 2)
    EURcur = round(EURdata[0]['close'], 2)

    USD = "$" + str(USDcur)
    EUR = str(EURcur) + euro

    return dict([('USD', USD), ('EUR', EUR)])

def advanced():
    euro=u'\u20ac'

    data_request = requests.get("http://nikomo.fi/markets.json").json()
    prices_request = requests.get("http://nikomo.fi/weighted_prices.json").json()

    USDmarket = filter(lambda x:x["symbol"]=="bitstampUSD", data_request)
    EURmarket = filter(lambda x:x["symbol"]=="krakenEUR", data_request)

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

    return dict([("EUR", EUR),("USD",USD)])
