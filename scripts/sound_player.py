#!/usr/bin/env python
# coding:utf-8

import numpy
import rospy
from cash.srv import *
from cash.msg import *
from time import sleep
import os
import pygame
import threading

APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
full_path = os.path.join(APP_FOLDER, "neck_warning.mp3")
pygame.mixer.init()
# sound_file = pygame.mixer.Sound('/home/xuxuanbo/cash_ws/src/cash/scripts/warning.mp3')
# sound_file = pygame.mixer.Sound(full_path)

alert = False
is_play = False
stop = False

def play_sound_thread():
    global is_play, sound_file, alert, full_path, stop
    pygame.mixer.music.load(full_path)
    while True:
        if stop:
            return
        if alert:
                if pygame.mixer.music.get_busy()==False:
                    pygame.mixer.music.play()
        else:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(full_path)

def sound_play_stop(req):
    global alert
    # try:
    if(req.cmd == 1):
        rospy.loginfo("start alerting %d"%req.cmd)
        alert = True
    elif(req.cmd == 2):
        rospy.loginfo("stop alerting %d"%req.cmd)
        alert = False
    return soundResponse(1)
    # except:
        # return soundResponse(2)
      #回调函数 收到的参数.data是通信的数据 默认通过这样的 def callback(data) 取出data.data数据


def sound_player():
    rospy.init_node('sound_player', anonymous=True)
    #启动节点并同时为节点命名     
    s_tracking = threading.Thread(target=play_sound_thread)
    s_tracking.start()
    s = rospy.Service("sound",sound, sound_play_stop)#新建一个新的服务,服务类型calRectArea, 回调函数calArea
    rospy.spin()
    stop = True


if __name__ == '__main__':s
    sound_player()