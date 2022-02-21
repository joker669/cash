#!/usr/bin/env python
# coding:utf-8

import rospy
from cash.srv import *

def start_tracking(req):
    if(req.cmd == 1):
        rospy.loginfo("start tracking %d"%req.cmd)
    elif(req.cmd == 2):
        rospy.loginfo("stop tracking %d"%req.cmd)
    return trackingResponse(1)
      #回调函数 收到的参数.data是通信的数据 默认通过这样的 def callback(data) 取出data.data数据

def acm():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # run simultaneously.
    rospy.init_node('acm', anonymous=True)
      #启动节点并同时为节点命名 
    
    s = rospy.Service("tracking",tracking, start_tracking)#新建一个新的服务,服务类型calRectArea, 回调函数calArea

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    acm()