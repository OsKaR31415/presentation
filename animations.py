"""Library containing animations.
An animation is a generator.
Each element generated is a tuple of the transformations to do on a frame.
each transformations is simply a function, taking a Frame object as an argument
and returning a frame object transformed.
Frame object are from `frame.py`
"""
from frame import Frame
from itertools import zip_longest, chain


def erase_line(screen, y: int):
    """Erase a given line."""
    yield [lambda fr: Frame.erase_line(fr, y)]

def center(screen, y: int, text: str, color: int =0):
    """Write text at the center of the screen."""
    margin = (screen.width - len(text)) // 2
    yield [lambda fr: Frame.str_at(fr, y, margin, text, color)]

def after(frames_to_wait: int, animation):
    """Run animation after the given number of frames."""
    for _ in range(frames_to_wait):
        yield [lambda fr: fr]
    yield from animation

def appear_left(screen, y: int, text: str, color: int =0, delay: int =0):
    """Make the text to apear on the left"""
    test = str(text)
    for x in range(1, (screen.width - len(text))//2):
        # the ' ' before text is to erase its trace
        yield [lambda fr: Frame.str_at(fr, y, x-1, '  ' + text, color)]
        for _ in range(delay):
            yield [lambda fr: fr]

def fadein(screen, y: int, x: int, text: str):
    """Fade in the text."""
    for color in range(232, 255):
        yield [lambda fr: Frame.str_at(fr, y, x, text, color=color)]

def center_fadein(screen, y: int, text: str):
    """Fade in the centered text."""
    for color in range(232, 255):
        yield from center(screen, y, text, color=color)

# def center_fadein_pause(screen, y: int, text: str):
#     for col in range(235, 255):
#         yield (lambda fr: next(center(screen, y, text, color=col))[0](fr),)
#     screen.getkey()

def appear(screen, line: int, text: str):
    """Make the given text to appear in the screen (fade in).
    Erasesthe line and then makes it to appear."""
    yield from cons(erase_line(screen, line),
                    center_fadein(screen, line, text))

def concat(*animations):
    """Concatenate all the animations given in the input.
    Args:
        *animations (generator[tuple[function]]): The animations to merge.
    Returns:
        generator[tuple[function]]: The merged animations.
    """
    # zip the two generators. The fill value is the identity function.
    for changes in zip_longest(*animations, fillvalue=[lambda x: x]):
        # flatten each changes (join the iterators)
        yield chain.from_iterable(changes)


