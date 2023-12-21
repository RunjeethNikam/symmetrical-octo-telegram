from time import sleep, time


def display_countdown(nseconds):
    """
    Display a countdown to the user to show time remaining.

    Parameters:
    - nseconds: Total duration of the countdown in seconds.
    """
    start_time = time()

    while True:
        sleep_interval = 5
        sleep(sleep_interval)

        now = time()
        elapsed_time = now - start_time

        if elapsed_time > nseconds:
            break

        time_remaining = nseconds - elapsed_time
        print(f"{time_remaining:.1f}s left...")


# Example usage:
# display_countdown(60)
