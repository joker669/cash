#ifndef BRACCIO_ROBOT_H_
#define BRACCIO_ROBOT_H_

#include <Servo.h>
#ifndef Servo_h
#error Sketch must include Servo.h
#endif

#define MAXIMUM_SPEED 100
#define MINIMUM_SPEED 0

enum PART
{
  BASE=0, 
  SHOULDER, 
  ELBOW,  
  WRISTROTATION, 
  WRIST  
};

enum DIRECTION
{
  L=1,  //left
  R,    //right
  F,    //forward
  B,    //backward
  U,    //up
  D,    //down
  WU,   //wrist up
  WD,   //wrist down
  H,    //horizontal
  V=0     //vertical
};

class _braccino_arm {

public:
  void init(bool doSoftStart=true);

  /* Turns off power to the servo motors. This only work if you are using a robot shield later than V1.6.
     Note that after a call to init() the power is on */
  void powerOff();

  /* Turns on power to the servo motors. This only work if you are using a robot shield later than V1.6 */
  void powerOn();
  
  Servo base;
  Servo shoulder;
  Servo elbow;
  Servo wristRotation;
  Servo wrist;
  Servo gripper;

  int parts_direction[5];
  int parts_speed[5];
  int parts_state[5];

  int check_val(int part);
  int calcSpeed(int part, int speed);
  void softStart();
  void set_speed(int part, int speed);
  void set_direction(int part, int direction);
};

#endif // BRACCIO_ROBOT_H_
