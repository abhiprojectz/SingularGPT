import cv2
import numpy as np

import component_detection.lib_ip.ip_draw as draw
import component_detection.lib_ip.ip_preprocessing as pre
from component_detection.lib_ip.Component import Component
import component_detection.lib_ip.Component as Compo
from config.CONFIG_ZEXUI import Config
C = Config()


def merge_intersected_corner(compos, org, is_merge_contained_ele, max_gap=(0, 0), max_ele_height=25):
    '''
    Merge compos that intersect or are close to each other into one component.

    :param compos: list of Component objects
    :param org: original image
    :param is_merge_contained_ele: if True, merge compos nested in others
    :param max_gap: (horizontal_distance, vertical_distance) to be merge into one line/column
    :param max_ele_height: if higher than it, recognize the compo as text
    :return: list of Component objects
    '''
    # Check if any compos have been merged
    changed = False
    # Create a new list for merged compos
    new_compos = []
    # Update the dimensions of each compo
    Compo.compos_update(compos, org.shape)

    # Loop through each compo
    for i in range(len(compos)):
        merged = False
        cur_compo = compos[i]
        # Loop through each merged compo
        for j in range(len(new_compos)):
            # Get the relation between compo[i] and compo[j]
            relation = cur_compo.compo_relation(new_compos[j], max_gap)
            
            # Merge compo[i] to compo[j] if:
            # 1. compo[j] contains compo[i]
            # 2. compo[j] intersects with compo[i] with certain intersection over union (iou)
            # 3. is_merge_contained_ele is True and compo[j] is contained in compo[i]
            if relation == 1 or relation == 2 or (is_merge_contained_ele and relation == -1):
                new_compos[j].compo_merge(cur_compo)
                cur_compo = new_compos[j]
                merged = True
                changed = True
         
        # Append the unmerged compo to new_compos
        if not merged:
            new_compos.append(compos[i])

    # If no compos have been merged, return the original list of compos
    if not changed:
        return compos
    # Otherwise, call the function recursively on the new_compos list until no more compos can be merged
    else:
        return merge_intersected_corner(new_compos, org, is_merge_contained_ele, max_gap, max_ele_height)
    

def merge_intersected_compos(compos):
    '''
    Merge intersected components in a list of components.

    :param compos: a list of Component objects
    :return: a new list of Component objects
    '''
    changed = True
    while changed:
        changed = False
        temp_set = []
        for compo_a in compos:
            merged = False
            for compo_b in temp_set:
                if compo_a.compo_relation(compo_b) == 2:
                    compo_b.compo_merge(compo_a)
                    merged = True
                    changed = True
                    break
            if not merged:
                temp_set.append(compo_a)
        compos = temp_set.copy()
    return compos

def compo_relation(compo_a, compo_b):
    '''
    Check the relation between two components.

    :param compo_a: a Component object
    :param compo_b: a Component object
    :return: an integer indicating the relation: 0 for no intersection, 1 for compo_b contains compo_a,
             2 for compo_a intersects compo_b, and -1 for compo_a contains compo_b
    '''
    relation = 0
    if compo_b.contains(compo_a):
        relation = 1
    elif compo_a.intersects(compo_b):
        iou = compo_a.intersection_over_union(compo_b)
        if iou >= 0.5:
            relation = 2
    elif compo_a.contains(compo_b):
        relation = -1
    return relation

def contains(compo_a, compo_b):
    '''
    Check if a component contains another component.

    :param compo_a: a Component object
    :param compo_b: a Component object
    :return: a boolean indicating if compo_a contains compo_b
    '''
    return compo_a.bounding_box.contains(compo_b.bounding_box)

def intersects(compo_a, compo_b):
    '''
    Check if a component intersects another component.

    :param compo_a: a Component object
    :param compo_b: a Component object
    :return: a boolean indicating if compo_a intersects compo_b
    '''
    return compo_a.bounding_box.intersects(compo_b.bounding_box)

def intersection_over_union(compo_a, compo_b):
    '''
    Calculate the intersection over union (IOU) between two components.

    :param compo_a: a Component object
    :param compo_b: a Component object
    :return: a float representing the IOU between compo_a and compo_b
    '''
    intersection = compo_a.bounding_box.intersection(compo_b.bounding_box)
    union = compo_a.bounding_box.union(compo_b.bounding_box)
    iou = intersection.area / union.area
    return iou

def compo_merge(compo_a, compo_b):
    '''
    Merge two components.

    :param compo_a: a Component object
    :param compo_b: a Component object
    :return: None
    '''
    new_bbox = compo_a.bounding_box.union(compo_b.bounding_box)
    new_compo = Component(new_bbox)
    new_compo.children = compo_a.children + compo_b.children
    compo_a.children = []
    compo_b.children = []
    return new_compo


def remove_contained_non_block_components(compos):
    '''
    Remove components that are contained by others and not of 'Block' category
    '''
    marked = np.full(len(compos), False)
    mark_contained_non_block_components(compos, marked)
    return get_unmarked_components(compos, marked)


def mark_contained_non_block_components(compos, marked):
    '''
    Mark contained non-block components
    '''
    for i in range(len(compos) - 1):
        for j in range(i + 1, len(compos)):
            relation = compos[i].compo_relation(compos[j])
            if relation == -1 and compos[j].category != 'Block':
                marked[i] = True
            if relation == 1 and compos[i].category != 'Block':
                marked[j] = True

def get_unmarked_components(compos, marked):
    '''
    Get unmarked components
    '''
    new_compos = []
    for i in range(len(marked)):
        if not marked[i]:
            new_compos.append(compos[i])
    return new_compos


def merge_text(compos, org_shape, max_word_gad=4, max_word_height=20):

    def is_text(compo):
        """
        Check if the component is text based on its height and category.

        Args:
            compo: a component

        Returns:
            True if the component is text, False otherwise.
        """
        height = compo.height
        # ignore non-text
        # if height / row > max_word_height_ratio\
        #         or compos[i].category != 'Text':
        if height > max_word_height:
            return False
        else:
            return True

    def is_same_line(compo_a, compo_b):
        """
        Check if two components are on the same line based on their bounding boxes.

        Args:
            compo_a: a component
            compo_b: a component

        Returns:
            True if the two components are on the same line, False otherwise.
        """
        (col_min_a, row_min_a, col_max_a, row_max_a) = compo_a.put_bbox()
        (col_min_b, row_min_b, col_max_b, row_max_b) = compo_b.put_bbox()

        col_min_s = max(col_min_a, col_min_b)
        col_max_s = min(col_max_a, col_max_b)
        row_min_s = max(row_min_a, row_min_b)
        row_max_s = min(row_max_a, row_max_b)

        # on the same line
        # if abs(row_min_a - row_min_b) < max_word_gad and abs(row_max_a - row_max_b) < max_word_gad:
        if row_min_s < row_max_s:
            # close distance
            if col_min_s < col_max_s or \
                    (0 < col_min_b - col_max_a < max_word_gad) or (0 < col_min_a - col_max_b < max_word_gad):
                return True
        return False

    def merge_components(compo_a, compo_b):
        """
        Merge two components into a new one.

        Args:
            compo_a: a component
            compo_b: a component

        Returns:
            A new component that is the merger of the two input components.
        """
        new_compo = compo_a.compo_copy()
        new_compo.compo_merge(compo_b)
        return new_compo

    def merge_text_recursive(compos):
        """
        Recursive function that merges text components until no more mergers can be made.

        Args:
            compos: a list of components

        Returns:
            A new list of merged components.
        """
        changed = False
        new_compos = []
        for i in range(len(compos)):
            merged = False
            if not is_text(compos[i]):
                new_compos.append(compos[i])
                continue
            for j in range(len(new_compos)):
                if not is_text(new_compos[j]):
                    continue
                if is_same_line(compos[i], new_compos[j]):
                    merged_compo = merge_components(compos[i], new_compos[j])
                    new_compos[j] = merged_compo
                    merged = True
                    changed = True
                    break
            if not merged:
                new_compos.append(compos[i])

        if not changed:
            return new_compos
        else:
            return merge_text_recursive(new_compos)

    return merge_text_recursive(compos)



def rm_top_or_bottom_corners(components, org_shape, top_bottom_height=C.THRESHOLD_TOP_BOTTOM_BAR):
    new_compos = []
    height, width = org_shape[:2]
    for compo in components:
        (column_min, row_min, column_max, row_max) = compo.put_bbox()
        # remove big ones
        # if (row_max - row_min) / height > 0.65 and (column_max - column_min) / width > 0.8:
        #     continue
        if not (row_max < height * top_bottom_height[0] or row_min > height * top_bottom_height[1]):
            new_compos.append(compo)
    return new_compos


def rm_line_v_h(binary, show=False, max_line_thickness=C.THRESHOLD_LINE_THICKNESS):
    def check_continuous_line(line, edge):
        continuous_length = 0
        line_start = -1
        for j, p in enumerate(line):
            if p > 0:
                if line_start == -1:
                    line_start = j
                continuous_length += 1
            elif continuous_length > 0:
                if continuous_length / edge > 0.6:
                    return [line_start, j]
                continuous_length = 0
                line_start = -1

        if continuous_length / edge > 0.6:
            return [line_start, len(line)]
        else:
            return None

    def extract_line_area(line, start_idx, flag='v'):
        for e, l in enumerate(line):
            if flag == 'v':
                map_line[start_idx + e, l[0]:l[1]] = binary[start_idx + e, l[0]:l[1]]

    map_line = np.zeros(binary.shape[:2], dtype=np.uint8)
    cv2.imshow('binary', binary)

    width = binary.shape[1]
    start_row = -1
    line_area = []
    for i, row in enumerate(binary):
        line_v = check_continuous_line(row, width)
        if line_v is not None:
            # new line
            if start_row == -1:
                start_row = i
                line_area = []
            line_area.append(line_v)
        else:
            # checking line
            if start_row != -1:
                if i - start_row < max_line_thickness:
                    # binary[start_row: i] = 0
                    # map_line[start_row: i] = binary[start_row: i]
                    print(line_area, start_row, i)
                    extract_line_area(line_area, start_row)
                start_row = -1

    height = binary.shape[0]
    start_col = -1
    for i in range(width):
        col = binary[:, i]
        line_h = check_continuous_line(col, height)
        if line_h is not None:
            # new line
            if start_col == -1:
                start_col = i
        else:
            # checking line
            if start_col != -1:
                if i - start_col < max_line_thickness:
                    # binary[:, start_col: i] = 0
                    map_line[:, start_col: i] = binary[:, start_col: i]
                start_col = -1

    binary -= map_line

    if show:
        cv2.imshow('no-line', binary)
        cv2.imshow('lines', map_line)
        cv2.waitKey()


def rm_line(binary,
            max_line_thickness=C.THRESHOLD_LINE_THICKNESS,
            min_line_length_ratio=C.THRESHOLD_LINE_MIN_LENGTH,
            show=False, wait_key=0):
    def is_valid_line(line):
        line_length = 0
        line_gap = 0
        for j in line:
            if j > 0:
                if line_gap > 5:
                    return False
                line_length += 1
                line_gap = 0
            elif line_length > 0:
                line_gap += 1
        if line_length / width > 0.95:
            return True
        return False

    height, width = binary.shape[:2]
    board = np.zeros(binary.shape[:2], dtype=np.uint8)

    start_row, end_row = -1, -1
    check_line = False
    check_gap = False
    for i, row in enumerate(binary):
        # line_ratio = (sum(row) / 255) / width
        # if line_ratio > 0.9:
        if is_valid_line(row):
            # new start: if it is checking a new line, mark this row as start
            if not check_line:
                start_row = i
                check_line = True
        else:
            # end the line
            if check_line:
                # thin enough to be a line, then start checking gap
                if i - start_row < max_line_thickness:
                    end_row = i
                    check_gap = True
                else:
                    start_row, end_row = -1, -1
                check_line = False
        # check gap
        if check_gap and i - end_row > max_line_thickness:
            binary[start_row: end_row] = 0
            start_row, end_row = -1, -1
            check_line = False
            check_gap = False

    if (check_line and (height - start_row) < max_line_thickness) or check_gap:
        binary[start_row: end_row] = 0

    if show:
        cv2.imshow('no-line binary', binary)
        if wait_key is not None:
            cv2.waitKey(wait_key)
        if wait_key == 0:
            cv2.destroyWindow('no-line binary')


def rm_noise_compos(compos):
    compos_new = []
    for compo in compos:
        if compo.category == 'Noise':
            continue
        compos_new.append(compo)
    return compos_new


def rm_noise_in_large_img(compos, org,
                      max_compo_scale=C.THRESHOLD_COMPO_MAX_SCALE):
    row, column = org.shape[:2]
    remain = np.full(len(compos), True)
    new_compos = []
    for compo in compos:
        if compo.category == 'Image':
            for i in compo.contain:
                remain[i] = False
    for i in range(len(remain)):
        if remain[i]:
            new_compos.append(compos[i])
    return new_compos


def detect_compos_in_img(compos, binary, org, max_compo_scale=C.THRESHOLD_COMPO_MAX_SCALE, show=False):
    compos_new = []
    row, column = binary.shape[:2]
    for compo in compos:
        if compo.category == 'Image':
            compo.compo_update_bbox_area()
            # org_clip = compo.compo_clipping(org)
            # bin_clip = pre.binarization(org_clip, show=show)
            bin_clip = compo.compo_clipping(binary)
            bin_clip = pre.reverse_binary(bin_clip, show=show)

            compos_rec, compos_nonrec = component_detection(bin_clip, test=False, step_h=10, step_v=10, rec_detect=True)
            for compo_rec in compos_rec:
                compo_rec.compo_relative_position(compo.bbox.col_min, compo.bbox.row_min)
                if compo_rec.bbox_area / compo.bbox_area < 0.8 and compo_rec.bbox.height > 20 and compo_rec.bbox.width > 20:
                    compos_new.append(compo_rec)
                    # draw.draw_bounding_box(org, [compo_rec], show=True)

            # compos_inner = component_detection(bin_clip, rec_detect=False)
            # for compo_inner in compos_inner:
            #     compo_inner.compo_relative_position(compo.bbox.col_min, compo.bbox.row_min)
            #     draw.draw_bounding_box(org, [compo_inner], show=True)
            #     if compo_inner.bbox_area / compo.bbox_area < 0.8:
            #         compos_new.append(compo_inner)
    compos += compos_new


def compo_filter(compos, min_area, img_shape):
    max_height = img_shape[0] * 0.8
    compos_new = []
    for compo in compos:
        if compo.area < min_area:
            continue
        if compo.height > max_height:
            continue
        ratio_h = compo.width / compo.height
        ratio_w = compo.height / compo.width
        if ratio_h > 50 or ratio_w > 40 or \
                (min(compo.height, compo.width) < 8 and max(ratio_h, ratio_w) > 10):
            continue
        compos_new.append(compo)
    return compos_new


def is_block(clip, thread=0.15):
    '''
    Block is a rectangle border enclosing a group of compos (consider it as a wireframe)
    Check if a compo is block by checking if the inner side of its border is blank
    '''
    side = 4  # scan 4 lines inner forward each border
    # top border - scan top down
    blank_count = 0
    for i in range(1, 5):
        if sum(clip[side + i]) / 255 > thread * clip.shape[1]:
            blank_count += 1
    if blank_count > 2: return False
    # left border - scan left to right
    blank_count = 0
    for i in range(1, 5):
        if sum(clip[:, side + i]) / 255 > thread * clip.shape[0]:
            blank_count += 1
    if blank_count > 2: return False

    side = -4
    # bottom border - scan bottom up
    blank_count = 0
    for i in range(-1, -5, -1):
        if sum(clip[side + i]) / 255 > thread * clip.shape[1]:
            blank_count += 1
    if blank_count > 2: return False
    # right border - scan right to left
    blank_count = 0
    for i in range(-1, -5, -1):
        if sum(clip[:, side + i]) / 255 > thread * clip.shape[0]:
            blank_count += 1
    if blank_count > 2: return False
    return True


def compo_block_recognition(binary, compos, block_side_length=0.15):
    height, width = binary.shape
    for compo in compos:
        if compo.height / height > block_side_length and compo.width / width > block_side_length:
            clip = compo.compo_clipping(binary)
            if is_block(clip):
                compo.category = 'Block'


# take the binary image as input
# calculate the connected regions -> get the bounding boundaries of them -> check if those regions are rectangles
# return all boundaries and boundaries of rectangles
def component_detection(binary, min_obj_area,
                        line_thickness=C.THRESHOLD_LINE_THICKNESS,
                        min_rec_evenness=C.THRESHOLD_REC_MIN_EVENNESS,
                        max_dent_ratio=C.THRESHOLD_REC_MAX_DENT_RATIO,
                        step_h = 5, step_v = 2,
                        rec_detect=False, show=False, test=False):
    """
    :param binary: Binary image from pre-processing
    :param min_obj_area: If not pass then ignore the small object
    :param min_obj_perimeter: If not pass then ignore the small object
    :param line_thickness: If not pass then ignore the slim object
    :param min_rec_evenness: If not pass then this object cannot be rectangular
    :param max_dent_ratio: If not pass then this object cannot be rectangular
    :return: boundary: [top, bottom, left, right]
                        -> up, bottom: list of (column_index, min/max row border)
                        -> left, right: list of (row_index, min/max column border) detect range of each row
    """
    mask = np.zeros((binary.shape[0] + 2, binary.shape[1] + 2), dtype=np.uint8)
    compos_all = []
    compos_rec = []
    compos_nonrec = []
    row, column = binary.shape[0], binary.shape[1]
    for i in range(0, row, step_h):
        for j in range(i % 2, column, step_v):
            if binary[i, j] == 255 and mask[i, j] == 0:
                # get connected area
                # region = util.boundary_bfs_connected_area(binary, i, j, mask)

                mask_copy = mask.copy()
                ff = cv2.floodFill(binary, mask, (j, i), None, 0, 0, cv2.FLOODFILL_MASK_ONLY)
                if ff[0] < min_obj_area: continue
                mask_copy = mask - mask_copy
                region = np.reshape(cv2.findNonZero(mask_copy[1:-1, 1:-1]), (-1, 2))
                region = [(p[1], p[0]) for p in region]

                # filter out some compos
                component = Component(region, binary.shape)
                # calculate the boundary of the connected area
                # ignore small area
                if component.width <= 3 or component.height <= 3:
                    continue
                # check if it is line by checking the length of edges
                # if component.compo_is_line(line_thickness):
                #     continue

                if test:
                    print('Area:%d' % (len(region)))
                    draw.draw_boundary([component], binary.shape, show=True)

                compos_all.append(component)

                if rec_detect:
                    # rectangle check
                    if component.compo_is_rectangle(min_rec_evenness, max_dent_ratio):
                        component.rect_ = True
                        compos_rec.append(component)
                    else:
                        component.rect_ = False
                        compos_nonrec.append(component)

                if show:
                    print('Area:%d' % (len(region)))
                    draw.draw_boundary(compos_all, binary.shape, show=True)

    # draw.draw_boundary(compos_all, binary.shape, show=True)
    if rec_detect:
        return compos_rec, compos_nonrec
    else:
        return compos_all


def nested_components_detection(grey, org, grad_thresh,
                   show=False, write_path=None,
                   step_h=10, step_v=10,
                   line_thickness=C.THRESHOLD_LINE_THICKNESS,
                   min_rec_evenness=C.THRESHOLD_REC_MIN_EVENNESS,
                   max_dent_ratio=C.THRESHOLD_REC_MAX_DENT_RATIO):
    '''
    :param grey: grey-scale of original image
    :return: corners: list of [(top_left, bottom_right)]
                        -> top_left: (column_min, row_min)
                        -> bottom_right: (column_max, row_max)
    '''
    compos = []
    mask = np.zeros((grey.shape[0]+2, grey.shape[1]+2), dtype=np.uint8)
    broad = np.zeros((grey.shape[0], grey.shape[1], 3), dtype=np.uint8)
    broad_all = broad.copy()

    row, column = grey.shape[0], grey.shape[1]
    for x in range(0, row, step_h):
        for y in range(0, column, step_v):
            if mask[x, y] == 0:
                # region = flood_fill_bfs(grey, x, y, mask)

                # flood fill algorithm to get background (layout block)
                mask_copy = mask.copy()
                ff = cv2.floodFill(grey, mask, (y, x), None, grad_thresh, grad_thresh, cv2.FLOODFILL_MASK_ONLY)
                # ignore small regions
                if ff[0] < 500: continue
                mask_copy = mask - mask_copy
                region = np.reshape(cv2.findNonZero(mask_copy[1:-1, 1:-1]), (-1, 2))
                region = [(p[1], p[0]) for p in region]

                compo = Component(region, grey.shape)
                # draw.draw_region(region, broad_all)
                # if block.height < 40 and block.width < 40:
                #     continue
                if compo.height < 30:
                    continue

                # print(block.area / (row * column))
                if compo.area / (row * column) > 0.9:
                    continue
                elif compo.area / (row * column) > 0.7:
                    compo.redundant = True

                # get the boundary of this region
                # ignore lines
                if compo.compo_is_line(line_thickness):
                    continue
                # ignore non-rectangle as blocks must be rectangular
                if not compo.compo_is_rectangle(min_rec_evenness, max_dent_ratio):
                    continue
                # if block.height/row < min_block_height_ratio:
                #     continue
                compos.append(compo)
                # draw.draw_region(region, broad)

    if write_path is not None:
        cv2.imwrite(write_path, broad)
        
    return compos
