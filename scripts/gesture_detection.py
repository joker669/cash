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


def cal_angle(pt1, pt2, pt3):
    # pt1: (x1,y1), pt2: (x2,y2), pt3: (x3,y3)
    # pt2 is the base point of the angle
    a = np.array(pt1)
    b = np.array(pt2)
    c = np.array(pt3)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)


def get_gesture_class(landmarks):
    # determined by the related position of landmarks
    class_no = 0

    thumb_angle = cal_angle(landmarks[0][:2], landmarks[2][:2], landmarks[4][:2])
    index_angle = cal_angle(landmarks[5][:2], landmarks[6][:2], landmarks[8][:2])
    middle_angle = cal_angle(landmarks[9][:2], landmarks[10][:2], landmarks[12][:2])
    ring_angle = cal_angle(landmarks[13][:2], landmarks[14][:2], landmarks[16][:2])
    pinky_angle = cal_angle(landmarks[17][:2], landmarks[18][:2], landmarks[20][:2])
    # print('finger angles: ', thumb_angle, index_angle, middle_angle, ring_angle, pinky_angle)

    angles = [thumb_angle, index_angle, middle_angle, ring_angle, pinky_angle]

    for angle in angles:
        if angle >= 150:
            class_no += 1

    print(class_no)
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
        landmarks = hand["lmList"]
        gesture_class = get_gesture_class(landmarks)

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
    bbox_x1,bbox_x2 = int(640/3), int(640/3*2)
    bbox_y1,bbox_y2 = int(480/3),int(480/3*2)
    print('received: frame ', count)


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
    
    cv_img_cp = cv_img
    cv2.circle(cv_img_cp,(max(fi.target_x,0),max(fi.target_y,0)),2,(0,0,255),-1)
    cv2.rectangle(cv_img_cp,(bbox_x1,bbox_y1),(bbox_x2,bbox_y2),(0,0,255),2)
    cv2.imshow("frame", cv_img_cp)
    cv2.waitKey(1)

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


