#include "m_braccino.h"
#include <Arduino.h>

#define SOFT_START_CONTROL_PIN 12
#define BIG_JOINT_MAXIMUM_SPEED 140
#define DEFAULT_START_SPEED 40
#define MS_PER_S 1000
#define SOFT_START_TIME 1000

void _braccino_arm::powerOn(){
    digitalWrite(SOFT_START_CONTROL_PIN,HIGH);
}

void _braccino_arm::powerOff() {
    digitalWrite(SOFT_START_CONTROL_PIN,LOW);
}

void _braccino_arm::softStart() {
  long int startTime=millis();
  while(millis()-startTime < SOFT_START_TIME) {
    digitalWrite(SOFT_START_CONTROL_PIN,LOW);
    delayMicroseconds(450);
    digitalWrite(SOFT_START_CONTROL_PIN,HIGH);
    delayMicroseconds(20); 
  }
}

void _braccino_arm::init(bool doSoftStart) {
  if (doSoftStart) {
    pinMode(SOFT_START_CONTROL_PIN,OUTPUT);
    digitalWrite(SOFT_START_CONTROL_PIN,LOW);
  }

  base.attach(11);
  shoulder.attach(10);
  elbow.attach(9);
  wrist.attach(5);
  wristRotation.attach(6);
  gripper.attach(3);
        
  base.write(90);
  shoulder.write(90);
  elbow.write(90);
  wrist.write(90);
  wristRotation.write(90);
  gripper.write(73);
  if (doSoftStart) {
    softStart();
  }
}

int _braccino_arm::calcSpeed(int part, int speed){
  return speed;
}

void _braccino_arm::set_speed(int part, int speed){
  speed = max(MINIMUM_SPEED, speed);
  speed = min(MAXIMUM_SPEED, speed);
  parts_speed[part] = speed;
  return;
}

void _braccino_arm::set_direction(int part, int direction){
  parts_direction[part] = direction;
  return;
}

int _braccino_arm::check_val(int part){
  // M1=base degrees. Allowed values from 0 to 180 degrees
  // M2=shoulder degrees. Allowed values from 15 to 165 degrees
  // M3=elbow degrees. Allowed values from 0 to 180 degrees
  // M4=wrist degrees. Allowed values from 0 to 180 degrees
  // M5=wrist rotation degrees. Allowed values from 0 to 180 degrees
  // M6=gripper degrees. Allowed values from 10 to 73 degrees. 10: the toungue is open, 73: the gripper is closed.
  int temp = parts_state[part];
  switch(part){
    case SHOULDER:
      if(parts_direction[part] == B){
        temp = parts_state[SHOULDER] - parts_speed[SHOULDER];
      }
      else if(parts_direction[part] == F){
        temp = parts_state[SHOULDER] + parts_speed[SHOULDER];
      }
      //temp = max(700, temp);
      //temp = min(2245, temp);
      temp = max(1000, temp);
      temp = min(2000, temp);
      parts_state[part] = temp;
      //Serial.print(temp);
      //Serial.print("\n");
      return temp;
    case BASE:
      if(parts_direction[part] == L){
        temp = parts_state[BASE] - parts_speed[BASE];
      }
      else if(parts_direction[part] == R){
        temp = parts_state[BASE] + parts_speed[BASE];
      }
      break;
    case ELBOW:
      if(parts_direction[part] == D){
        temp = parts_state[ELBOW] - parts_speed[ELBOW];
      }
      else if(parts_direction[part] == U){
        temp = parts_state[ELBOW] + parts_speed[ELBOW];
      }
      break;
    case WRISTROTATION:
      if(parts_direction[part] == WD){
        temp = parts_state[WRISTROTATION] - parts_speed[WRISTROTATION];
      }
      else if(parts_direction[part] == WU){
        temp = parts_state[WRISTROTATION] + parts_speed[WRISTROTATION];
      }
      break;
    case WRIST:
      if(parts_direction[part] == H){
        temp = 90;
      }
      if(parts_direction[part] == V){
        temp = 0;
      }
      parts_state[part] = temp;
      return temp;
    default:
      break;
  }
  temp = max(MIN_PULSE_WIDTH, temp);
  temp = min(MAX_PULSE_WIDTH, temp);
  parts_state[part] = temp;
  return temp;
}
