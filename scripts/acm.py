#!/usr/bin/env python
# coding:utf-8
import threading
import rospy
from cash.srv import *
from cash.msg import *
from moveArm import arm
from time import sleep

Is_tracking = True
width = 640
height = 480
depth = -1
center = [int(width/2), int(height/2)]
target_x = center[0]
target_y = center[1]

# PID controller gain variables
SAMPLETIME=0.5
KP=0.02  #proportiaonal
KD=0.01  #derivative
KI=0.005 #integral

# for vertical movement
prev_error_y = 0
sum_error_y = 0


def callback(data):
    global width
    global height
    global target_x
    global target_y
    da = data
    target_x = da.target_x
    target_y = da.target_y
    depth = da.depth
    #print(center)
    #rospy.loginfo("receive")
      #回调函数 收到的参数.data是通信的数据 默认通过这样的 def callback(data) 取出data.data数据


def tracking_thread():
    global target_x
    global target_y
    global Is_tracking
    prev_error_y = 0
    a = arm()

    while(1):
        if Is_tracking:
            center_t = [target_x, target_y]
            sum_error_y = 0
            print('**********', target_x, target_y)
            di_x = 0
            di_y = 0
            if(center_t[0] > center[0]):#############pid for Left and right
                di_x = 'R'
                speed_x = 2
            elif(center_t[0] < center[0]):
                di_x = 'L'
                speed_x = 2
            else:
                di_x = 'R'
                speed_x = 0
                
            if(center_t[1] - center[1] > 0):#############pid for up & down
                speed_y = 0
                error_y = abs(center[1] - center_t[1])
                speed_y +=(error_y*KP) +(prev_error_y*KD) +(sum_error_y*KI)
                speed_y = 10 - speed_y # take the inverse to increase speed as error become less
                speed_y = max(min(10, speed_y), 2)  # make sure speed don't go past max=10 or below min=1
                di_y = 'D'
                #speed_y = 2
                sleep(SAMPLETIME)
                prev_error_y = error_y
                sum_error_y += error_y
               
            elif(center_t[1] - center[1] < 0):
                speed_y = 0
                error_y = abs(center[1] - center_t[1])
                speed_y +=(error_y*KP) +(prev_error_y*KD) +(sum_error_y*KI)
                speed_y = 10 - speed_y # take the inverse to increase speed as error become less
                speed_y = max(min(10, speed_y), 2)  # make sure speed don't go past max=10 or below min=1
                di_y = 'U'
                #speed_y = 2
                sleep(SAMPLETIME)
                prev_error_y = error_y
                sum_error_y += error_y
     
            else:
                di_y = 'D'
                speed_y = 0
            #print(, ' ', str(center[1]))
            #print(di_y+str(speed_y))
            #a.set_joint('BASE', di_x, speed_x)
            a.set_joint('ELBOW', di_y, speed_y)
            
        else:
            print(str('****11111**************'))
            a.set_joint('BASE', 'L',0)
            a.set_joint('SHOULDER', 'F',0)
            a.set_joint('ELBOW', 'U', 0)
            a.set_joint('WRISTROTATION', 'WU', 0)
            #a.set_joint('WRIST', 'V', 0)
            
        
def start_tracking(req):
    global Is_tracking
    if(req.cmd == 2):
        rospy.loginfo("start tracking %d"%req.cmd)
        Is_tracking = True
    elif(req.cmd == 1):
        rospy.loginfo("stop tracking %d"%req.cmd)
        Is_tracking = True
    return trackingResponse(1)
      #回调函数 收到的参数.data是通信的数据 默认通过这样的 def callback(data) 取出data.data数据

def acm():
    
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # run simultaneously.
    rospy.init_node('acm', anonymous=True)
      #启动节点并同时为节点命名 
    print('########start###############3')
    t_tracking = threading.Thread(target=tracking_thread)
    t_tracking.start()
    print("###############################33")
    
    rospy.Subscriber('gesture_info', gesture_info, callback)
    s = rospy.Service("tracking",tracking, start_tracking)#新建一个新的服务,服务类型calRectArea, 回调函数calArea

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    acm()