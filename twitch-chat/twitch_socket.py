import socket
from time import sleep, time as timestamp
from itertools import count

#---- TWITCH API ---------------------------------------------------------------

class TwitchSocket:
    def __init__(self, address, data):
        self.socket = self._connect_to_Twitch(address, data)

    def _connect_to_Twitch(self, address, data):
        TwitchSocket = socket.socket()

        # bug: takes no keyword arguments
        TwitchSocket.connect(address)
        TwitchSocket.sendall(data)

        return TwitchSocket

    def _get_responses(self):
        bufsize = 2048 # buffer size; may need to be increased with long nick
        responses = self.socket.recv(bufsize).decode("utf-8")

        # if not new_responses: print(responses)
        # responses = new_responses

        if responses.startswith("PING"):
            # matches "PING :tmi.twitch.tv"
            self.socket.send("PONG".encode("utf-8"))

        return responses

    def stream_responses(self, sleep_length):
        """This is a slightly more accurate way to sleep 2 seconds between
        every response call, as sleep(sleep_length) would be 2 seconds +
        the time it takes to call get_responses(), as it can take 2+ seconds."""
        start_time = timestamp()

        for step in count(1):
            yield self._get_responses()

            sleep_until = start_time  + step*sleep_length
            sleep_time  = sleep_until - timestamp()

            sleep(max(1, sleep_time))

    def close(self):
        self.socket.close()
