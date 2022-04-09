#!/usr/bin/env python
# coding:utf-8

import cv2
import FaceMesh_module as faceMesh
import headPoseEstimation_module as headPose
import time
import os
import pygame
from sensor_msgs.msg import Image
import rospy
import numpy as np
import cv2
from cash.msg import gesture_info
from cv_bridge import CvBridge, CvBridgeError
import os, sys

APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
full_path = os.path.join(APP_FOLDER, "neck_warning.mp3")

s = 0
pygame.mixer.init()
#sound_file = pygame.mixer.Sound('/home/xuxuanbo/cash_ws/src/cash/scripts/warning.mp3')
sound_file = pygame.mixer.Sound(full_path)

def neck_alert_info(color_frame):
    global s
    detector = faceMesh.FaceMeshDetector()
    image = bridge.imgmsg_to_cv2(color_frame, "bgr8")
    message = None
    
    start = time.time()


    #image = cv2.flip(image, 1)
    image, face, keypoint_2d, keypoint_3d, nose_2d, nose_3d = detector.findFaceMesh(image)

    if len(face) != 0:
        nose_bridge_location = face[6]
        print('location of nose bridge is', nose_bridge_location)
        cv2.circle(image, face[6], 5, (255, 0, 0), -1)
        
        x = nose_bridge_location[0]
        y = nose_bridge_location[1]
        pitch, yaw, ih, iw = headPose.headPoseEstimation(image, keypoint_2d, keypoint_3d, nose_2d, nose_3d)  # original
        #pitch, yaw = headPose.headPoseEstimation(image, keypoint_2d, keypoint_3d, nose_2d, nose_3d)

        if yaw < -15 or yaw > 15 or pitch < -15 or pitch > 15:
        #if yaw < -30 or yaw > 30:
            s += 1
            t = str(s//24)
            cv2.putText(image, t, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1)
            if s > 2*24:
                text = "Warning: Bad Neck Posture Detected"
                message = True
                cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.rectangle(image, (5, 5), (iw - 5, ih - 5), (0, 0, 255), 2)
                # os.system("say 'Warning: Bad pose'")
                sound_file.play()
        else:
            sound_file.stop()
            s = 0
            message = False

        cv2.imshow('MediaPipe Face Mesh', image)
        cv2.waitKey(1)

    #cap.release()

def callback(color_frame):
    neck_alert_info(color_frame)
    
   
def  subscriber():
    rospy.init_node('neck_alert_node', anonymous=True)
    rospy.Subscriber('/image_view/image_raw', Image, callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        count = 0
        bridge = CvBridge()
        #face_pub=rospy.Publisher('neck_alert', alert, queue_size = 1) 
        subscriber()
    except rospy.ROSInterruptException as E:
        print("quit unsuccessfully due  to ",E)