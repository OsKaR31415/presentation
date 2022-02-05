"""Library containing animations.
An animation is a generator.
Each element generated is a tuple of the transformations to do on a frame.
each transformations is simply a function, taking a Frame object as an argument
and returning a frame object transformed.
Frame object are from `frame.py`
"""
from frame import Frame  # animations are returning frames
from itertools import zip_longest, chain


def concat(*animations):
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


def wait_for(delay: int):
    for _ in range(delay):
        yield []

def after(frames_to_wait: int, animation):
    """Run animation after the given number of frames."""
    yield from wait_for(frames_to_wait)
    yield from animation


def erase_line(screen, y: int):
    """Erase a given line."""
    yield [lambda fr: Frame.erase_line(fr, y)]


def center(screen, y: int, text: str, color: int = 255):
    """Write text at the center of the screen."""
    margin = (screen.width - len(text)) // 2
    yield [lambda fr: Frame.str_at(fr, y, margin, text, color)]


def appear_left(screen, y: int, text: str, color: int = 255, delay: int = 0):
    """Make the text to apear on the left"""
    test = str(text)
    for x in range(1, (screen.width - len(text))//2):
        # the ' ' before text is to erase its trace
        yield [lambda fr: Frame.str_at(fr, y, x-1, '  ' + text, color)]
        yield from wait_for(delay)


def fadein(screen, animation, *args, delay: int =0):
    """Fade in a certain animation.
    To work properly, the animation should be short : Each play of the
    animation changes of one shade the brightness.
    Args:
        animation: The animation to add fade in to.
        *args: The arguments to give to the animation.
        delay (int): the delay (in number of frames) to wait before brightness
                     is changed (also pauses the animation). Default to 0.
    """
    for color in range(235, 255):
        yield from animation(screen, *args, color=color)
        yield from wait_for(delay)


def put_char(screen, y: int, x: int, char: str, color: int = 255):
    yield [lambda fr: Frame.char_at(fr, y, x, str(char)[0], color)]


def put_text(screen, y: int, x: int, text: str, color: int = 255):
    yield [lambda fr: Frame.str_at(fr, y, x, str(text), color)]


def fadein_text(screen, y: int, x: int, text: str, delay: int = 0):
    """Fade in the text."""
    yield from fadein(screen, put_text, y, x, text, delay=delay)


def center_fadein(screen, y: int, text: str, delay: int = 0):
    """Fade in the centered text.
    Duration: 20 frames (multiplied by delay+1)."""
    yield from fadein(screen, center, y, text, delay=delay)


# def center_appear_up(screen, text: str, final_y: int = None,
#     color: int = 255, delay: int = 0):
#     """Appear the text from to top."""
#     if final_y is None:
#         final_y = screen.height // 2
#     else:
#         final_y = int(final_y)
#     margin = (screen.width - len(text)) // 2
#     for y in range(final_y):
#         yield from put_text(yield, y, margin)
#         yield from center(screen, y, str(text), color=int(color))
#         yield from wait_for(delay)


def appear(screen, line: int, text: str, delay: int = 0):
    """Make the given text to appear in the screen (fade in).
    Erasesthe line and then makes it to appear."""
    # if the text is less large than the screen, then center it
    if len(text) < screen.width:
        yield from concat(erase_line(screen, line),
                          center_fadein(screen, line, text, delay))
    # if there is too much text, then it well be automatically left-aligned
    # and wrapped by the frame's *str_at* method.
    else:
        yield from fadein_text(screen, line, 0, text, delay)


def box(screen, topleft: (int, int), bottomright: (int, int), color: int = 255):
    """Draw a box from *topleft* to *bottomright*."""
    yield [lambda fr: Frame.box(fr, topleft, bottomright, color)]


def fadein_box(screen, topleft: (int, int), bottomright: (int, int),
               delay: int = 0):
    for color in range(235, 255):
        yield from box(screen, topleft, bottomright, color=color)
        yield from wait_for(delay)


def boxed(screen, y: int, x: int, text: str,
          full_width: bool = False,
          color: int = 255):
    yield from put_text(screen, y, x, text, color)
    if full_width:
        yield from box(screen, (y-1, 0), (y+1, screen.width-1), color)
    else:
        yield from box(screen, (y-1, x-1), (y+1, x+len(text)), color)


def fadein_boxed(screen, y: int, x: int, text: str, full_width: bool = False,
        delay: int = 0):
    yield from fadein(screen, boxed, y, x, text, full_width, delay=delay)


def boxed_centered(screen, y: int, text: str,
        full_width: bool = False,
        color: int = 255):
    yield from center(screen, y, text)
    if full_width:
        yield from box(screen, (y-1, 0), (y+1, screen.width-1), color=color)
    else:
        margin = (screen.width - len(text)) // 2
        yield from box(screen, (y-1, margin-1), (y+1, margin+len(text)), color)


def circle(screen, x: int, y: int, radius: int,
           y_stretch: int = 1, x_stretch: int = 1,
           fill: str = '█',
           color: int = 255):
    circle_pixels = []
    for line in range(y-radius*y_stretch, y+radius*y_stretch+1):
        for col in range(x-radius*x_stretch, x+radius*x_stretch+1):
            if x_stretch*(col-x)**2 + y_stretch*(line-y)**2 <= radius**2:
                circle_pixels.extend(next(
                    put_char(screen, line, col, str(fill)[0], color)
                    ))
    yield circle_pixels



