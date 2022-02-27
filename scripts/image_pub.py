#!D:\Users\yyz\anaconda3\python.exe
import rospy 
import cv2
from cash.msg import target  
from cvzone.HandTrackingModule import HandDetector


WIDTH=640
LENGTH=480


def get_camera():
    camera = cv2.VideoCapture(0) # 定义摄像头
    return camera

def img_pub():
    pub = rospy.Publisher('target_co', target, queue_size=10)
      #Publisher函数创建发布节点（topic名‘target_co’，消息类型target，queue_size发布消息缓冲区大小都是未被接收走的）
    
    rospy.init_node('img_pub', anonymous=True)
      #启动节点img_pub，同时为节点命名，若anoymous为真则节点会自动补充名字，实际名字以talker_322345等表示，
      #若为假，则系统不会补充名字，采用用户命名。如果有重名，则最新启动的节点会注销掉之前的同名节点
    
    rate = rospy.Rate(10) # 10hz
    #延时的时间变量赋值，通过rate.sleep()实现延时
    
    cap = cv2.VideoCapture(0)
    cap.set(3, WIDTH)
    cap.set(4, LENGTH)
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    
    while not rospy.is_shutdown():
        success, img = cap.read()
        hands, img = detector.findHands(img)
        cv2.imshow("Image", img)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            end = 1
            break
        if(hands):
            hand = hands[0]
            [xmin, ymin, w, h] = hand["bbox"]  # 矩形裁剪区域 (ymin:ymin+h, xmin:xmin+w) 的位置参数
               # 判定开始方式，循环发送，以服务程序跳出为终止点 一般ctrl+c也可
            tt = target()
            tt.length = LENGTH
            tt.width = WIDTH
            tt.co = [xmin, ymin, w, h]
              # 数据变量的内容 rospy.get_time() 是指ros系统时间，精确到0.01s 
            
            rospy.loginfo(tt.co)
              #在运行的terminal界面info 出信息，可不加，可随意改
            
            pub.publish(tt)
              #发布数据 必须发布
            
            rate.sleep()
              # 按rospy.Rate()设置的速率延迟 

if __name__ == '__main__':
    try:
        img_pub()
    except rospy.ROSInterruptException:
        pass