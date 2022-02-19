import rospy
from cash.srv import *

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
      #回调函数 收到的参数.data是通信的数据 默认通过这样的 def callback(data) 取出data.data数据

def acm():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # run simultaneously.
    rospy.init_node('acm', anonymous=True)
      #启动节点并同时为节点命名 

    rospy.Subscriber('target_co', String, callback)
     #启动订阅，订阅主题‘chatter’，及标准字符串格式，同时调用回调函数，当有数据时调用函数，取出数据

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    acm()