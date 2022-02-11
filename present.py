from asciimatics.screen import Screen
from frame import Frame  # object representing a frame
from animations import *  # animation functions
from time import time, sleep


def run_animation(screen, anim, post_delay: int = 0):
    fr = Frame(screen)
    for changes in anim:
        prev_frame_time = time()
        for anim in changes:
            fr = anim(fr)
            key = screen.get_key()
            if key == ord('n'):
                fr.clear()
                return "next"
            if key == ord('p'):
                return "previous"
            if key == ord('r'):
                return "restart"
            if key == ord('q'):
                exit(0)
        fr.show(screen)
        while time() - prev_frame_time < 0.01:
            pass
    sleep(post_delay/100)
    return "finished"


def run_presentation(screen, presentation: list):
    """Run the given presentation in the given screen.
    A presentation is simply a list of animations, each of for a slide."""
    fr = Frame(screen)
    slide_idx = 0
    while slide_idx < len(presentation):
        ##### Here, play the animation #####
        for list_modifications in presentation[slide_idx]:
            prev_frame_time = time()
            for modif in list_modifications:
                fr = modif(fr)
                key = screen.get_key()
                if key == ord('n'):  # next
                    slide_idx += 1
                    continue
                if key == ord('p'):  # previous
                    slide_idx -= 1
                    continue
                if key == ord('r'):  # restart
                    continue
                if key == ord('q'):  # quit
                    exit(0)
            fr.show()
            while time() - prev_frame_time < 0.01:
                pass
        # a pause
        key = screen.get_key()
        while key == screen.get_key():
            if key == ord('n'):  # next
                slide_idx += 1
                continue
            if key == ord('p'):  # previous
                slide_idx -= 1
                continue
            if key == ord('r'):  # restart
                continue
            if key == ord('q'):  # quit
                exit(0)
        fr.clear()
        slide_idx += 1


def presentation(screen):
    a = PrimitiveAnimations(screen)
    present= [

        a.one_by_one(
            a.title("slide 1"),
            a.appear(4, "this library is usefull for making presentations"),
            a.appear(6, "more precisely, text-based presentations"),
            a.appear(8, "Here is a little demonstration of what it can do"),
            # pauses=True
        ),

        a.one_by_one(
            a.title("slide 2"),
            a.appear(2, "you"),
            a.appear(3, "can"),
            a.appear(4, "make"),
            a.appear(5, "things"),
            a.appear(6, "appear"),
        ),

        a.one_by_one(
            a.title("slide 3"),
            a.appear(2, "these"),
            a.appear(3, "ones"),
            a.appear(4, "are"),
            a.appear(5, "slower"),
            delay=20,
            ),

        a.concat(
            a.title("slide 3"),
            a.appear(2, "animations are very powerful"),
            a.after(100, a.appear_left(4, "-> here it comes", delay=3)),
            a.bulleted(6,  5, "and"),
            a.bulleted(7,  5, "we"),
            a.bulleted(8,  5, "have"),
            a.bulleted(9, 5, "bullet"),
            a.bulleted(10, 5, "lists"),
            ),

        ]
    run_presentation(screen, present)
    # for a in present:
    #     run_animation(screen, a, 100)
    # run_animation(screen, present[0], 100)


Screen.wrapper(presentation)

