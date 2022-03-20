#include <Stepper.h>

// nema 17 bipolar motor with 200 steps per revolution draws 1.7 A at 2.8 V,
// microstepping 1/16 is 2.5 microns per step

const int stepsPerRevolution = 200;  // change this the steps/rev for your motor

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 2, 3); // Pin 2 connected to DIRECTION & Pin 3 connected to STEP Pin of Driver
void setup() {
  // initialize the serial port:
  Serial.begin(9600);
}


int stepCount = 0;         // number of steps the motor has taken
// moves 40 microns per step
// pitch length to move to
int pitchint = float (39.0) / float (0.04);


void loop() {
  // step one step:
  myStepper.step(1);
  Serial.print("steps:");
  Serial.println(stepCount);
  stepCount++;
  delay(500);
  
  myStepper.step(1);
  Serial.print("steps:");
  Serial.println(stepCount);
  stepCount++;
  delay(500);
  
  myStepper.step(1);
  Serial.print("steps:");
  Serial.println(stepCount);
  stepCount++;
  delay(500);
  
  myStepper.step(-3);
  Serial.print("steps:");
  Serial.println(stepCount);
  stepCount++;
  delay(500);
  
  
  if (stepCount > 6){
    stepper.stop();}
  
}
