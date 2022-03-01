#!/usr/bin/env python
# coding:utf-8

import rospy
import numpy as np
import cv2
from cash.msg import gesture_info
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.8, maxHands=1)


def get_gesture_class(finger_status):
    # determined by the number of fingers are up
    class_no = 0

    for finger in finger_status:
        if finger == 1:
            class_no += 1

    return class_no


def process_hand(cv_img):
    bbox = None
    gesture_class = None
    hands = detector.findHands(cv_img, draw=False)

    if not hands:
        print('WARNING: no hand detected!')
        return bbox, gesture_class  # return None, None

    for hand in hands:
        if hand1["type"] != 'Right':  # control only with right hand
            continue

        # get bbox
        bbox = list(hand["bbox"])
        # get gesture class
        finger_status = detector.fingersUp(hand)
        gesture_class = get_gesture_class(finger_status)

    if not bbox:
        print('WARNING: please use right hand for controlling!')  # return None, None

    return bbox, gesture_class


def callback(data):
    global bridge, count, face_pub

    # get the frame info
    cv_img = bridge.imgmsg_to_cv2(data, "bgr8")
    count += 1
    print('received: frame ', count)
    # cv2.imshow("frame", cv_img)
    # cv2.waitKey(1)

    height, width, _ = frame.shape
    bbox, gesture = process_hand(cv_img)

    fi = gesture_info()
    fi.height = height
    fi.width = width
    fi.co = bbox
    fi.gesture = gesture

    rospy.loginfo(fi)
    face_pub.publish(fi)


def subscriber():
    rospy.init_node('gesture_detection_node', anonymous=True)
    rospy.Subscriber('/image_view/image_raw', Image, callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        count = 0
        bridge = CvBridge()
        face_pub = rospy.Publisher('gesture_info', gesture_info, queue_size=1)
        subscriber()
    except rospy.ROSInterruptException as E:
        print("quit unsuccessfully due  to ", E)


