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
        appear(s, 1, "voici une présentation"),
        after(200,
            appear(s, 4, "Elle est faîte avec ma super librairie python !")),
        after(400,
            appear_left(s, 6, "youpiii"))
    )
    run_anim(screen=s, anim=anim)


Screen.wrapper(main)
