"""Object representing a frame for a presentation.
"""
from textwrap import wrap

class Frame:
    def __init__(self, width, height):
        self.width = int(width)
        self.height = int(height)
        self.text = [[" " for _ in range(self.width)]
                     for _ in range(self.height)]
        self.color = [[0 for _ in range(width)]
                      for _ in range(height)]

    def show(self, screen) -> None:
        """Show the frame in a screen."""
        self.width = screen.width
        self.height = screen.height
        for x in range(self.width):
            for y in range(self.height):
                screen.print_at(self.text[y][x], x, y, colour=self.color[y][x])
        screen.refresh()

    def char_at(self, y: int, x: int, char: str, color: int =255):
        """Set the character at the given position (with the given colour)."""
        # wrap arout the screen
        while x > self.width:
            x -= self.width
            y += 1
        # set the char in the char matrix
        self.text[y][x] = str(char)[0]  # only take the first character
        self.color[y][x] = int(color)
        return self

    def str_at(self, y: int, x: int, string: str, color: int =255):
        """Put the given string at the given position."""
        string = wrap(string, width=self.width)
        for line_shift, line in enumerate(string):
            for pos, char in enumerate(line):
                self.char_at(y + line_shift, x+pos,
                             char, color)
        return self

    def erase_line(self, y: int):
        """Erase the given line."""
        self.text[y] = [" " for _ in range(self.width)]
        return self

    def line(self, begin: (int, int), end: (int, int), char: str =None):
        """Draw a straight line starting at *begin* coordinates and
        ending and *end* coodinates."""
        assert len(begin) == 2 and len(end) == 2  # both must be couples
        self.move(*begin)
        self.draw(*end)
        return self


