"""Library containing animations.
An animation is a generator.
Each element generated is a tuple of the transformations to do on a frame.
each transformations is simply a function, taking a Frame object as an argument
and returning a frame object transformed.
Frame object are from `frame.py`
"""
from frame import Frame  # animations are returning frames
from itertools import zip_longest, chain

class Animation:
    def __init__(self, screen):
        self.screen = screen

    def concat(self, *animations):
        """Concatenate all the animations given in the input.
        Args:
            *animations (generator[tuple[function]]): The animations to merge.
        Returns:
            generator[tuple[function]]: The merged animations.
        """
        # zip the two generators.
        for changes in zip_longest(*animations, fillvalue=[lambda fr: fr]):
            # flatten each changes (join the iterators)
            yield chain.from_iterable(changes)


    def wait_for(self, delay: int):
        for _ in range(delay):
            yield []


    def pause(self):
        key = self.screen.get_key()
        while key == self.screen.get_key():
            pass
        yield []


    def paused(self, animation, *args, **kwargs):
        yield from self.pause()
        yield from animation(self.screen, *args, **kwargs)


    def after(self, frames_to_wait: int, animation):
        """Run animation after the given number of frames."""
        yield from self.wait_for(frames_to_wait)
        yield from animation


    def one_by_one(self, *animations,
                   pauses: bool = False, insert = None, delay: int = 0):
        """Make animations to be played one at a time.
        Args:
            *animations: all the animations to play.
            pauses (bool) (optional): If True, there will be a pause between
                                      each animation. Default to False.
            insert: An animation between each tof the others. Default to None.
            delay (int): The delay between each animation.
        """
        for anim in animations:
            yield from anim
            yield from self.wait_for(delay)
            if pauses:
                yield from self.pause()
            if insert is not None:
                yield from insert()


    def repeat(self, animation, repetitions: int = 2, delay: int = 0):
        for _ in range(int(repetitions)):
            yield from animation

    def erase_line(self, y: int):
        """Erase a given line."""
        yield [lambda fr: Frame.erase_line(fr, y)]


    def clear(self):
        """Clear the screen."""
        yield [lambda fr: Frame.clear(fr)]

    def center(self, y: int, text: str, color: int = 255):
        """Write text at the center of the screen."""
        margin = (self.screen.width - len(text)) // 2
        yield [lambda fr: Frame.str_at(fr, y, margin, text, color)]


    def appear_left(self, y: int, text: str, color: int = 255, delay: int = 0):
        """Make the text to apear on the left"""
        text = str(text)
        for x in range(1, (self.screen.width - len(text))//2):
            # the ' ' before text is to erase its trace
            yield [lambda fr: Frame.str_at(fr, y, x-1, '  ' + text, color)]
            yield from self.wait_for(delay)


    def fadein(self, animation, *args, delay: int =0):
        """Fade in a given animation.
        To work properly, the animation should be short : Each play of the
        animation changes of one shade the brightness.
        Args:
            animation: The animation to add fade in to.
            *args: The arguments to give to the animation.
            delay (int): the delay (in number of frames) to wait before brightness
                         is changed (also pauses the animation). Default to 0.
        """
        for color in range(235, 255):
            yield from animation(*args, color=color)
            yield from self.wait_for(delay)


    def fadeout(self, animation, *args, delay: int = 0):
        """Fade out a given animation."""
        for color in reversed(range(233, 253)):
            yield from animation(self.screen, *args, color=color)
            yield from self.wait_for(delay)
        yield from animation(self.screen, *args, color=0)


    def put_char(self, y: int, x: int, char: str, color: int = 255):
        """Put a char in the screen."""
        yield [lambda fr: Frame.char_at(fr, y, x, str(char)[0], color)]


    def put_text(self, y: int, x: int, text: str, color: int = 255):
        """Put a text in the screen."""
        yield [lambda fr: Frame.str_at(fr, y, x, str(text), color)]


    def bullet(self, y: int, x: int, depth: int = 0, color: int = 255):
        """Put a bullet for item lists.
        The depth changes the symbol for the bullet. The bullets by depth are :
        0 : ●
        1 : ○
        2 : ■
        3 : □
        4 : -
        """
        yield from self.put_char(y, x, '●○■□-­'[depth])


    def bell(self, y: int, x: int, text: str):
        yield from self.put_char(self.screen, y, x, '\u0007')


    def fadein_text(self, y: int, x: int, text: str, delay: int = 0):
        """Fade in the text."""
        yield from self.fadein(self.put_text, y, x, text, delay=delay)


    def fadein_center(self, y: int, text: str, delay: int = 0):
        """Fade in the centered text.
        Duration: 20 frames (multiplied by delay+1)."""
        yield from self.fadein(self.center, y, text, delay=delay)


    def fadeout_center(self, y: int, text: str, delay: int = 0):
        """Fade out the centered text."""
        yield from self.fadeout(self.center, y, text, delay=delay)


    def center_appear_up(self, text: str, final_y: int = None,
        color: int = 255, delay: int = 0):
        """Appear the text from to top."""
        if final_y is None:
            final_y = self.screen.height // 2
        else:
            final_y = int(final_y)
        # margin = (self.screen.width - len(text)) // 2
        for y in range(final_y):
            yield from self.center(y, str(text), color=int(color))
            if y > 0:
                yield from self.center(y-1, " "*len(str(text)))
            yield from self.wait_for(delay)


    def appear(self, line: int, text: str, delay: int = 0):
        """Make the given text to appear in the screen (fade in).
        Erasesthe line and then makes it to appear."""
        # if the text is less large than the screen, then center it
        if len(text) < self.screen.width:
            yield from self.concat(self.erase_line(line),
                              self.fadein_center(line, text, delay))
        # if there is too much text, then it well be automatically left-aligned
        # and wrapped by the *Frame.str_at* method.
        else:
            yield from self.fadein_text(line, 0, text, delay)


    def box(self, topleft: (int, int), bottomright: (int, int), color: int = 255):
        """Draw a box from *topleft* to *bottomright*."""
        yield [lambda fr: Frame.box(fr, topleft, bottomright, color)]


    def fadein_box(self, topleft: (int, int), bottomright: (int, int),
                   delay: int = 0):
        """Fade in a box."""
        for color in range(235, 255):
            yield from self.box(topleft, bottomright, color=color)
            yield from self.wait_for(delay)


    def boxed_text(self, y: int, x: int, text: str,
              full_width: bool = False,
              color: int = 255):
        """Surround text with a box."""
        yield from self.put_text(y, x, text, color)
        if full_width:
            yield from self.box((y-1, 0), (y+1, self.screen.width-1), color)
        else:
            yield from self.box((y-1, x-1), (y+1, x+len(text)), color)


    def fadein_boxed(self, y: int, x: int, text: str, full_width: bool = False,
            delay: int = 0):
        """Fade in a boxed text."""
        yield from self.fadein(self.boxed_text,
                               y, x, text, full_width, delay=delay)


    def boxed_centered(self, y: int, text: str,
            full_width: bool = False,
            color: int = 255):
        yield from self.center(y, text, color)
        if full_width:
            yield from self.box((y-1, 0), (y+1, self.screen.width-1),
                                color=color)
        else:
            margin = (self.screen.width - len(text)) // 2
            yield from self.box((y-1, margin-1), (y+1, margin+len(text)), color)


    def circle(self, x: int, y: int, radius: int,
               y_stretch: int = 1, x_stretch: int = 1,
               fill: str = '█',
               color: int = 255):
        circle_pixels = []
        for line in range(y-radius*y_stretch, y+radius*y_stretch+1):
            for col in range(x-radius*x_stretch, x+radius*x_stretch+1):
                if x_stretch*(col-x)**2 + y_stretch*(line-y)**2 <= radius**2:
                    circle_pixels.extend(next(
                        self.put_char(line, col, str(fill)[0], color)
                        ))
        yield circle_pixels





