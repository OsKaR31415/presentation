from asciimatics.screen import Screen
from frame import Frame  # object representing a frame
from animations import *  # animation functions
from time import sleep
from itertools import zip_longest

def run_anim(anim, screen):
    fr = Frame(screen.width, screen.height)
    for changes in anim:
        for anim in changes:
            fr = anim(fr)
        fr.show(screen)
        sleep(0.01)
    sleep(1)

def main(scr):
    anim = concat(
    )
    run_anim(anim, scr)

Screen.wrapper(main)


