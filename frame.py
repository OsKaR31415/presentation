"""Object representing a frame for a presentation.
"""
from textwrap import wrap

class Frame:
    def __init__(self, screen):
        self.width = screen.width
        self.height = screen.height
        self.text = [[" " for _ in range(self.width)]
                     for _ in range(self.height)]
        self.color = [[0 for _ in range(self.width)]
                      for _ in range(self.height)]

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
            for col, char in enumerate(line):
                self.char_at(y+line_shift, x+col, char, color)
            # for pos, char in enumerate(line):
            #     self.char_at(y + line_shift, x+pos, char, color)
        return self

    def erase_line(self, y: int):
        """Erase the given line.
        Args:
            y (int): The index of the line to erase.
        Returns:
            Frame: The frame with the line erased. Also modifies self.
        """
        self.text[y] = [" " for _ in range(self.width)]
        return self

    def clear(self):
        """Clear the whole frame."""
        self.text = [[" " for _ in range(self.width)]
                     for _ in range(self.height)]
        self.color = [[0 for _ in range(width)]
                      for _ in range(height)]

    def box(self, topleft: (int, int), bottomright: (int, int),
            color: int =255):
        """Draw a box (using unicode box-drawing), from the coordinates in
        *topleft* to the coordinates in *bottomright*.
        Args:
            topleft (tuple(int, int)): The couple of coordinates of the
                                       top-left corner of the box.
            bottomright (tuple(int, int)): The couple of coordinates of the
                                           bottom-right corner of the box.
            color (int): The color to draw the box in. Default to 255 (white).
        Returns:
            Frame: The frame with the box drawn. Also modifies self.
        """
        top, left = topleft
        bottom, right = bottomright
        width, height = abs(right - left), abs(bottom - top)
        self.str_at(top, left, '┏' + '━'*(width-1) + '┓', color)
        for y in range(1, height):
            self.char_at(top+y, left, '┃', color)
            self.char_at(top+y, right, '┃', color)
        self.str_at(bottom, left, '┗' +'━'*(width-1) + '┛', color)
        return self


