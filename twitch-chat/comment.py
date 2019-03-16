from table import TABLE
from datetime import datetime
import re

NICK_WIDTH = 37
try:
    from styleprint import sformat
    NICK_WIDTH += 14 # includes format width of nick+time
except ImportError:
    def sformat(string, **format): return string

#---- COMMENT FORMATTER --------------------------------------------------------

def border(): TABLE.printrow(f"├─{'─'*TABLE.text_width}─┤")


def split(message, split_width):
    i = 0
    while i <= len(message):
        try:
            # Skip spaces at the beginning of a line
            i += next(j for j, c in enumerate(message[i:]) if not c.isspace())
        except StopIteration:
            pass

        # Try to find a space near the end (-1 is return if none are found)
        s = message[i+split_width-3:i+split_width+1].find(' ')

        # Start a newline if there is a space near the end
        if s > 0:
            yield message[i:i+split_width-3+s]
            i += split_width-3+s

        # If the message ends we just return (yield) it
        elif len(message[i:]) < split_width:
            yield message[i:]
            i += split_width

        # Otherwise we hyphenate the line
        else:
            yield message[i:i+split_width-1] + '-'
            i += split_width - 1

def closest_color(r, g, b):
    """Given a triple (0-255, 0-255, 0-255), computes the L2-closest color"""
    colors = {
        (0x00, 0x00, 0x00) : 'black',
        (0x80, 0x00, 0x00) : 'darkred',
        (0x00, 0x80, 0x00) : 'darkgreen',
        (0x80, 0x80, 0x00) : 'darkyellow',
        (0x00, 0x00, 0x80) : 'blue',
        (0x80, 0x00, 0x80) : 'darkmagenta',
        (0x00, 0x80, 0x80) : 'darkcyan',
        (0xC0, 0xC0, 0xC0) : 'lightgrey',
        (0x80, 0x80, 0x80) : 'grey',
        (0x40, 0x40, 0x40) : 'darkgrey',
        (0xF0, 0x00, 0x00) : 'red',
        (0x00, 0xF0, 0x00) : 'green',
        (0xF0, 0xF0, 0x00) : 'yellow',
        (0x00, 0x00, 0xF0) : 'violet', #blue?
        (0xF0, 0x00, 0xF0) : 'magenta',
        (0x00, 0xF0, 0xF0) : 'cyan',
        (0xF0, 0xF0, 0xF0) : 'white',
    }

    m, d = (0x00, 0x00, 0x00), 0xFF**2
    for R, G, B in colors:
        l = (r-R)**2 + (g-G)**2 + (b-B)**2

        if l < d:
            m, d = (R, G, B), l

    return colors[m]


def get_color(string):
    """Generates a colour depending on the nick : str"""
    c = lambda s: hash(s) % 256
    return c(string[0:3]), c(string[3:6]), c(string[6:9])


#---- COMMENT PRINTER ----------------------------------------------------------

def post(comment):
    color   = closest_color(*comment['color'])
    nick    = sformat(comment['nick'], color=color, font='underline')
    time    = sformat(comment['time'], color='darkgray')
    message = comment['message']

    TABLE.printrow(f"│ {nick.ljust(NICK_WIDTH)} {time} │")

    for chunk in split(message, TABLE.text_width):
        TABLE.printrow(f"│ {chunk.ljust(TABLE.text_width)} │")

    # Add bottom border of cell
    border()

    # Move the cursor to the bottom-left corner
    # so it stays fixed after printing
    TABLE.reset_cursor()

    # Force update terminal
    print(flush=True)


def make_comment(match):
    return dict(
        nick    = match["nick"],
        message = match["message"],
        time    = datetime.now().strftime('%H:%M:%S'),
        color   = get_color(match["nick"]),
    )


MESSAGE_FORMAT = re.compile(r":(?P<nick>.*)!(?P=nick)@(?P=nick).tmi.twitch.tv PRIVMSG #(?P<channel>.*) :(?P<message>.*)")


def post_comments(responses):
    for response in responses.splitlines():
        match = MESSAGE_FORMAT.match(response)
        if match is None: continue

        comment = make_comment(match)
        post(comment)
