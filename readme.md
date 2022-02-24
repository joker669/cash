#package_guide

**1. First, create your own workspace (remember to create a python3 version one). Plz refer to http://wiki.ros.org/cn/catkin/Tutorials/create_a_workspace.**


**2. git clone our github repository to src sub-folder of your workspace**

cmd:
```
cd $your_work_space/src
git clone https://github.com/joker669/cash.git
```


**3. compile it.**

cmd:
```
catkin_make
. ~/$your_work_space/devel/setup.bash
```
to check if successful or not: (may need to run rosdep update first)
rospack depends1 cash (as long as it outputs some packages then it's fine)

**4. If find that unable to use cv_bridge with ROS Kinetic and Python3, plz refer to this link:https://stackoverflow.com/questions/49221565/unable-to-use-cv-bridge-with-ros-kinetic-and-python3?rq=1 (Kindly remember to modify those ros version or python version.)**

**5. Can use roslaunch to start all the nodes (plz refer to 6 for details). But it is recommended to only rosrun your node when debugging which would be much more covenient and efficient.**
cmd:
```
roslaunch cash cash_all.launch
```

**6.Project Structure**

Currently we use "acm.py", "camera_pub.py", "face_detection.py", "gesture_detection.py", "pcm_new.py" these five files to implement our full functionality, which means that we don't need "image_pub.py" and "pcm.py" for now but you still can refer to it. All the codes for message communication have been written so you may only need to add on codes to form the message. (Now the messages in the code are filled with fake data). 

Feel free to modify everything but in case you want to modify the topic, service or message, plz kindly discuss with the team so that other can do the corresponding modification.

There are two messages in total to enable nodes communication.

*gesture_info*:

`int32 height` :the height of the frame node received. (The coordinates are relative so it's important for acm to have this information)

`int32 width` :the width of the frame node received. (The coordinates are relative so it's important for acm to have this information)

`int32 gesture`: which kind of gesture. Later we could discuss how many kinds of gestures and what they represent

`int32[] co`: [x_upleft, y_upleft, rectangle_height, rectangle_width], a four-elements integer list which represents the coordinates of the target (hand) in the frame

*face_info*:

`int32 height` :the height of the frame node received. (The coordinates are relative so it's important for acm to have this information)

`int32 width` :the width of the frame node received. (The coordinates are relative so it's important for acm to have this information)

`int32 angle`: face angle 

`int32[] co`: [x_upleft, y_upleft, rectangle_height, rectangle_width], a four-elements integer list which represents the coordinates of the target (face) in the frame

There are one service in the project.

*tracking.srv*

`uint32 cmd` : the command PCM sends to the ACM. 1 means start and 2 means stop.

`uint32 rsp` : task status. Later we could discuss how many kinds of task statuses and what they represent

