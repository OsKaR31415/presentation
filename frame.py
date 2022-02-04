"""Object representing a frame for a presentation.
"""


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

    def char_at(self, y: int, x: int, char: str, colour: int =0):
        """Set the character at the given position (with the given colour)."""
        # wrap arout the screen
        while x > self.width:
            x -= self.width
            y += 1
        # set the char in the char matrix
        self.text[y][x] = str(char)[0]
        self.color[y][x] = int(colour)
        return self

    def str_at(self, y: int, x: int, string: str, colour: int =0):
        """Put the given string at the given position."""
        for pos, char in enumerate(string):
            self.char_at(y, x+pos, char, colour)
        return self

    def erase_line(self, y: int):
        """Erase the given line."""
        self.text[y] = [" " for _ in range(self.width)]
        return self
