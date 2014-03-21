

IRCBot, because I haven't made one of those
================================

This started off life as the TestBot in the [Python IRC library] [1] project, but after I mangled it horribly, it does other stuff.

  [1]: https://pypi.python.org/pypi/irc       "PyIRC"
  
It needs Requests for fetching JSON for the Bitcoin pricing functionality, grab that with pip. 

        pip install requests

If you run into the bot complaining about not passing server, channel and name to it, you might need to escape the # in the channel name, like this:

        ./bot.py server.org \#channel name
