#!/usr/bin/env python
# coding:utf-8
import threading

import numpy
import rospy
from cash.srv import *
from cash.msg import *
from moveArm import arm
from time import sleep

import cv2

Is_tracking = False
width = 640
height = 480
depth = -1
center = [int(width/2), int(height/2)]
target_x = center[0]
target_y = center[1]

stop = False
#mode: 1 for gesture mode 2 for face mode
mode = 0

# PID controller gain variables
KP=0.5  #proportiaonal
KD=0.1  #derivative
KI=0.00001 #integral

# Errors for vertical movement
#prev_error_y = 0
#sum_error_y = 0

# Errors for horizontal movement
#prev_error_x = 0
#sum_error_x = 0

def callback_face(data):
    global width
    global height
    global target_x
    global target_y
    global mode
    if(mode == 1):
        return
    da = data
    if(da.target_x != -1 or da.target_y != -1):
        target_x = da.target_x
        target_y = da.target_y
        depth = da.depth
    else:
        target_x = center[0]
        target_y = center[1]

def callback_gesture(data):
    global width
    global height
    global target_x
    global target_y
    global mode
    if(mode == 2):
        return
    da = data
    if(da.target_x != -1 or da.target_y != -1):
        target_x = da.target_x
        target_y = da.target_y
        depth = da.depth
    else:
        target_x = center[0]
        target_y = center[1]
        
    #print(center)
    #rospy.loginfo("receive")
      #回调函数 收到的参数.data是通信的数据 默认通过这样的 def callback(data) 取出data.data数据


def tracking_thread():
    global target_x
    global target_y
    global Is_tracking
    global stop
    prev_error_x = 0
    prev_error_y = 0

    a = arm()

    while(1):
        # cv_img_cp = numpy.zeros((640,480,3))
        # bbox_x1,bbox_x2 = 160,480
        # bbox_y1,bbox_y2 = 120,360
        # cv2.circle(cv_img_cp,(max(target_x,0),max(target_y,0)),2,(0,0,255),-1)
        # cv2.rectangle(cv_img_cp,(bbox_x1,bbox_y1),(bbox_x2,bbox_y2),(0,0,255),2)
        # cv2.imshow("frame", cv_img_cp)
        # cv2.waitKey(1)

        if stop:
            a.close()
            return
        if Is_tracking:
            center_t = [target_x, target_y]
            speed_x = 0
            speed_y = 0
            sum_error_x = 0
            sum_error_y = 0

            print('**********', target_x, target_y)
            di_x = 'R'
            di_y = 'R'
            if(center_t[0] - center[0] > 0):#############pid for Left and right
                error_x = abs(center[0] - center_t[0])
                speed_x =((error_x*KP) +(prev_error_x*KD) +(sum_error_x*KI))//10
                speed_x = max(min(15, speed_x), 1)  # make sure speed don't go past max=10 or below min=2
                di_x = 'R'
                #speed_x = 5
                prev_error_x = error_x
                sum_error_x += error_x
            elif(center_t[0] - center[0] < 0):
                error_x = abs(center[0] - center_t[0])
                speed_x =((error_x*KP) +(prev_error_x*KD) +(sum_error_x*KI))//10
                speed_x = max(min(15, speed_x), 1)  # make sure speed don't go past max=10 or below min=2
                di_x = 'L'
                #speed_x = 5
                prev_error_x = error_x
                sum_error_x += error_x
            else:
                di_x = 'R'
                speed_x = 0
                
            if(center_t[1] - center[1] > 0):#############pid for up & down
                error_y = abs(center[1] - center_t[1])
                speed_y =((error_y*KP) +(prev_error_y*KD) +(sum_error_y*KI))//10
                speed_y = max(min(15, speed_y), 1)  # make sure speed don't go past max=10 or below min=2
                di_y = 'D'
                #speed_y = 5
                prev_error_y = error_y
                sum_error_y += error_y
               
            elif(center_t[1] - center[1] < 0):
                error_y = abs(center[1] - center_t[1])
                speed_y =((error_y*KP) +(prev_error_y*KD) +(sum_error_y*KI))//10
                speed_y = max(min(15, speed_y), 1)  # make sure speed don't go past max=10 or below min=2
                di_y = 'U'
                #speed_y = 5
                prev_error_y = error_y
                sum_error_y += error_y
     
            else:
                di_y = 'D'
                speed_y = 0
            #print(, ' ', str(center[1]))
            #print(di_y+str(speed_y))
            #a.set_joint('BASE', di_x, speed_x)
            a.set_joint('ELBOW', di_y, speed_y)
            a.set_joint('BASE', di_x, speed_x)
            
        else:
            #print(str('****11111**************'))
            a.set_joint('BASE', 'L',0)
            a.set_joint('SHOULDER', 'F',0)
            a.set_joint('ELBOW', 'U', 0)
            a.set_joint('WRISTROTATION', 'WU', 0)
            a.set_joint('WRIST', 'V', 0)
            
        
def start_tracking(req):
    global Is_tracking
    global mode
    if(req.cmd == 2):
        rospy.loginfo("start tracking %d"%req.cmd)
        Is_tracking = True
        mode = 1
    elif(req.cmd == 1):
        rospy.loginfo("stop tracking %d"%req.cmd)
        Is_tracking = False
        mode = 1
    elif(req.cmd == 3):#face start
        Is_tracking = True
        mode = 2
    elif(req.cmd == 4):#face stop
        Is_tracking = False
        mode = 2
        
    return trackingResponse(1)
      #回调函数 收到的参数.data是通信的数据 默认通过这样的 def callback(data) 取出data.data数据

def acm():
    global stop
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # run simultaneously.
    rospy.init_node('acm', anonymous=True)
      #启动节点并同时为节点命名 
    #print('########start###############3')
    t_tracking = threading.Thread(target=tracking_thread)
    t_tracking.start()
    #print("###############################33")
    
    rospy.Subscriber('gesture_info', gesture_info, callback_gesture)
    s = rospy.Service("tracking",tracking, start_tracking)#新建一个新的服务,服务类型calRectArea, 回调函数calArea
    
    rospy.Subscriber('face_info', face_info, callback_face)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
    stop = True

if __name__ == '__main__':
    acm()