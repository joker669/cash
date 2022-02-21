#!/usr/bin/env python
# coding:utf-8

import rospy
import numpy as np
from cash.msg import gesture_info
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

def get_coordinates(cv_img):
    '''
    Plz modify this function to call your algorithms to get the coordinates
    :param cv_img:the image frame
    :return: a four-elements integer list which represents the coordinates of the target (gesture) in the frame
    '''
    x_upleft = 20
    y_upleft = 40
    rectangle_height = 30
    rectangle_width = 30
    return [x_upleft, y_upleft, rectangle_height, rectangle_width]


def callback(data):
    global bridge, count,face_pub
    
    # get the frame info
    cv_img = bridge.imgmsg_to_cv2(data, "bgr8")
    count += 1
    print('receieved: frame',count )
    #cv2.imshow("frame", cv_img)
    #cv2.waitKey(1)
    
    #Below are just some mock codes. Plz modify the code. 
    width = 640  #the image width ( corresponding to the coordinates)
    height = 480  #the image height ( corresponding to the coordinates)
    gesture = 1 #call your algorithms to get which kind of gesture
    co = get_coordinates(cv_img)
    
    fi = gesture_info()
    fi.width = width
    fi.height = height
    fi.gesture = gesture
    fi.co = co
    
    rospy.loginfo(fi)
    face_pub.publish(fi)


def  subscriber():
    rospy.init_node('gesture_dection_node', anonymous=True)
    rospy.Subscriber('/image_view/image_raw', Image, callback)
    rospy.spin()
    
    
if __name__ == '__main__':
    try:
        count = 0
        bridge = CvBridge()
        face_pub=rospy.Publisher('gesture_info', gesture_info, queue_size = 1) 
        subscriber()
    except rospy.ROSInterruptException as E:
        print("quit unsuccessfully due  to ",E)


