from asciimatics.screen import Screen
from frame import Frame  # object representing a frame
from animations import *  # animation functions
from time import sleep
from itertools import zip_longest


def main(scr):
    fr = Frame(scr.width, scr.height)
    anim = concat(
            appear_left(scr, 1, "test", delay=1),
            appear_left(scr, 2, "test", delay=2),
            appear_left(scr, 3, "test", delay=3),
            appear_left(scr, 4, "test", delay=4),
            after(80, fadein(scr, 5, 0, "cool"))
            )
    # anim = cons(anim, after(3, left(scr, 4, "left", 0)))
    # input(list(anim))
    for changes in anim:
        for anim in changes:
            fr = anim(fr)
        fr.show(scr)
        sleep(0.03)
    sleep(1)

Screen.wrapper(main)


