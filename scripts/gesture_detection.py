#!/usr/bin/env python
# coding:utf-8

import rospy
import numpy as np
import cv2
from cash.msg import gesture_info
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from cvzone.HandTrackingModule import HandDetector
from message_filters import TimeSynchronizer, Subscriber,ApproximateTimeSynchronizer

detector = HandDetector(detectionCon=0.8, maxHands=1)


def get_gesture_class(finger_status):
    # determined by the number of fingers are up
    class_no = 0
    print(finger_status)
    for finger in finger_status:
        if finger == 1:
            class_no += 1

    return class_no


def process_hand(cv_img):
    center = None
    gesture_class = None
    hands = detector.findHands(cv_img, draw=False)

    if not hands:
        print('WARNING: no hand detected!')
        return center, gesture_class  # return None, None

    for hand in hands:
        if hand["type"] != 'Right':  # control only with right hand
            continue

        # get center of hand
        center = list(hand["center"])
        # get gesture class
        finger_status = detector.fingersUp(hand)
        gesture_class = get_gesture_class(finger_status)

    if not center:
        print('WARNING: please use right hand for controlling!')  # return None, None

    return center, gesture_class


def callback(color_frame, depth_frame):
    global bridge, count, gesture_pub

    # get the frame info
    cv_img = bridge.imgmsg_to_cv2(color_frame, "bgr8")
    cv_img_depth = bridge.imgmsg_to_cv2(depth_frame, "mono16")
    print(cv_img_depth.shape)
    count += 1
    print('received: frame ', count)
    # cv2.imshow("frame", cv_img)
    # cv2.waitKey(1)

    #height, width, _ = frame.shape
    center, gesture = process_hand(cv_img)
    rospy.loginfo(center)
    fi = gesture_info()    
    if center:
        fi.target_x = min(center[0],639)
        fi.target_y = min(center[1],479)
        fi.depth = cv_img_depth[fi.target_y][fi.target_x]
        fi.gesture = gesture
        
    else:
        fi.target_x = -1
        fi.target_y = -1
        fi.depth = -1
        fi.gesture = -1

    rospy.loginfo(fi)
    print(fi)
    gesture_pub.publish(fi)


def subscriber():
    rospy.init_node('gesture_detection_node', anonymous=True)
    # rospy.Subscriber('/image_view/image_raw', Image, callback)
    tss = ApproximateTimeSynchronizer([Subscriber("/image_view/image_raw", Image),
                Subscriber("/image_view/depth_image_raw", Image)],queue_size=5, slop=0.1)
    tss.registerCallback(callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        count = 0
        bridge = CvBridge()
        gesture_pub = rospy.Publisher('gesture_info', gesture_info, queue_size=1)
        subscriber()
    except rospy.ROSInterruptException as E:
        print("quit unsuccessfully due  to ", E)


