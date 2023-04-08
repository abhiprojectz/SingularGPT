import subprocess
import re
from time import sleep

def click_one(x, y):
    """
    This function uses the xdotool utility to move the mouse to given x and y coordinates on the screen and
    performs a left-click (mouse button 1) operation.

    Parameters:
    x (int): The x-coordinate on the screen where the left-click operation needs to be performed.
    y (int): The y-coordinate on the screen where the left-click operation needs to be performed.
    """
    # Get the current window ID
    window = subprocess.check_output("xdotool getmouselocation", shell=True)
    wind__ = int(re.search(r'\d+', str(window).split(" ")[-1].strip()).group())

    # Move the mouse to the provided x and y coordinates and perform a left click
    subprocess.run(f"xdotool mousemove --window {wind__} {x} {y} click 1", shell=True)


def click_two(x, y):
    """
    This function uses the xdotool utility to move the mouse to given x and y coordinates on the screen and
    performs a right-click (mouse button 2) operation.

    Parameters:
    x (int): The x-coordinate on the screen where the right-click operation needs to be performed.
    y (int): The y-coordinate on the screen where the right-click operation needs to be performed.
    """
    # Get the current window ID
    window = subprocess.check_output("xdotool getmouselocation", shell=True)
    wind__ = int(re.search(r'\d+', str(window).split(" ")[-1].strip()).group())

    # Move the mouse to the provided x and y coordinates and perform a right click
    subprocess.run(f"xdotool mousemove --window {wind__} {x} {y} click 2", shell=True)


def write(_text, delay):
    """
    This function uses the xdotool utility to simulate keyboard input and type out the provided text.

    Parameters:
    _text (str): The text to be typed out.
    """

    if delay: 
        subprocess.run(f'xdotool type --delay 50 "{_text}"', shell=True)
    else:
        subprocess.run(f'xdotool type "{_text}"', shell=True)


def press_key(x):
    """
    This function uses the xdotool utility to simulate key presses on the keyboard.

    Parameters:
    x (str): The key to be press. For example, 'ctrl+v', 'ctrl+t', 'shift+tab' etc.
    """

    subprocess.run(f"xdotool key {x}", shell=True)


def left_click():
    """
    This function uses the xdotool utility to perform a left-click (mouse button 1) operation.
    """

    subprocess.run("xdotool click 1", shell=True)


def middle_click():
    """
    This function uses the xdotool utility to perform a middle-click (mouse button 2) operation.
    """

    subprocess.run("xdotool click 2", shell=True)


def right_click():
    """
    This function uses the xdotool utility to perform a right-click (mouse button 3) operation.
    """

    subprocess.run("xdotool click 3", shell=True)


def left_click_at(x,y):
    """
    This function uses the xdotool utility to move the mouse to the provided coordinates and perform
    a left-click (mouse button 1) operation.

    Parameters:
    x (int): The x-coordinate on the screen where the left-click operation needs to be performed.
    y (int): The y-coordinate on the screen where the left-click operation needs to be performed.
    """

    subprocess.run(f"xdotool mousemove {x} {y} click 1", shell=True)


def middle_click_at(x,y):
    """
    This function uses the xdotool utility to move the mouse to the provided coordinates and perform
    a middle-click (mouse button 2) operation.

    Parameters:
    x (int): The x-coordinate on the screen where the middle-click operation needs to be performed.
    y (int): The y-coordinate on the screen where the middle-click operation needs to be performed.
    """

    subprocess.run(f"xdotool mousemove {x} {y} click 2", shell=True)


def right_click_at(x,y):
    """
    This function uses the xdotool utility to move the mouse to the provided coordinates and perform
    a right-click (mouse button 3) operation.

    Parameters:
    x (int): The x-coordinate on the screen where the right-click operation needs to be performed.
    y (int): The y-coordinate on the screen where the right-click operation needs to be performed.
    """

    subprocess.run(f"xdotool mousemove {x} {y} click 3", shell=True)


def mouse_move(x, y):
    """
    This function uses the xdotool utility to move the mouse to the provided coordinates.

    Parameters:
    x (int): The x-coordinate on the screen where the mouse cursor needs to be moved.
    y (int): The y-coordinate on the screen where the mouse cursor needs to be moved.
    """

    subprocess.run(f"xdotool mousemove {x} {y}", shell=True)


def scroll_up(x):
    """
    Simulates scrolling up by a specified x using xdotool.
    :param x: The x of scrolling to be done vertically (in pixels)
    """
    subprocess.run(['xdotool', 'mousemove_relative', '0', f'-{x}'])

def scroll_down(x):
    """
    Simulates scrolling down by a specified x using xdotool.
    :param x: The x of scrolling to be done vertically (in pixels)
    """
    subprocess.run(['xdotool', 'mousemove_relative', '0', f'{x}'])

def scroll_left(x):
    """
    Simulates scrolling left with the mouse wheel using xdotool.
    :param x: The x of scrolling to be done horizontally (in pixels)
    """
    subprocess.run(['xdotool', 'mousemove_relative', '--', f'-{x}', '0'])

def scroll_right(x):
    """
    Simulates scrolling right with the mouse wheel using xdotool.
    :param x: The x of scrolling to be done horizontally (in pixels)
    """
    subprocess.run(['xdotool', 'mousemove_relative', f'{x}', '0'])


# $ xdotool click 3
# Replace “3” with with any number from the reference below:

# 1 – Left click
# 2 – Middle click
# 3 – Right click
# 4 – Scroll wheel up
# 5 – Scroll wheel down

# $ xdotool mousemove 100 100 click 3