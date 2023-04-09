import subprocess
import re
from time import sleep
import pyautogui
import random


def capture(_img):
    # Capture the entire screen
    screenshot = pyautogui.screenshot()
    print(_img)
    # Save the screenshot to the same file, overwriting the previous screenshot
    screenshot.save(_img)

def click_one(x, y):
    """
    This function uses the xdotool utility to move the mouse to given x and y coordinates on the screen and
    performs a left-click (mouse button 1) operation.

    Parameters:
    x (int): The x-coordinate on the screen where the left-click operation needs to be performed.
    y (int): The y-coordinate on the screen where the left-click operation needs to be performed.
    """
    
    # # move the mouse to a specific coordinate
    pyautogui.moveTo(x, y, duration=0.6)

    # click the left mouse button
    pyautogui.click(x, y)

def click_two(x, y):
    """
    This function uses the xdotool utility to move the mouse to given x and y coordinates on the screen and
    performs a right-click (mouse button 2) operation.

    Parameters:
    x (int): The x-coordinate on the screen where the right-click operation needs to be performed.
    y (int): The y-coordinate on the screen where the right-click operation needs to be performed.
    """
    # move the mouse to a specific coordinate
    pyautogui.moveTo(x, y)

    # Move the mouse to the provided x and y coordinates and perform a right click
    pyautogui.doubleClick(x, y)


def write(_text, delay):
    """
    This function uses the xdotool utility to simulate keyboard input and type out the provided text.

    Parameters:
    _text (str): The text to be typed out.
    """

    if delay: 
        delay = 0.2
        pyautogui.typewrite(_text, interval=delay)
    else:
        pyautogui.write(_text)


def press_key(x):
    """
    This function uses the xdotool utility to simulate key presses on the keyboard.

    Parameters:
    x (str): The key to be press. For example, 'ctrl+v', 'ctrl+t', 'shift+tab' etc.
    """
    # press and release a key
    pyautogui.press(x)


def left_click():
    """
    This function uses the xdotool utility to perform a left-click (mouse button 1) operation.
    """

    # click the left mouse button
    pyautogui.click()

def middle_click():
    """
    This function uses the xdotool utility to perform a middle-click (mouse button 2) operation.
    """

    pyautogui.middleClick()


def right_click():
    """
    This function uses the xdotool utility to perform a right-click (mouse button 3) operation.
    """

    pyautogui.rightClick()

def left_click_at(x,y):
    """
    This function uses the xdotool utility to move the mouse to the provided coordinates and perform
    a left-click (mouse button 1) operation.

    Parameters:
    x (int): The x-coordinate on the screen where the left-click operation needs to be performed.
    y (int): The y-coordinate on the screen where the left-click operation needs to be performed.
    """

    pyautogui.click(x, y)


def middle_click_at(x,y):
    """
    This function uses the xdotool utility to move the mouse to the provided coordinates and perform
    a middle-click (mouse button 2) operation.

    Parameters:
    x (int): The x-coordinate on the screen where the middle-click operation needs to be performed.
    y (int): The y-coordinate on the screen where the middle-click operation needs to be performed.
    """

    pyautogui.middleClick(x, y)


def right_click_at(x,y):
    """
    This function uses the xdotool utility to move the mouse to the provided coordinates and perform
    a right-click (mouse button 3) operation.

    Parameters:
    x (int): The x-coordinate on the screen where the right-click operation needs to be performed.
    y (int): The y-coordinate on the screen where the right-click operation needs to be performed.
    """

    pyautogui.rightClick(x, y)

def mouse_move(x, y):
    """
    This function uses the xdotool utility to move the mouse to the provided coordinates.

    Parameters:
    x (int): The x-coordinate on the screen where the mouse cursor needs to be moved.
    y (int): The y-coordinate on the screen where the mouse cursor needs to be moved.
    """

    # move the mouse to a specific coordinate
    pyautogui.moveTo(x, y)

def scroll_up(x):
    """
    Simulates scrolling up by a specified x using xdotool.
    :param x: The x of scrolling to be done vertically (in pixels)
    """
    pyautogui.scroll(x)

def scroll_down(x):
    """
    Simulates scrolling down by a specified x using xdotool.
    :param x: The x of scrolling to be done vertically (in pixels)
    """
    pyautogui.scroll(-x)

def scroll_left(x):
    """
    Simulates scrolling left with the mouse wheel using xdotool.
    :param x: The x of scrolling to be done horizontally (in pixels)
    """
    pyautogui.hscroll(x)

def scroll_right(x):
    """
    Simulates scrolling right with the mouse wheel using xdotool.
    :param x: The x of scrolling to be done horizontally (in pixels)
    """
    pyautogui.hscroll(-x)

def wait(x):
    if not x:
        x = 3
    sleep(x)

def mouseToggleUp(self):
    # Get the x and y coordinates of the target object
    x, y = self.cords[0], self.cords[1]
    pyautogui.mouseUp(x=x, y=y, button='left')

def mouseToggleDown(self):
    # Get the x and y coordinates of the target object
    x, y = self.cords[0], self.cords[1]
    pyautogui.mouseDown(x=x, y=y, button='left')
