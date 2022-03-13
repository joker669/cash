#!/usr/bin/env python
# coding:utf-8

import rospy
import cv2
import time
import numpy as np  
from cash.msg import face_info,gesture_info
from cash.srv import tracking

acm_mode = 'start' # ['start','stop']
system_mode = 'face' # ['face','gesture','frozen']

def boundary_checking(data):
    frame_height = 480
    frame_width = 640
    bbox_x1,bbox_x2 = frame_width/3,frame_width/3*2
    bbox_y1,bbox_y2 = frame_height/3,frame_height/3*2
    bbox_z1,bbox_z2 = 10,1000
    target_x = data.target_x
    target_y = data.target_y
    depth = data.depth

    if target_x<=bbox_x1 or target_x>=bbox_x2 or target_y<=bbox_y1 or target_y>=bbox_y2:
        return False
    else:
        return True


def face_callback(data):
    global system_mode, acm_mode
    if system_mode == 'face':
        rospy.loginfo(data)
        inside = boundary_checking(data)
        
        if not inside and acm_mode == 'stop':
        
            tracking_client(3)
            acm_mode = 'start'
            rospy.loginfo("call  acm")
            
        elif inside and acm_mode == 'start':
        
            tracking_client(4)
            acm_mode = 'stop'
            rospy.loginfo("stop  acm")
            
    rospy.loginfo("current acm_mode: {},  current system_mode: {}".format(acm_mode, system_mode))


def gesture_callback(data):
    global system_mode, acm_mode
    
    if data.gesture == 3:        
        system_mode = 'face'
    elif data.gesture == 2:        
        system_mode = 'gesture'
    elif data.gesture == 0:        
        system_mode = 'frozen'
        acm_mode = 'stop'
        tracking_client(1)
    
    if system_mode == 'gesture':
        rospy.loginfo(data)
        inside = boundary_checking(data)
        
        if not inside and acm_mode == 'stop':
        
            tracking_client(2)
            acm_mode = 'start'
            rospy.loginfo("call  acm")
            
        elif inside and acm_mode == 'start':
        
            tracking_client(1)
            acm_mode = 'stop'
            rospy.loginfo("stop  acm")
                    
    rospy.loginfo("current acm_mode: {},  current system_mode: {}".format(acm_mode, system_mode))


def tracking_client(cmd):
    # 等待接入服务节点
    # 第二句是调用wait_for_service，阻塞直到名为“tracking”的服务可用。
    rospy.wait_for_service('tracking')
    try: 
        # 创建服务的处理句柄,可以像调用函数一样，调用句柄
        tracking_s = rospy.ServiceProxy('tracking', tracking)
        resp1 = tracking_s(cmd)
        print("Service call success: %s"%resp1.rsp)
        return resp1.rsp #如果调用失败，可能会抛出rospy.ServiceException
    except rospy.ServiceException as e:     
        print("Service call failed: %s"%e)


def pcm():
    global width
    global length
    global target_co

    rospy.init_node('pcm_node', anonymous=True)#启动节点并同时为节点命名 
    rospy.Subscriber('face_info', face_info, face_callback) #启动订阅，订阅主题‘face_detection_node’，同时调用回调函数，回调函数会根据情况确定是否调用acm服务
    rospy.Subscriber('gesture_info', gesture_info, gesture_callback) #启动订阅，订阅主题‘face_detection_node’，同时调用回调函数，回调函数会根据情况确定是否调用acm服务
    rospy.spin()


if __name__ == '__main__':
    pcm()
