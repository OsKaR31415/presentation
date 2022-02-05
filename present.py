from asciimatics.screen import Screen
from frame import Frame  # object representing a frame
from animations import *  # animation functions
from time import time, sleep
from itertools import zip_longest


def run_anim(screen, anim):
    fr = Frame(screen.width, screen.height)
    for changes in anim:
        prev_frame_time = time()
        for anim in changes:
            fr = anim(fr)
        fr.show(screen)
        while time() - prev_frame_time < 0.01:
            pass
    sleep(1)


def main(s):
    anim = concat(
        appear(s, 2, "un texte apparaîte"),
        after(100, appear(s, 4, "un autre")),
        after(200, appear(s, 2, "on le remplace")),
        after(300, appear_left(s, 6, "youpi !!!", delay=2))
        # *(after(3*y, center(s, y, "test")) for y in range(10)),
        # *(after(3*y, erase_line(s, y-1)) for y in range(0, 10)),
    )
    run_anim(screen=s, anim=anim)


Screen.wrapper(main)
