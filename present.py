from asciimatics.screen import Screen
from frame import Frame  # object representing a frame
from animations import *  # animation functions
from time import sleep
from itertools import zip_longest


def main(scr):
    fr = Frame(scr.width, scr.height)
    anim = concat(
            after(0, fadein(scr, 5, 0, "cool")),
            after(10, fadein(scr, 6, 0, "cool")),
            )
    # anim = cons(anim, after(3, left(scr, 4, "left", 0)))
    # input(list(anim))
    for changes in anim:
        for anim in changes:
            fr = anim(fr)
        fr.show(scr)
        sleep(0.01)
    sleep(1)

Screen.wrapper(main)


