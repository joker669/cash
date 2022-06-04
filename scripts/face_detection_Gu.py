#!/usr/bin/env python
# coding:utf-8

import rospy
import numpy as np
from cash.msg import face_info
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
from message_filters import TimeSynchronizer, Subscriber,ApproximateTimeSynchronizer
import FaceMesh_module as faceMesh
import headPoseEstimation_module as headPose

detector = faceMesh.FaceMeshDetector()


def get_coordinates(cv_img):
    '''
    Plz modify this function to call your algorithms to get the coordinates
    :param cv_img:the image frame
    :return: a four-elements integer list which represents the coordinates of the target (face) in the frame
    '''
    
    image, face, keypoint_2d, keypoint_3d, nose_2d, nose_3d = detector.findFaceMesh(cv_img)
    
    if len(face) != 0:
    	nose_bridge_location = face[6]
    	print('location of nose bridge is', nose_bridge_location)
    	cv2.circle(image, face[6], 5, (255, 0, 0), -1)
    	
    	x = nose_bridge_location[0]
    	y = nose_bridge_location[1]
    	pitch, yaw = headPose.headPoseEstimation(image, keypoint_2d, keypoint_3d, nose_2d, nose_3d)
    else:
        x, y, pitch, yaw = -1,-1,-1,-1
    # cv2.imshow('MediaPipe Face Mesh', image)
    # cv2.waitKey(1)

    return x, y, pitch, yaw


def callback(color_frame, depth_frame):
    global bridge, count,face_pub


    # get the frame info
    cv_img = bridge.imgmsg_to_cv2(color_frame,"bgr8")
    cv_img_depth = bridge.imgmsg_to_cv2(depth_frame, "mono16")

    # cv_img = cv2.flip(cv_img, 1) 
    # cv_img_depth = cv2.flip(cv_img_depth, 1)

    count += 1
    print('receieved: frame',count,cv_img.shape )
    # cv2.imshow("frame", cv_img)
    # cv2.waitKey(1)
    
    #Below are just some mock codes. Plz modify the code. 
    # width = cv_img.shape[1]  #the image width ( corresponding to the coordinates)
    # height = cv_img.shape[0]  #the image height ( corresponding to the coordinates)
    
    x, y, pitch, yaw = get_coordinates(cv_img)
    
    fi = face_info()
    fi.target_x = min(x,639)
    fi.target_y = min(y,479)
    fi.depth = cv_img_depth[fi.target_y][fi.target_x]
    fi.angle_yaw = yaw
    fi.angle_pitch = pitch

    rospy.loginfo(fi)
    face_pub.publish(fi)


def  subscriber():
    rospy.init_node('face_detection_node', anonymous=True)
    # rospy.Subscriber('/image_view/image_raw', Image, callback)
    tss = ApproximateTimeSynchronizer([Subscriber("/image_view/image_raw", Image),
                Subscriber("/image_view/depth_image_raw", Image)],queue_size=5, slop=0.1)
    tss.registerCallback(callback)
    rospy.spin()
    
    
if __name__ == '__main__':
    try:
        count = 0
        bridge = CvBridge()
        face_pub=rospy.Publisher('face_info', face_info, queue_size = 1) 
        subscriber()
    except rospy.ROSInterruptException as E:
        print("quit unsuccessfully due  to ",E)

