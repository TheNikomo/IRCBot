#!/usr/bin/env python2

import resource
import inspect
import os
import random
import string
import irc.bot
import irc.strings
import bitcoin
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
        a = e.arguments[0].split(".")
        if len(a) > 1:
            self.do_command(e, a[1], "public")
        return

    def do_command(self, e, cmd, target):
        nick = e.source.nick
        c = self.connection

        if target == "private":
            destination = nick
        else:
            destination = self.channel

        if cmd == self.code:
            c.privmsg(self.channel, "Shutdown code detected.")
            print "Code accepted from " + nick + ", shutting off."
            self.die()

        elif cmd == "help":
            c.privmsg(destination, "Commands: .bitcoin, .bitcoin more, .status")

        elif cmd == "status":
            memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            c.privmsg(destination, "Currently using %s KiB of memory." % memory)

        elif cmd == "bitcoin":
            data = bitcoin.basic()
            message = nick + ": Bitcoin - Current: %s, %s - \".bitcoin more\" for more information" % (data['USD'], data['EUR'])
            c.privmsg(destination, message)

        elif cmd == "bitcoin more":

            data = bitcoin.advanced()

            c.privmsg(destination, nick + ": Bitcoin prices - USD from Bitstamp, EUR from Kraken")
            c.privmsg(destination, "Low: %s, %s - Average: %s, %s - High: %s, %s" % (data["USD"]["low"], data["EUR"]["low"], data["USD"]["avg"], data["EUR"]["avg"], data["USD"]["high"], data["EUR"]["high"], ))
            c.privmsg(destination, "24hr: %s, %s - 7d: %s, %s - 30d: %s, %s" % (data["USD"]["24h"], data["EUR"]["24h"], data["USD"]["7d"], data["EUR"]["7d"], data["USD"]["30d"], data["EUR"]["30d"], ))

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

    code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(24))

    bot = ChatBot(code, channel, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
