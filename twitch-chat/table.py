from os import get_terminal_size, system

#---- TERMINAL WRITER ----------------------------------------------------------

# WARNING: Terminal variables are technically not constants,
# as the terminal can be resized; the user is expect not to.
TERMINAL_WIDTH,\
TERMINAL_HEIGHT = get_terminal_size(0)
COLUMN_WIDTH    = 50
ROW_HEIGHT      = 1
system('clear')

class Table:
    def __init__(self, init=None):
        self.anchor = [1, 1] if init is None else init
        self.iter   = iter(self)
        self.text_width = COLUMN_WIDTH - 4

    def __iter__(self):
        while 1:
            for column in range(1, TERMINAL_WIDTH-COLUMN_WIDTH, COLUMN_WIDTH):
                for row in range(1, TERMINAL_HEIGHT-ROW_HEIGHT, ROW_HEIGHT):
                    self.anchor[:] = column, row
                    yield row, column # (y, x) pair

    def __next__(self):
        """Next table row"""
        return self.iter.__next__()


    def move_cursor(self, y=1, x=1):
        """Moves the cursor to the selected position"""
        print(f"\033[{y};{x}H", end='')


    def go_to_next_row(self):
        """Moves the cursor to the next table row"""
        self.move_cursor(*self.__next__())


    def printrow(self, *string, end=True, **format):
        """Prints a row in the table"""
        if end: self.go_to_next_row()
        print(*string, end='', **format)


    def reset_cursor(self):
        """Moves cursor to bottom-left corner"""
        self.move_cursor(TERMINAL_HEIGHT-1, 1)


TABLE = Table()
