from asciimatics.screen import Screen
from frame import Frame  # object representing a frame
from animations import *  # animation functions
from time import sleep
from itertools import zip_longest


def main(scr):
    fr = Frame(scr.width, scr.height)
    # anim = concat(
    #     appear(scr, 2, "un texte apparaît"),
    #     appear(scr, 4, "un autre plus lentement", delay=9),
    #     after(100, appear(scr, 0, "celui-ci ensuite")),
    #     after(170, appear(scr, 2, "on remplace")),
    #     after(200, appear_left(scr, 6, "youpi !", delay=2)),
    # )
    anim = concat(
        appear(scr, 2, "un texte apparaît"),
        appear(scr, 4, "un autre plus lentement", delay=9),
        after(100, appear(scr, 0, "texte " + "très "*12 + "long" )),
        after(170, appear(scr, 2, "on remplace ")),
        after(200, appear_left(scr, 6, "youpi !", delay=2)),
        after(200, appear_left(scr, 7, "youpi !", delay=3)),
        after(200, appear_left(scr, 8, "youpi !", delay=4)),
        after(200, appear_left(scr, 9, "youpi !", delay=5)),
    )
    for changes in anim:
        for anim in changes:
            fr = anim(fr)
        fr.show(scr)
        sleep(0.01)
    sleep(1)

Screen.wrapper(main)


