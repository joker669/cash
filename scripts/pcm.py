import rospy
import cv2
import time
import numpy as np  
from cash.msg import *
from cash.srv import *

width = 0
length = 0
target_co = [0, 0, 0, 0]

def face_callback(data):
    global width
    global length
    global target_co
    da = data
    width = da.width
    length = da.length
    target_co = da.co
    rospy.loginfo("receive")
      #回调函数 收到的参数.data是通信的数据 默认通过这样的 def callback(data) 取出data.data数据
      

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
    rospy.Subscriber('target_co', target, callback)#启动订阅，订阅主题‘target_co’，及标准字符串格式，同时调用回调函数，当有数据时调用函数，取出数据
    
    old_width = 0
    old_length = 0
    old_tc = [0,0,0,0]
    img = None
    rc = False
    s_tracking = False
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
        #########################计算距离，距离过大开始跟踪
        distance = abs(target_co[0]+(target_co[2]/2) - (width/2)) + abs(target_co[2]+(target_co[3]/2)-(length/2))
        if(distance > 200 and s_tracking == False):
            tracking_client(1)
            s_tracking = True
        elif(distance < 150 and s_tracking == True):
            tracking_client(2)
            s_tracking = False
        if(rc == True):
            cv2.imshow("img",img)
            cv2.waitKey(1)
    # spin() simply keeps python from exiting until this node is stopped

if __name__ == '__main__':
    pcm()
