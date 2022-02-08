from asciimatics.screen import Screen
from frame import Frame  # object representing a frame
from animations import Animation  # animation functions
from time import time, sleep


def run_animation(screen, anim, post_delay: int = 0):
    fr = Frame(screen)
    for changes in anim:
        prev_frame_time = time()
        for anim in changes:
            fr = anim(fr)
            # key = screen.get_key()
            if screen.get_key() == ord('n'):
                return "next"
            if screen.get_key() == ord('p'):
                return "previous"
            if screen.get_key() == ord('r'):
                return "restart"
            if screen.get_key() == ord('q'):
                return "quit"
        fr.show(screen)
        while time() - prev_frame_time < 0.01:
            pass
    sleep(post_delay/100)
    return "finished"


def run_presentation(screen, presentation: list):
    """Run the given presentation in the given screen.
    A presentation is simply a list of animations, each of for a slide."""
    a = Animation(screen)
    presentation = a.one_by_one(*presentation, pauses=True)
    run_animation(screen, presentation)
    return
    slide_idx = 0
    while slide_idx < len(presentation):
        screen.clear()
        exit_status = run_animation(screen, presentation[slide_idx])
        if exit_status == "quit":
            return
        elif exit_status == "previous":
            slide_idx -= 2
            if slide_idx < 0: slide_idx = 0
            continue
        elif exit_status == "restart":
            continue
        # else:
        #     key = screen.get_key()
        #     while key == screen.get_key():
        #         pass


def presentation(screen):
    a = Animation(screen)
    present= [
        a.concat(
            a.appear(2, "super"),
            a.appear(3, "cool!"),
            a.after(100, a.appear(5, "Et facile")),
            a.after(200, a.one_by_one(
                a.appear(5, "on remplace"),
                a.appear_left(6, "-> whoooo !"),
                delay=50,
            ))
        ),
        a.one_by_one(
            a.appear(1, "des"),
            a.appear(2, "animations"),
            a.appear(3, "qui"),
            a.appear(4, "se"),
            a.appear(5, "suivent"),
            ),
        a.one_by_one(
            a.appear(1, "plus"),
            a.appear(2, "ou"),
            a.appear(3, "moins"),
            a.appear(4, "vite"),
            delay=40,
            ),
        a.concat(
            a.appear(1, "ou bien"),
            a.appear(3, "toutes en même temps"),
            a.appear(10, "c'est bien aussi"),
            a.pause(),
            ),
        ]
    run_presentation(screen, present)
    # for a in present:
    #     run_animation(screen, a, 100)
    # run_animation(screen, present[0], 100)


Screen.wrapper(presentation)

