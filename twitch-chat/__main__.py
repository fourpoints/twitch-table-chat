import sys, os

from table import TABLE
from comment import post_comments
from twitch_socket import TwitchSocket

#---- PROGRAM PARAMETERS -------------------------------------------------------

SERVER   = "irc.chat.twitch.tv"
PORT     = 6667 # 6697 (SSL), 6667 (otherwise)

TOKEN    = "oauth:<code>"
USERNAME = "<nickname>"
CHANNEL  = "#<channelname>"

address = (SERVER, PORT)
data = f"PASS {TOKEN}\n NICK {USERNAME}\n JOIN {CHANNEL}\n".encode("utf-8")

WAIT = 2 # update every {WAIT} seconds
assert WAIT >= 2 # max 20 messages every 30rd second (source?)


if __name__ == "__main__":
    try:
        twitchSocket = TwitchSocket(address=address, data=data)

        for responses in twitchSocket.stream_responses(sleep_length=WAIT):
            post_comments(responses)

    except KeyboardInterrupt:
        # Move the cursor to the bottom-left corner
        TABLE.reset_cursor()
        print("Exiting on keyboard interrupt.")

        twitchSocket.close()

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
