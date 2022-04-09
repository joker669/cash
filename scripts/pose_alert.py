#!/usr/bin/env python
# coding:utf-8

import cv2
import FaceMesh_module as faceMesh
import headPoseEstimation_module as headPose
import time
import os, sys
#from playsound import playsound
import pygame

s = 0
APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
full_path = os.path.join(APP_FOLDER, "neck_warning.mp3")
pygame.mixer.init()
sound_file = pygame.mixer.Sound(full_path)

if __name__ == "__main__":
    detector = faceMesh.FaceMeshDetector()
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, image = cap.read()
        start = time.time()

        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        image = cv2.flip(image, 1)
        image, face, keypoint_2d, keypoint_3d, nose_2d, nose_3d = detector.findFaceMesh(image)

        if len(face) != 0:
            nose_bridge_location = face[6]
            print('location of nose bridge is', nose_bridge_location)
            cv2.circle(image, face[6], 5, (255, 0, 0), -1)
            
            x = nose_bridge_location[0]
            y = nose_bridge_location[1]
            pitch, yaw, ih, iw = headPose.headPoseEstimation(image, keypoint_2d, keypoint_3d, nose_2d, nose_3d)

            if yaw < -30 or yaw > 30 or pitch < -30 or pitch > 30:
                s += 1
                t = str(s//24)
                cv2.putText(image, t, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1)
                if s > 2*24:
                    text = "Warning: Bad Neck Posture Detected"
                    cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    #cv2.rectangle(image, (5, 5), (iw - 5, ih - 5), (0, 0, 255), 2)
                    # os.system("say 'Warning: Bad pose'")
                    #playsound('warning.mp3',True)
                    sound_file.play()
            else:
                s = 0

        cv2.imshow('MediaPipe Face Mesh', image)
        cv2.waitKey(1)

    cap.release()


# # Head Yaw
# # Ratio of Distance: Left Eye[33] to Nose Bridge vs Nose Bridge[6] to Right Eye[263]
# # Turn left or turn right
# cv2.line(image, face[263], face[6], (0, 0, 255), 2)
# cv2.line(image, face[33], face[6], (0, 0, 255), 2)
#
# # Head Roll
# # Arctan of Difference: Cheek to Cheek Height vs Width change. Left cheek[234],Right cheek[454]
# # Tilt Left or Tilt Right
# cv2.line(image, face[234], face[454], (0, 255, 0), 2)
#
# # Head Pitch
# # Ratio of Difference: Upper[67][297] and Lower[54][284] Forehead line distance change
# # vS Upper[172][397] and Lower[150][379] Chin change
# cv2.line(image, face[67], face[297], (255, 0, 0), 2)
# cv2.line(image, face[54], face[284], (255, 0, 0), 2)
# cv2.line(image, face[172], face[397], (255, 0, 0), 2)
# cv2.line(image, face[150], face[379], (255, 0, 0), 2)
