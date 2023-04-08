from os.path import join as pjoin
import cv2
import os
import numpy as np
from config.CONFIG import _OCR


"""
Main Functions for Components detection purposes.
"""

# Getting highest between width and height based on numpy array image 
def get_longest_side(img):
    height, width, channels = img.shape
    if height > width:
        return height
    else:
        return width 
    

# For debugging purposes
def resize_height_by_longest_edge(img_path, resize_length):
    org = cv2.imread(img_path)
    height, width = org.shape[:2]
    
    if height > width:
        return resize_length
    else:
        return int(resize_length * (height / width))


# Detecting text 
def detect_text(input_path_img, output_root):
    # Import the text detection module and call the text_detection function
    
    import text_detection.text_detection as text
    # Create the output directory
    os.makedirs(pjoin(output_root, 'ocr'), exist_ok=True)
    text.text_detection(input_path_img, output_root, method=_OCR)



# Detecting components using opencv approaches
def detect_component_by_ip(input_path_img, output_root, key_params, resized_height):
    os.makedirs(pjoin(output_root, 'element'), exist_ok=True)
    import component_detection.ip_region as ip
    ip.compo_detection(input_path_img, output_root, key_params, resize_by_height=resized_height)


# Detecting both text and components at once 
def detect_components_and_text(input_path_img, output_root, _is_text, _is_element):
    key_params = {'min-grad':3, 'ffl-block':5, 'min-ele-area':25, 'max-word-inline-gap':4, 'max-line-gap':4,
                    'merge-contained-ele':True, 'merge-line-to-paragraph':False, 'remove-bar':True}
    resize_length = get_longest_side(cv2.imread(input_path_img))
    resized_height = resize_height_by_longest_edge(input_path_img, resize_length)

    if _is_text:
        detect_text(input_path_img, output_root)

    if _is_element:
        detect_component_by_ip(input_path_img, output_root, key_params, resized_height)


def detect_component(input_path_img, output_root, _is_text, _is_element):
    key_params = {'min-grad':3, 'ffl-block':5, 'min-ele-area':25, 'max-word-inline-gap':4, 'max-line-gap':4,
                    'merge-contained-ele':True, 'merge-line-to-paragraph':False, 'remove-bar':True}
    resize_length = get_longest_side(cv2.imread(input_path_img))
    resized_height = resize_height_by_longest_edge(input_path_img, resize_length)
    is_clf = False

    if _is_text:
        detect_text(input_path_img, output_root)

    if _is_element:
        detect_component_by_ip(input_path_img, output_root, key_params, resized_height)



# set input image path
# input_path_img = 'data/input/gg.PNG'
# output_root = 'data/output'

# detect_component(input_path_img, output_root, _is_text=True, _is_element=True)
