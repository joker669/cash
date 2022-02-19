import rospy
import cv2
import time
import numpy as np  
from cash.msg import target
from cash.msg import control

width = 0
length = 0
target_co = [0, 0, 0, 0]

def callback(data):
    global width
    global length
    global target_co
    da = data
    width = da.width
    length = da.length
    target_co = da.co
    rospy.loginfo("receive")
      #回调函数 收到的参数.data是通信的数据 默认通过这样的 def callback(data) 取出data.data数据

def pcm():
    global width
    global length
    global target_co
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # run simultaneously.
    rospy.init_node('pcm', anonymous=True)
      #启动节点并同时为节点命名 

    rospy.Subscriber('target_co', target, callback)
     #启动订阅，订阅主题‘target_co’，及标准字符串格式，同时调用回调函数，当有数据时调用函数，取出数据
    old_width = 0
    old_length = 0
    old_tc = [0,0,0,0]
    img = None
    rc = False
    while 1:
        time.sleep(0.01)
        ####################判断是否新发布的消息是否有更新，有更新才重新画图
        if(width > 0 and length > 0):
            if(old_width != width or old_length != length):
                img = np.zeros((length,width,3), np.uint8)
                img.fill(255)
                rc = True
                old_width = width
                old_length = length
        if( (old_tc!=target_co) and (rc == True)):
            img.fill(255)
            cv2.rectangle(img,(target_co[0],target_co[1]),(target_co[0]+target_co[2],target_co[1]+target_co[3]),(0,0,255),2)
            old_tc = target_co
        #########################
        if(rc == True):
            cv2.imshow("img",img)
            cv2.waitKey(1)
    # spin() simply keeps python from exiting until this node is stopped

if __name__ == '__main__':
    pcm()