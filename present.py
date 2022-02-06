from asciimatics.screen import Screen
from frame import Frame  # object representing a frame
from animations import *  # animation functions
from time import time, sleep


def run_anim(screen, anim, post_delay: int = 100):
    fr = Frame(screen.width, screen.height)
    for changes in anim:
        prev_frame_time = time()
        for anim in changes:
            fr = anim(fr)
        fr.show(screen)
        while time() - prev_frame_time < 0.01:
            pass
    sleep(post_delay/100)


def main(scr):
    anim = concat(
        one_by_one(
            appear(scr, 2, "an appearing text"),
            appear(scr, 4, "another appearing text"),
            appear(scr, 2, "now we replace it"),
            appear_left(scr, 6, "wooooh !", delay=3),
            delay=50
            ),
        fadein(scr, boxed_centered, 8, "synchronously appearing text"),
        after(300, fadein(scr, circle, scr.width//2, 20, 13, 2)),
        after(300, fadein(scr, circle, scr.width//2, 20, 10, 2, 1, ' ')),
    )
    run_anim(screen=scr, anim=anim)


Screen.wrapper(main)

