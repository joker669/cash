#!/usr/bin/env python
# coding:utf-8

import cv2
import numpy as np
import rospy
from std_msgs.msg import Header
from sensor_msgs.msg import Image
import time

def get_camera():
    camera = cv2.VideoCapture(0) # 定义摄像头
    return camera


def  publisher():
    capture = get_camera()
    rospy.init_node('camera_node', anonymous=True)
    image_pub=rospy.Publisher('/image_view/image_raw', Image, queue_size = 1)

    while not rospy.is_shutdown():
        start = time.time()
        ret, frame = capture.read()
        if ret: # if get frame
            frame = cv2.flip(frame,1)
    
            ros_frame = Image()
            header = Header(stamp = rospy.Time.now())
            header.frame_id = "Camera"
            ros_frame.header=header
            ros_frame.width = 640
            ros_frame.height = 480
            ros_frame.encoding = "bgr8"
            ros_frame.step = 1920
            ros_frame.data = np.array(frame).tostring()
            image_pub.publish(ros_frame)
            end = time.time()  
            print("cost time:", end-start ) # to check if rate suitable
            rate = rospy.Rate(25) # 10hz

    capture.release()
    cv2.destroyAllWindows() 


if __name__=="__main__":
    try:
        publisher()
        print("quit successfully!")
    except rospy.ROSInterruptException as E:
        print("quit unsuccessfully due  to ",E)

