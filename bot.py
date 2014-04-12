#!/usr/bin/env python2

import resource
import requests
import inspect
import os
import random
import string
import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

class ChatBot(irc.bot.SingleServerIRCBot):
    def __init__(self, code, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.code = code

    def on_nicknameinuse(self, c, e):
        raise RuntimeError("Nickname in use, failing spectacularly")
        self.die()

    def on_welcome(self, c, e):
        c.join(self.channel)
        print "Self-destruct code: " + self.code

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0], "private")

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip(), "public")
        return

    def do_command(self, e, cmd, target):
        nick = e.source.nick
        c = self.connection
        print target + " - " + nick + ": " + cmd

        if target == "private":
            destination = nick
        else:
            destination = self.channel

        if cmd == self.code:
            c.privmsg(self.channel, "Self-destruct code detected, exploding into bits.")
            self.die()

        elif cmd == "status":
            memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            c.privmsg(destination, "Currently using %s KiB of memory." % memory)

        elif cmd == "help":
            c.privmsg(destination, "Commands: bitcoin, bitcoin more, status")

        elif cmd == "bitcoin":
            euro=u'\u20ac'
            data = requests.get("http://nikomo.fi/markets.json").json()
            USD = filter(lambda x:x["symbol"]=="bitstampUSD", data)
            EUR = filter(lambda x:x["symbol"]=="krakenEUR", data)

            USDcur = round(USD[0]['close'], 2)
            EURcur = round(EUR[0]['close'], 2)


            message = nick + ": Bitcoin - Current: $%.2f, %.2f%s - \"bitcoin more\" for more information" % (USDcur, EURcur, euro)

            c.privmsg(destination, message)

        elif cmd == "bitcoin more":
            euro=u'\u20ac'

            data = requests.get("http://nikomo.fi/markets.json").json()
            prices = requests.get("http://nikomo.fi/weighted_prices.json").json()

            USDmarket = filter(lambda x:x["symbol"]=="bitstampUSD", data)
            EURmarket = filter(lambda x:x["symbol"]=="krakenEUR", data)

            USD7d = "$" + prices['USD']['7d']
            USD30d = "$" + prices['USD']['30d']
            USD24h = "$" + prices['USD']['24h']

            EUR7d = prices['EUR']['7d'] + euro
            EUR30d = prices['EUR']['30d'] + euro 
            EUR24h = prices['EUR']['24h'] + euro

            USDlow = "$" + str(round(USDmarket[0]['low'], 2))
            USDavg = "$" + str(round(USDmarket[0]['avg'], 2))
            USDhigh = "$" + str(round(USDmarket[0]['high'], 2))

            EURlow = str(round(EURmarket[0]['low'], 2)) + euro
            EURavg = str(round(EURmarket[0]['avg'], 2)) + euro
            EURhigh = str(round(EURmarket[0]['high'], 2)) + euro

            c.privmsg(destination, nick + ": Bitcoin prices - USD from Bitstamp, EUR from Kraken")
            c.privmsg(destination, "Low: %s, %s - Average: %s, %s - High: %s, %s" % (USDlow, EURlow, USDavg, EURavg, USDhigh, EURhigh))
            c.privmsg(destination, "24hr: %s, %s - 7d: %s, %s - 30d: %s, %s" % (USD24h, EUR24h, USD7d, EUR7d, USD30d, EUR30d))
        else:
            c.privmsg(nick, "Not understood: " + cmd)

def main():
    import sys
    if len(sys.argv) != 4:
        print("Usage: " + inspect.getfile(inspect.currentframe()) + " <server[:port]> <channel> <nickname>")
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print("Error: Erroneous port.")
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    nickname = sys.argv[3]

    code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

    bot = ChatBot(code, channel, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
