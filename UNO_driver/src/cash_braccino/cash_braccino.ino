#include "m_braccino.h"

#define DEBUG 0
#define MIN_SPEED 0
#define MAX_SPEED 100
#define INPUT_BUFFER_SIZE 50
#define DELAY_TIME 20
_braccino_arm braccino;
char buffer[INPUT_BUFFER_SIZE]; 

void setup() {
  // put your setup code here, to run once:
  braccino.init();
  Serial.begin(9600);
  delay(1000);
  for(int i=0; i < 5; i++){
    braccino.parts_direction[i] = 0;
    braccino.parts_speed[i] = 20;
    braccino.parts_state[i] = 0;
  }
  braccino.parts_state[BASE] = braccino.base.readMicroseconds();
  braccino.parts_state[SHOULDER] = braccino.shoulder.readMicroseconds();
  braccino.parts_state[ELBOW] = braccino.elbow.readMicroseconds();
  braccino.parts_state[WRISTROTATION] = braccino.wristRotation.readMicroseconds();
  
//TEST
  //braccino.set_direction(WRISTROTATION, WU);
}

int ii = 0;


void loop() {
  // put your main code here, to run repeatedly:
  int temp = 0;
  int p_temp = 0;
  //update motion code here
  p_temp = braccino.parts_state[BASE];
  temp = braccino.check_val(BASE);
  if(temp != p_temp)
    braccino.base.writeMicroseconds(temp);

  p_temp = braccino.parts_state[SHOULDER];
  temp = braccino.check_val(SHOULDER);
  if(temp != p_temp)
    braccino.shoulder.writeMicroseconds(temp);

  p_temp = braccino.parts_state[ELBOW];
  temp = braccino.check_val(ELBOW);
  if(temp != p_temp)
    braccino.elbow.writeMicroseconds(temp);

  p_temp = braccino.parts_state[WRISTROTATION];
  temp = braccino.check_val(WRISTROTATION);
  if(temp != p_temp)
    braccino.wristRotation.writeMicroseconds(temp);

  p_temp = braccino.parts_state[WRIST];
  temp = braccino.check_val(WRIST);
  if(temp != p_temp)
    braccino.wrist.write(temp);
  delay(DELAY_TIME);
  //TEST
  /*
   * ii++;
  if(ii == 150){
    ii = 0;
    if(braccino.parts_direction[WRISTROTATION] == WU){
      braccino.set_direction(WRISTROTATION, WD);
    }
    else{
      braccino.set_direction(WRISTROTATION, WU);
    }
  }*/
}

void serialEvent() {
  if (Serial.available() == 7) {
    int numdata = 0;
    int part = 0;
    int direction = 0;
    int speed = 0;
    // get the new byte:
    numdata = Serial.readBytes(buffer,6);
    buffer[6] = '\0';
#if DEBUG
    Serial.print(numdata);
    Serial.print("\nbuffer:");
    Serial.print(buffer);
#endif
    if(buffer[0] != 'S'){
      Serial.write('F');
      return;
    }
    part = buffer[1] - '0';
    direction = buffer[2] - '0';
    for(int i = 0; i < 3; i++){
      speed = (buffer[3+i]-'0') + speed * 10;
    }
    speed = max(0, speed);
    speed = min(100, speed);

    braccino.set_direction(part, direction);
    braccino.set_speed(part, speed);
#if DEBUG
    Serial.print("\npart : ");
    Serial.print(part);
    Serial.print("direction: ");
    Serial.print(direction);
    Serial.print("speed: ");
    Serial.print(speed);
    Serial.print("\n");
#endif
    Serial.write('T');
    delay(20);
    while(Serial.read() >= 0){
    }
  }
}
