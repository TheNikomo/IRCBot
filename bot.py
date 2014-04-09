#! /usr/bin/env python2

import resource
import requests
import inspect
import os
import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

class ChatBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        raise RuntimeError("Nickname in use, failing spectacularly")
        self.die()

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip())
        return

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection
        print nick + ": " + cmd


        if cmd == "leave":
        	if nick == "nikomo":
        		c.privmsg(self.channel, "Shutting down.")
        		self.die()
        	else:
        		c.privmsg(self.channel, "Not authorized.")
                print nick + " tried to shut me down"

        elif cmd == "status":
            memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            c.privmsg(self.channel, "Currently using %s KiB of memory." % memory)

        elif cmd == "help":
            c.privmsg(self.channel, "Commands: bitcoin, bitcoin more, status")

        elif cmd == "bitcoin":
            euro=u'\u20ac'
            data = requests.get("http://nikomo.fi/markets.json").json()
            USD = filter(lambda x:x["symbol"]=="bitstampUSD", data)
            EUR = filter(lambda x:x["symbol"]=="krakenEUR", data)

            USDcur = round(USD[0]['close'], 2)
            EURcur = round(EUR[0]['close'], 2)


            message = nick + ": Bitcoin - Current: $%.2f, %.2f%s - \"bitcoin more\" for more information" % (USDcur, EURcur, euro)

            c.privmsg(self.channel, message)

        elif cmd == "bitcoin more":
            euro=u'\u20ac'
            data = requests.get("http://nikomo.fi/markets.json").json()
            USDmarket = filter(lambda x:x["symbol"]=="bitstampUSD", data)
            EURmarket = filter(lambda x:x["symbol"]=="krakenEUR", data)

            USDlow = round(USDmarket[0]['low'], 2)
            USDavg = round(USDmarket[0]['avg'], 2)
            USDhigh = round(USDmarket[0]['high'], 2)

            EURlow = round(EURmarket[0]['low'], 2)
            EURavg = round(EURmarket[0]['avg'], 2)
            EURhigh = round(EURmarket[0]['high'], 2)

            #worth = str('{:,}'.format(round(market[0]['volume']*market[0]['avg'], 2)))

            c.privmsg(self.channel, "Low: $%.2f - Average: $%.2f - High: $%.2f" % (USDlow, USDavg, USDhigh))
            c.privmsg(self.channel, "Low: %.2f%s - Average: %.2f%s - High: %.2f%s" % (EURlow, euro, EURavg, euro, EURhigh, euro))
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

    bot = ChatBot(channel, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
