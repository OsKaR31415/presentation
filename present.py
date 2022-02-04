from asciimatics.screen import Screen
from time import sleep



def erase_line(screen, y: int):
    """Erase a given line."""
    yield (lambda fr: Frame.erase_line(fr, y),)

def center(screen, y: int, text: str, color: int =0):
    """Write text at the center of the screen."""
    margin = (screen.width - len(text)) // 2
    yield (lambda fr: Frame.str_at(fr, y, margin, text, color),)

def after(frames_to_wait: int, animation):
    """Run animation after the given number of frames."""
    for _ in range(frames_to_wait):
        yield (lambda fr: fr,)
    yield from animation

# def appear_left(screen, y: int, text: str):
#     for x in range((screen.width - len(text))//2):
#         yield ()

def center_fadein(screen, y: int, text: str):
    for col in range(232, 255):
        yield from center(screen, y, text, color=col)

def center_fadein_pause(screen, y: int, text: str):
    for col in range(235, 255):
        yield (lambda fr: next(center(screen, y, text, color=col))[0](fr),)
    screen.getkey()

def cons(anim1, anim2):
    for cons_anim in zip(anim1, anim2):
        yield cons_anim[0] + cons_anim[1]
    yield from anim1
    yield from anim2

def concat(*animations):
    if len(animations) == 1:
        return animations[0]
    else:
        return cons(animations[0], concat(*animations[1:]))

def main(scr):
    fr = Frame(scr.width, scr.height)
    anim = concat(
            center_fadein(scr, 5, "j'adore programmer"),
            after(100, erase_line(scr, 5)),
            after(100, center_fadein(scr, 5, "c'est cool")),
            after(200, erase_line(scr, 5)),
            after(200, center_fadein(scr, 5, "wow !"))
            )
    # anim = cons(anim, after(3, left(scr, 4, "left", 0)))
    for next_frame in anim:
        for anim in next_frame:
            fr = anim(fr)
        fr.show(scr)
        sleep(0.01)
    sleep(1)

Screen.wrapper(main)


