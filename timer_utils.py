from time import sleep, time


def display_countdown(ns):
    """
    Display a countdown to the user to show time remaining.

    Parameters:
    - nseconds: Total duration of the countdown in seconds.
    """
    st = time()
    sleep_itv = 6

    while 1:
        sleep(sleep_itv)
        et = time() - st

        if et > ns: break

        time_remaining = ns - et
        print(f"{time_remaining:.1f}s to go")

# Example usage:
# display_countdown(60)
