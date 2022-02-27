#!/usr/bin/env python
# coding:utf-8
import threading
import rospy
from cash.srv import *
from cash.msg import *
from moveArm import arm

Is_tracking = True
width = 0
length = 0
target_co = [0, 0, 0, 0]
center = [0,0]

def callback(data):
    global width
    global length
    global target_co
    global center
    da = data
    width = da.width
    length = da.length
    target_co = da.co
    center = [int(width/2), int(length/2)]
    #print(center)
    #rospy.loginfo("receive")
      #回调函数 收到的参数.data是通信的数据 默认通过这样的 def callback(data) 取出data.data数据


def tracking_thread():
    a = arm()

    while(Is_tracking):
        center_t = [(target_co[0]+int(target_co[2]/2)), (target_co[1]+int(target_co[3]/2))]
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
            
        if(center_t[1] - center[1] > 50):#############pid for up & down
            di_y = 'D'
            speed_y = 2
        elif(center_t[1] - center[1] < -50):
            di_y = 'U'
            speed_y = 2
        else:
            di_y = 'D'
            speed_y = 0
        ##print(str(center_t[1])+' '+str(center[1]))
        #print(di_y+str(speed_y))
        #a.set_joint('BASE', di_x, speed_x)
        a.set_joint('ELBOW', di_y, speed_y)
        
def start_tracking(req):
    if(req.cmd == 1):
        rospy.loginfo("start tracking %d"%req.cmd)
        Is_tracking = True
    elif(req.cmd == 2):
        rospy.loginfo("stop tracking %d"%req.cmd)
        Is_tracking = False
    return trackingResponse(1)
      #回调函数 收到的参数.data是通信的数据 默认通过这样的 def callback(data) 取出data.data数据

def acm():
    
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # run simultaneously.
    rospy.init_node('acm', anonymous=True)
      #启动节点并同时为节点命名 
    t_tracking = threading.Thread(target=tracking_thread)
    t_tracking.start()
    
    rospy.Subscriber('target_co', target, callback)
    s = rospy.Service("tracking",tracking, start_tracking)#新建一个新的服务,服务类型calRectArea, 回调函数calArea

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    acm()