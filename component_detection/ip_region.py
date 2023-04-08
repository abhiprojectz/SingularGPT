import cv2
from os.path import join as pjoin
import time
import json
import numpy as np

import component_detection.lib_ip.ip_preprocessing as pre
import component_detection.lib_ip.ip_draw as draw
import component_detection.lib_ip.ip_detection as det
import component_detection.lib_ip.file_utils as file
import component_detection.lib_ip.Component as Compo


def nesting_inspection(org, grey, compos, ffl_block):
    '''
    Inspect all big compos through block division by flood-fill
    :param ffl_block: gradient threshold for flood-fill
    :return: nesting compos
    '''
    nesting_compos = []
    
    for compo in compos:
        replace, n_compos = inspect_compo(org, grey, compo, ffl_block)
        if not replace:
            nesting_compos += n_compos
    
    return nesting_compos


def inspect_compo(org, grey, compo, ffl_block):
    '''
    Inspect a single component and detect its nested components
    :return: a tuple of two elements (replace, n_compos)
    replace: whether the component has redundant nested components
    n_compos: a list of nested components
    '''
    replace = False
    n_compos = []
    
    if compo.height > 50:
        clip_grey = compo.compo_clipping(grey)
        n_compos = detect_nested_components(org, clip_grey, compo.bbox.col_min, compo.bbox.row_min, ffl_block)
        replace = check_for_redundant_components(compo, n_compos)
        
    return replace, n_compos


def detect_nested_components(org, clip_grey, col_min, row_min, grad_thresh):
    '''
    Detect nested components inside a component
    :return: a list of nested components
    '''
    n_compos = det.nested_components_detection(clip_grey, org, grad_thresh=grad_thresh)
    Compo.cvt_compos_relative_pos(n_compos, col_min, row_min)
    return n_compos


def check_for_redundant_components(compo, n_compos):
    '''
    Check if any of the nested components are redundant
    :return: a boolean value representing whether the component has redundant nested components or not
    '''
    for n_compo in n_compos:
        if n_compo.redundant:
            compo.update(n_compo)
            return True
    return False


# Pre-processing
def preprocess_image(input_img_path: str, resize_by_height: int, zexui_params):
    """
    Pre-processes the input image by reading it, converting it to grayscale, and binarizing it.
    
    Args:
    - input_img_path (str): Path to the input image
    - resize_by_height (int): Height to resize the input image to
    - zexui_params (Dict): Dictionary of parameters for the pre-processing steps
    
    Returns:
    - Tuple of (original image, grayscale image, binarized image)
    """
    # Read the input image and convert it to grayscale
    org, grey = pre.read_img(input_img_path, resize_by_height)
    
    # Binarize the grayscale image
    binary = pre.binarization(org, grad_min=int(zexui_params['min-grad']))
    
    return org, grey, binary

# Element detection
def detect_elements(binary: np.ndarray, zexui_params):
    """
    Detects UI elements from the binarized image.
    
    Args:
    - binary (np.ndarray): Binarized image
    - zexui_params (Dict): Dictionary of parameters for the element detection step
    
    Returns:
    - List of Compo objects representing the detected UI elements
    """
    # Remove lines from the binarized image
    det.rm_line(binary)
    
    # Detect components from the binarized image
    uicompos = det.component_detection(binary, min_obj_area=int(zexui_params['min-ele-area']))
    
    return uicompos


# Refinement
def refine_results(uicompos, org, binary, zexui_params):
    # Filter out components smaller than a certain minimum area
    uicompos = det.compo_filter(uicompos, min_area=int(zexui_params['min-ele-area']), img_shape=binary.shape)
    
    # Merge intersecting components
    uicompos = det.merge_intersected_compos(uicompos)
    
    # Recognize components that form a block
    det.compo_block_recognition(binary, uicompos)
    
    # Merge contained components that are not part of a block
    if zexui_params['merge-contained-ele']:
        uicompos = det.remove_contained_non_block_components(uicompos)
    
    # Update component information, including their size, position, and containment hierarchy
    Compo.compos_update(uicompos, org.shape)
    Compo.compos_containment(uicompos)
    
    # Return the updated component list
    return uicompos


# Component detection
def compo_detection(input_img_path, output_root, zexui_params, resize_by_height):
    start = time.process_time()
    name = input_img_path.split('/')[-1][:-4] if '/' in input_img_path else input_img_path.split('\\')[-1][:-4]
    ip_root = file.build_directory(pjoin(output_root, "element"))
    
    # Pre-processing
    org, grey, binary = preprocess_image(input_img_path, resize_by_height, zexui_params)
    
    # Element detection
    uicompos = detect_elements(binary, zexui_params)
    
    # Refinement
    uicompos = refine_results(uicompos, org, binary, zexui_params)
    
    # Nesting inspection
    uicompos += nesting_inspection(org, grey, uicompos, ffl_block=zexui_params['ffl-block'])
    Compo.compos_update(uicompos, org.shape)
    
    # Draw bounding box and save detection result
    draw.draw_bounding_box(org, uicompos, name='merged compo', write_path=pjoin(ip_root, name + '.jpg'))
    Compo.compos_update(uicompos, org.shape)
    file.save_corners_json(pjoin(ip_root, name + '.json'), uicompos)
    
    # calculate the elapsed time of the compositional detection process
    elapsed_time = time.process_time() - start

    print(f"[Component Detection Completed in {elapsed_time:.3f} seconds.]\nOutput JSON file path: {pjoin(ip_root, name + '.json')}")
