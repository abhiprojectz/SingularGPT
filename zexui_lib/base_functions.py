import numpy as np 
import cv2 

def find_obj_to_left_of_target_obj(target_obj, objects):
  # Convert the given list of coordinates into NumPy array format
  coordinates = np.array(objects)

  # Find the index of the target point in the NumPy array of coordinates
  target_index = np.where((coordinates == target_obj).all(axis=1))[0][0]

  # Find the coordinates of the point that is just left side of the target point
  left_side_coords = coordinates[target_index - 1]

  # Iterate through the NumPy array of coordinates and draw a circle for each point with green color except for the point that is just left side of the target point
  # for coord in coordinates:
  #     if (coord == left_side_coords).all():
  #         cv2.circle(img, tuple(coord), 10, (0, 0, 255), -1)
  #     else:
  #         cv2.circle(img, tuple(coord), 10, (0, 255, 0), -1)

  # Print the coordinates of the point that is just left side of the target point
  print(f"Coordinates of the point just left side of the target point: {left_side_coords}")
  return left_side_coords


def find_obj_to_right_of_target_obj(target_obj, objects):
  # Convert the given list of coordinates into NumPy array format
  coordinates = np.array(objects)

  # Find the index of the target point in the NumPy array of coordinates
  target_index = np.where((coordinates == target_obj).all(axis=1))[0][0]

  # Find the coordinates of the point that is just right side of the target point
  right_side_coords = coordinates[target_index + 1]

  # Iterate through the NumPy array of coordinates and draw a circle for each point with green color except for the point that is just left side of the target point
  # for coord in coordinates:
  #     if (coord == left_side_coords).all():
  #         cv2.circle(img, tuple(coord), 10, (0, 0, 255), -1)
  #     else:
  #         cv2.circle(img, tuple(coord), 10, (0, 255, 0), -1)

  # Print the coordinates of the point that is just left side of the target point
  print(f"Coordinates of the point just left side of the target point: {right_side_coords}")
  return right_side_coords


def find_obj_to_bottom_of_target_obj(target_obj, objects):
  # Convert the given list of coordinates into NumPy array format
  coordinates = np.array(objects)

  # Find the index of the target point in the NumPy array of coordinates
  target_index = np.where((coordinates == target_obj).all(axis=1))[0][0]

  # Find the coordinates of the point that is just bottom side of the target point
  bottom_side_coords = coordinates[np.where(coordinates[:, 0] == coordinates[target_index][0])[0][np.where(coordinates[:, 0] == coordinates[target_index][0])[0] > target_index][0]]


  # Iterate through the NumPy array of coordinates and draw a circle for each point with green color except for the point that is just left side of the target point
  # for coord in coordinates:
  #     if (coord == left_side_coords).all():
  #         cv2.circle(img, tuple(coord), 10, (0, 0, 255), -1)
  #     else:
  #         cv2.circle(img, tuple(coord), 10, (0, 255, 0), -1)

  # Print the coordinates of the point that is just left side of the target point
  print(f"Coordinates of the point just left side of the target point: {bottom_side_coords}")
  return bottom_side_coords


def find_obj_to_top_of_target_obj(target_obj, objects):
  # Convert the given list of coordinates into NumPy array format
  coordinates = np.array(objects)

  # Find the index of the target point in the NumPy array of coordinates
  target_index = np.where((coordinates == target_obj).all(axis=1))[0][0]

  # Find the coordinates of the point that is just top side of the target point
  top_side_coords = coordinates[np.where(coordinates[:, 0] == coordinates[target_index][0])[0][np.where(coordinates[:, 0] == coordinates[target_index][0])[0] < target_index][-1]]

  # Iterate through the NumPy array of coordinates and draw a circle for each point with green color except for the point that is just left side of the target point
  # for coord in coordinates:
  #     if (coord == left_side_coords).all():
  #         cv2.circle(img, tuple(coord), 10, (0, 0, 255), -1)
  #     else:
  #         cv2.circle(img, tuple(coord), 10, (0, 255, 0), -1)

  # Print the coordinates of the point that is just left side of the target point
  print(f"Coordinates of the point just left side of the target point: {top_side_coords}")
  return top_side_coords


def find_location_of_img_obj(original_path, target_path):
  # Load the original image and convert it to grayscale
  original_image = cv2.imread(original_path)
  original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

  # Load the cropped image and convert it to grayscale
  cropped_image = cv2.imread(target_path)
  cropped_gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

  # Find the coordinates of the cropped image within the original image
  result = cv2.matchTemplate(original_gray, cropped_gray, cv2.TM_CCOEFF_NORMED)
  (_, _, minLoc, maxLoc) = cv2.minMaxLoc(result)
  (left, top) = maxLoc
  right = left + cropped_gray.shape[1]
  bottom = top + cropped_gray.shape[0]

  print(f"Coordinates of cropped image with respect to original image: ({left}, {top}, {right}, {bottom})")
  return [left, top, right, bottom]