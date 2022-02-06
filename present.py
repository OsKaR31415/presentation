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
        repeat(one_by_one(
            fadein_center(scr, 12, "cool !"),
            fadeout_center(scr, 12, "cool !"),
            delay=100,
            ))
        )
    run_anim(screen=scr, anim=anim)


Screen.wrapper(main)

