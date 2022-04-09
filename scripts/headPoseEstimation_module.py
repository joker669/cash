#!/usr/bin/env python
# coding:utf-8

import math
import cv2
import numpy as np


def headPoseEstimation(image, keypoint_2d, keypoint_3d, nose_2d, nose_3d):
    # Convert it to the NumPy array
    keypoint_2d = np.array(keypoint_2d, dtype=np.float64)
    # Convert it to the NumPy array
    keypoint_3d = np.array(keypoint_3d, dtype=np.float64)

    ih, iw, ic = image.shape
    # The camera matrix
    focal_length = 1 * iw
    cam_matrix = np.array([[focal_length, 0, iw / 2],
                           [0, focal_length, ih / 2],
                           [0, 0, 1]])
    # print("Camera Matrix :\n {0}".format(cam_matrix))

    # The distortion parameters
    dist_matrix = np.zeros((4, 1), dtype=np.float64)

    # Solve PnP
    success, rot_vec, trans_vec = cv2.solvePnP(keypoint_3d, keypoint_2d, cam_matrix, dist_matrix)
    # print("Rotation Vector:\n {0}".format(rot_vec))
    # print("Translation Vector:\n {0}".format(trans_vec))

    # Get rotational matrix
    rmat, jac = cv2.Rodrigues(rot_vec)

    # In[ ]:
    # # Get angles
    angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

    # Get the rotation degree
    pitch = int(angles[0] * 360)
    yaw = int(angles[1] * 360)
    # roll = angles[2] * 360
    # rot_params = [pitch, yaw, roll]

    # See where the user's head tilting
    # if yaw < -10:
    #     text = "Looking Left"
    # elif yaw > 10:
    #     text = "Looking Right"
    # elif pitch < -10:
    #     text = "Looking Down"
    # elif pitch > 10:
    #     text = "Looking Up"
    # else:
    #     text = "Forward"

    # In[ ]:
    # Display the nose direction
    nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix,
                                                     cv2.cv2.SOLVEPNP_ITERATIVE)
    p1 = (int(nose_2d[0]), int(nose_2d[1]))
    p2 = (int(nose_3d_projection[0][0][0]), int(nose_3d_projection[0][0][1]))
    cv2.line(image, p1, p2, (0, 255, 0), 3)  # Green

    # Add the text on the image
    # cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
    # cv2.putText(image, "roll: " + str(np.round(roll, 1)), (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
    cv2.putText(image, "pitch: " + str(np.round(pitch, 1)), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
    cv2.putText(image, "yaw: " + str(np.round(yaw, 1)), (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

    return pitch, yaw, ih, iw