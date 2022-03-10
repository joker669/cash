#!/usr/bin/env python
# coding:utf-8

import cv2
import time
import rospy
import numpy as np
import pyrealsense2 as rs
from std_msgs.msg import Header
from sensor_msgs.msg import Image


# config realsense camera
def get_camera():
	pipeline = rs.pipeline()
	config = rs.config()
	config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
	config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
	# Start streaming
	pipeline.start(config)

	return pipeline


def publisher():
	pipeline = get_camera()
	rospy.init_node('camera_node', anonymous=True)
	image_pub = rospy.Publisher('/image_view/image_raw', Image, queue_size=1)
    
	depth_image_pub = rospy.Publisher('/image_view/depth_image_raw', Image, queue_size=1)

	while not rospy.is_shutdown():
		start = time.time()
		frames = pipeline.wait_for_frames()
		depth_frame = frames.get_depth_frame()
		color_frame = frames.get_color_frame()

		if depth_frame and color_frame:  # if get frame
			depth_frame = np.asanyarray(depth_frame.get_data())
			depth_frame = np.expand_dims( cv2.flip(depth_frame, 1) , axis = 2)
			#depth_frame = np.full(depth_frame.shape, 33)
			print(depth_frame.shape)

			# only RGB channels are included in the msg now
			color_frame = np.asanyarray(color_frame.get_data())
			color_frame = cv2.flip(color_frame, 1)

			# color_depth_frame = np.concatenate((color_frame, depth_frame), axis = 2)
			# print(color_depth_frame[:5,:5,0], color_depth_frame[:5,:5,1], color_depth_frame[:5,:5,2], color_depth_frame[:5,:5,3])
            
			#print(color_depth_frame.shape)
			stamp=rospy.Time.now()

			ros_frame = Image()
			header = Header(stamp=stamp)
			header.frame_id = "Camera"
			ros_frame.header = header
			ros_frame.width = 640
			ros_frame.height = 480
			ros_frame.encoding = "bgr8"
			#ros_frame.encoding = "bgra8"
			ros_frame.step = 1920
			ros_frame.data = np.array(color_frame).tostring()
            
			ros_depth_frame = Image()
			header = Header(stamp=stamp)
			header.frame_id = "Depth_Camera"
			ros_depth_frame.header = header
			ros_depth_frame.width = 640
			ros_depth_frame.height = 480
			ros_depth_frame.encoding = "z16"
			#ros_depth_frame.step = 1920
			ros_depth_frame.data = np.array(depth_frame).tostring()

			image_pub.publish(ros_frame)
			depth_image_pub.publish(ros_depth_frame)
            
            
			end = time.time()
			print("cost time:", end - start)  # to check if rate suitable
			rate = rospy.Rate(25)  # 10hz

	cv2.destroyAllWindows()


if __name__ == "__main__":
	try:
		publisher()
		print("quit successfully!")
	except rospy.ROSInterruptException as E:
		print("quit unsuccessfully due  to ", E)

