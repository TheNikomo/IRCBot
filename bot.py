#!/usr/bin/env python2

import resource
import inspect
import os
import random
import string
import irc.bot
import irc.strings
import modules.bitcoin as bitcoin
import modules.news as news
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
        print("Self-destruct code: " + self.code)

    def on_privmsg(self, c, e):
        a = e.arguments[0].split("!")
        if len(a) > 1:
            self.do_command(e, a[1], "private")
        if e.arguments[0] == self.code:
            self.die()
        return

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split("!")
        if len(a) > 1:
            self.do_command(e, a[1], "public")
        if e.arguments[0] == self.code:
            self.die()
        return

    def do_command(self, e, cmd, target):
        nick = e.source.nick
        c = self.connection
        channel = self.channel

        argcmd = cmd.split(" ")

        if target == "private":
            client = nick
        else:
            client = channel

        if cmd == self.code:
            print("Code accepted from " + nick + ", shutting off.")
            self.die()

        elif cmd == "help":
            c.privmsg(client, "Commands: !bitcoin, !status, !help")

        elif cmd == "status":
            memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            c.privmsg(client, "Currently using %s KiB of memory." % memory)

        elif cmd == "bitcoin":
            if client == nick:
                bitcoin.sendPrivatePrices(c, nick)
            if client == channel:
                bitcoin.sendPublicPrices(c, channel, nick)
                bitcoin.sendPrivatePrices(c, nick)

        elif argcmd[0] == "news":
            news.readNews(c, client, argcmd[1]) #argcmd: 0 - command, 1 - url


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
