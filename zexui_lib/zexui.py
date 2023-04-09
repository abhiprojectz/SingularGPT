# from google.colab.patches import cv2_imshow
import re 
import cv2
import subprocess
import json 
import numpy as np 
from vision.vision_utils import detect_component
from zexui_lib.base_functions import * 
from time import sleep 
from config.CONFIG import _PLATFORM
"""
Main automation library that automates the device level stuffs.
"""

if _PLATFORM == 'windows':
    from .py_gui_commands import * 
elif _PLATFORM == 'linux':
    from .x11_commands import *


class ZexUI(object):
    """
    Main ZEXUI library for the automation stuff.
    """
    def __init__(self):
        # This variable stores the path of the captured image in PNG format.
        self.capture_png = 'data/input/curr_img.png'
        self.img_path = ""    
        self.cords = ""       
        self.img_chunk = ""   
        self._type_elm = ""   

    def capture(self):
        """
        This function captures the screenshot of the current screen and saves it
        to the path specified by self.capture_png variable.
        """
        capture(self.capture_png)
        self.img_path = self.capture_png

    def _preprocess_img(self, _img):
        """
        This function preprocesses the image by:
        - Reading the image using OpenCV (cv2).
        - Converting the image to grayscale.
        - Applying thresholding to the grayscale image using Binary Inverse Thresholding.
        - Calling `detect_component` function with input_path_img, output_root, is_ocr, and is_merge arguments,
          and returning self.

        Parameters:
        _img (str): The path of the image which is to be preprocessed.

        Returns:
        self: The object of the class.
        """
        img = cv2.imread(_img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY_INV)
        # input_path_img = 'data/input/tx_5.PNG'
        output_root = 'data/output'
        # detect_component(input_path_img, output_root, is_ocr=True, is_ip=False, is_merge=False)
        return self


    def text(self, text):
        """
        Finds the center of the bounding box around a given text in an image.

        Args:
            img_path (str): Path to the input image.
            text (str): The text to search for.

        Returns:
            Tuple[int, int]: The (x, y) coordinates of the center of the bounding box.
        """
        # Getting latest screenshot of the screen/display
        self.capture()

        # Detect text components in the image using OCR.
        input_path_img = self.img_path
        output_root = 'data/output'
        detect_component(input_path_img, output_root, _is_text=True, _is_element=False)

        # Read JSON data
        with open('data/output/ocr/curr_img.json', 'r') as f:
            data = json.load(f)

        # Create a white image
        img = 255 * np.ones((200, 1900, 3), dtype=np.uint8)

        _res = None
        # Draw rectangles and points on the image
        for compo in data['texts']:
            # Removes anyn trailings spaces from the text
            if compo['content'].lstrip() == text:
                pt1 = (compo['column_min'], compo['row_min'])
                pt2 = (compo['column_max'], compo['row_max'])
                color = (0, 0, 255)  # BGR color code for red
                thickness = 2
                # img = cv2.rectangle(img, pt1, pt2, color, thickness)
                center = ((compo['column_min'] + compo['column_max']) // 2,
                        (compo['row_min'] + compo['row_max']) // 2)
                radius = 2
                # img = cv2.circle(img, center, radius, color, thickness=-1)
                # print(center)
                _res = center

        if _res == None:
            raise ValueError(f"The {text} is not present in the current component")

        # Display the image
        # cv2_imshow(img)

        self.cords = _res
        self._type_elm = 'texts'
        return self
  

    def textRegex(self, text_regex):
        """
        This function performs text detection and recognition on the processed image
        using the path specified in self.img_path. It uses `detect_component` function
        with input_path_img, output_root, is_ocr, and is_merge arguments.

        Parameters:
        text_regex (str): The text recognised by OCR. It is not used in the code provided.

        Returns:
        Text co-ordinates instance.
        """

        # Getting latest screenshot of the screen/display
        self.capture()

        input_path_img = self.img_path
        output_root = 'data/output'
        detect_component(input_path_img, output_root, _is_text=True, _is_element=False)

        # Read JSON data
        with open('data/output/ocr/curr_img.json', 'r') as f:
            data = json.load(f)

        # Create a white image
        img = 255 * np.ones((200, 1900, 3), dtype=np.uint8)

        _res = None
        # Draw rectangles and points on the image
        for compo in data['texts']:
            if re.search(text_regex, compo['content'].lstrip()):
                pt1 = (compo['column_min'], compo['row_min'])
                pt2 = (compo['column_max'], compo['row_max'])
                color = (0, 0, 255)  # BGR color code for red
                thickness = 2
                # img = cv2.rectangle(img, pt1, pt2, color, thickness)
                center = ((compo['column_min'] + compo['column_max']) // 2,
                        (compo['row_min'] + compo['row_max']) // 2)
                radius = 2
                # img = cv2.circle(img, center, radius, color, thickness=-1)
                # print(center)
                _res = center

        if _res == None:
            raise ValueError(f"The {text_regex} is not present in the current component")

        # Display the image
        # cv2_imshow(img)

        self.cords = _res
        self._type_elm = 'texts'
        return self


    def textContains(self, text):
        """
        This function checks whether the output elements contains the text or not.
        """
        # Getting latest screenshot of the screen/display
        self.capture()

        input_path_img = self.img_path
        output_root = 'data/output'
        detect_component(input_path_img, output_root, _is_text=True, _is_element=False)

        # Read JSON data
        with open('/content/SingularGPT/data/output/ocr/curr_img.json', 'r') as f:
            data = json.load(f)

        # Create a white image
        img = 255 * np.ones((200, 1900, 3), dtype=np.uint8)

        _res = None
        # Draw rectangles and points on the image
        for compo in data['texts']:
            if text in compo['content'].lstrip():
                pt1 = (compo['column_min'], compo['row_min'])
                pt2 = (compo['column_max'], compo['row_max'])
                color = (0, 0, 255)  # BGR color code for red
                thickness = 2
                # img = cv2.rectangle(img, pt1, pt2, color, thickness)
                center = ((compo['column_min'] + compo['column_max']) // 2,
                        (compo['row_min'] + compo['row_max']) // 2)
                radius = 2
                # img = cv2.circle(img, center, radius, color, thickness=-1)
                # print(center)
                _res = center

        if _res == None:
            raise ValueError(f"The {text} is not present in the current component")

        # Display the image
        # cv2_imshow(img)

        self.cords = _res
        self._type_elm = 'texts'
        return self


    def image(self, target_img):
        """
        This function takes an input target image and finds its location on the main image using the find_location_of_img_obj function. 
        It then calculates the center coordinates of the target image using its height and width. 
        The coordinates are saved in self.cords and the type of element is saved in _type_elm as compos. 
        """
        # input_path_img = self.img_path
        # output_root = 'data/output'
        # detect_component(input_path_img, output_root, is_ocr=False, is_ip=True, is_merge=False)
        self.capture()
        
        _x = find_location_of_img_obj(self.img_path, target_img)
        _img = cv2.imread(target_img)
        height, width, c = _img.shape

        # center_coordinates = (x + int(width/2), y + int(height/2))    
        # radius = 2
        # color = (0, 78, 255)
        # thickness = 2
        # cv2.circle(cv2.imread(self.img_path), center_coordinates, radius, color, thickness)
        # cv2_imshow(cv2.imread(self.img_path))
        
        self.cords = (_x[0] + int(width/2), _x[1] + int(height/2))
        self._type_elm = 'compos'
        return self


    def get_all_objects(self, _type_elm):
        """
        Returns the list of all the objects that are so far detected and saved in the ocr results json format.
        """


        if _type_elm == 'texts':
            _el_type = 'texts'
            with open('data/output/ocr/curr_img.json', 'r') as f:
                data = json.load(f)
        else:
            _el_type = 'compos'
            input_path_img = self.img_path
            output_root = 'data/output'
            detect_component(input_path_img, output_root, _is_text=False, _is_element=True)

            with open('data/output/element/curr_img.json', 'r') as f:
                data = json.load(f)  

        objects = []
        objs = []

        # Draw rectangles and points on the image
        for compo in data[_el_type]:
            pt1 = (compo['column_min'], compo['row_min'])
            pt2 = (compo['column_max'], compo['row_max'])
            color = (0, 0, 255)  # BGR color code for red
            thickness = 2
            radius = 2
            # img = cv2.rectangle(img, pt1, pt2, color, thickness)
            center = ((compo['column_min'] + compo['column_max']) // 2,
                    (compo['row_min'] + compo['row_max']) // 2)
            # img = cv2.circle(img, center, radius, color, thickness=-1)
            objects.append(center)
            objs.append(compo)

        return objects, objs


    def findLeftOf(self):
        """
        This function finds the object present to the left of the target object based on
        the coordinates of the target object `cords` and the list of objects obtained after
        calling the `get_all_objects` method with `self._type_elm` as argument.
        It then returns the object present to the left of the target object.

        Returns:
        self (object): The object present to the left of the target object returned by this method.
        """
        # Extract all objects and object labels of type element
        objects, objs = self.get_all_objects(self._type_elm)

        # Find the target object for which we're searching for the object to the left
        target_obj = self.cords

        # Find the object present to the bottom of the target object
        x = find_obj_to_bottom_of_target_obj(target_obj, objects)

        # Get the index of the object present to the bottom of the target object
        x_ind = objects.index(x)

        # Get the object present to the left of the target object
        _compo = objs[x_ind]

        # Update the coordinates of the target object to the bottom object coordinates
        self.cords = x

        # Return the object present to the left of the target object
        return self

    def findRightOf(self):
        """
        This function finds the object present to the right of the target object based on
        the coordinates of the target object `cords` and the list of objects obtained after
        calling the `get_all_objects` method with `self._type_elm` as argument.
        It then returns the object present to the right of the target object.

        Returns:
        self (object): The object present to the right of the target object returned by this method.
        """
        # Extract all objects and object labels of type element
        objects, objs = self.get_all_objects(self._type_elm)

        # Find the target object for which we're searching for the object to the right
        target_obj = self.cords

        # Find the object present to the right of the target object
        x = find_obj_to_right_of_target_obj(target_obj, objects)

        # Get the index of the object present to the right of the target object
        x_ind = objects.index(x)

        # Get the object present to the right of the target object
        _compo = objs[x_ind]

        # Update the coordinates of the target object to the right object coordinates
        self.cords = x

        # Return the object present to the right of the target object
        return self


    def findTopOf(self):
        """
        This function finds the object present at the top of the target object based on
        the coordinates of the target object `cords` and the list of objects obtained after
        calling the `get_all_objects` method with `self._type_elm` as argument.
        It then returns the object present at the top of the target object.

        Returns:
        self (object): The object present at the top of the target object returned by this method.
        """
        # Extract all objects and object labels of type element
        objects, objs = self.get_all_objects(self._type_elm)

        # Find the target object for which we're searching for the object at the top
        target_obj = self.cords

        # Find the object present at the top of the target object
        x = find_obj_to_top_of_target_obj(target_obj, objects)

        # Get the index of the object present at the top of the target object
        x_ind = objects.index(x)

        # Get the object present at the top of the target object
        _compo = objs[x_ind]

        # Update the coordinates of the target object to the top object coordinates
        self.cords = x

        # Return the object present at the top of the target object
        return self


    def findBottomOf(self):
        """
        This function finds the object present at the bottom of the target object based on
        the coordinates of the target object `cords` and the list of objects obtained after
        calling the `get_all_objects` method with `self._type_elm` as argument.
        It then returns the object present at the bottom of the target object.

        Returns:
        self (object): The object present at the bottom of the target object returned by this method.
        """
        # Extract all objects and object labels of type element
        objects, objs = self.get_all_objects(self._type_elm)

        # Find the target object for which we're searching for the object at the bottom
        target_obj = self.cords

        # Find the object present at the bottom of the target object
        x = find_obj_to_bottom_of_target_obj(target_obj, objects)

        # Get the index of the object present at the bottom of the target object
        x_ind = objects.index(x)

        # Get the object present at the bottom of the target object
        _compo = objs[x_ind]

        # Update the coordinates of the target object to the bottom object coordinates
        self.cords = x

        # Return the object present at the bottom of the target object
        return self

  # Todo
  # def or(self):
  #   pass 


    def findNearestTo(self):
        objects, objs = self.get_all_objects(self._type_elm)
        # Define the list of coordinates
        coords = objects

        # Define the target point
        target_point = self.cords

        # Calculate the Euclidean distance between the target point and all other points
        distances = [np.linalg.norm(np.array(coord) - np.array(target_point)) for coord in coords]

        # Find the index of the nearest point
        nearest_idx = np.argmin(distances)

        # Get the nearest point
        nearest_point = coords[nearest_idx]

        # # Create a white image
        # img = np.zeros((512, 800, 3), np.uint8)
        # img.fill(255)

        # # Draw a red circle around the nearest point
        # cv2.circle(img, nearest_point, 10, (0, 0, 255), -1)

        # # Draw green circles around all other points
        # for coord in coords:
        #     if coord != nearest_point:
        #         cv2.circle(img, coord, 10, (0, 255, 0), -1)
        # Display the image
        # cv2.imshow('image', img)

        # Print the coordinates of the nearest point
        print("Nearest point coordinates:", nearest_point)
        self.cords = nearest_point
        return self


    def write(self, text):
        delay = True
        write(text, delay)


    def click(self):
        """
        This function gets the x and y coordinates of the target object `cords` and calls the `click_one` function
        by passing the x and y coordinates as arguments.

        """
        # Get the x and y coordinates of the target object
        x = self.cords[0]
        y = self.cords[1]
        sleep(1)

        # Print the x and y coordinates of the target object
        print(x, y)

        # Call the `click_one` function by passing the x and y coordinates as arguments
        click_one(x, y)


    def mouseMoveTo(self, x, y):
        """
        This function moves the mouse cursor to the provided x and y coordinates.

        Parameters:
        x (int): The x-coordinate to which the mouse cursor has to be moved.
        y (int): The y-coordinate to which the mouse cursor has to be moved.
        """
        # Move the mouse cursor to the provided x and y coordinates
        mouse_move(x, y)


    def mouseMove(self):
        """
        This function moves the mouse cursor to the x and y coordinates of the target object.

        Parameters:
        None

        Returns:
        None
        """
        # Get the x and y coordinates of the target object
        x, y = self.cords[0], self.cords[1]

        # Move the mouse cursor to the x and y coordinates of the target object
        mouse_move(x, y)

    def wait(self, x):
        wait(x)

    def scroll_up(self, x):
        scroll_up(x)

    def scroll_down(self, x):
        scroll_down(x)

    def scroll_left(self, x):
        scroll_left(self, x)

    def scroll_right(self, x):
        scroll_right(self, x)

    def mouseToggleUp(self):
        # Get the x and y coordinates of the target object
        x, y = self.cords[0], self.cords[1]
        mouseToggleUp(x, y)

    def mouseToggleDown(self):
        # Get the x and y coordinates of the target object
        x, y = self.cords[0], self.cords[1]
        mouseToggleDown(x, y)

