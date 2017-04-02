// source for TextMotorCommandsInterpretter: "https://github.com/danionescu0/arduino/tree/master/libraries/TextMotorCommandsInterpretter"

#include <SoftwareSerial.h>
#include <TextMotorCommandsInterpretter.h>

const char MOTOR_COMMAND = 'M';
const char LIGHT_COMMAND = 'L';
const long maxDurationForMottorCommand = 300;
const byte maxPwmValue = 230;
const long transmitingInterval = 500;
const int maxObstacleDetection = 1000; // analog read max detection value
const int minObstacleDetection = 500; // analog read min detection value

const byte FLASH_PIN = 3;

const byte RIGHT_MOTOR_PWM_PIN = 5;
const byte RIGHT_MOTOR_EN1_PIN = A4;
const byte RIGHT_MOTOR_EN2_PIN = A5;
const byte LEFT_MOTOR_PWM_PIN = 6;
const byte LEFT_MOTOR_EN1_PIN = A3;
const byte LEFT_MOTOR_EN2_PIN = A2;

const byte FRONT_DISTANCE_SENSOR = A0;
const byte BACK_DISTANCE_SENSOR = A1;

SoftwareSerial masterComm(11, 10); // RX, TX
TextMotorCommandsInterpretter motorCommandsInterpretter(-50, 50, -50, 50);

String currentCommand;
long lastCheckedTime;
long lastTransmitTime;
boolean inMotion = false;

void setup() 
{
    Serial.begin(9600);
    masterComm.begin(9600);
    masterComm.setTimeout(10);  
    pinMode(FLASH_PIN, OUTPUT);
    pinMode(LEFT_MOTOR_PWM_PIN, OUTPUT);
    pinMode(LEFT_MOTOR_EN1_PIN, OUTPUT);
    pinMode(LEFT_MOTOR_EN2_PIN, OUTPUT);
    pinMode(RIGHT_MOTOR_PWM_PIN, OUTPUT);
    pinMode(RIGHT_MOTOR_EN1_PIN, OUTPUT);
    pinMode(RIGHT_MOTOR_EN2_PIN, OUTPUT);
    lastCheckedTime = millis();
    lastTransmitTime = millis();
}

void loop() 
{
    if (masterComm.available() > 0) {   
        currentCommand = masterComm.readString();
        processCommand();
    }
    if (inMotion && millis() - lastCheckedTime > maxDurationForMottorCommand) {
        stopMotors();
    }
    if (millis() - lastTransmitTime > transmitingInterval) {
        lastTransmitTime = millis();
        masterComm.print(getObstacleData());
        Serial.print(analogRead(BACK_DISTANCE_SENSOR));Serial.print("---");
        Serial.println(getObstacleData());
    }
    /*motorCommandsInterpretter.analizeText("M:-14:40;");
    Serial.write("Left==");Serial.println(motorCommandsInterpretter.getPercentLeft());
    Serial.write("Right==");Serial.println(motorCommandsInterpretter.getPercentRight());   
    delay(10000);*/
}

String getObstacleData()
{
    //int frontDistance = analogRead(FRONT_DISTANCE_SENSOR);
    int backDistace = analogRead(BACK_DISTANCE_SENSOR);
    //frontDistance = map(frontDistance, maxObstacleDetection, minObstacleDetection, 0, 10);
    backDistace = map(backDistace, maxObstacleDetection, minObstacleDetection, 0, 10);

    return String("F=" + String(0) + ":B=" + String(backDistace) + ";");
}

void processCommand() 
{
    switch (currentCommand.charAt(0)) {
        case (MOTOR_COMMAND):
            steerCar();
            break;
        case (LIGHT_COMMAND):
            toggleLight(currentCommand.charAt(2));
            break;
    }
}

void steerCar() 
{
    motorCommandsInterpretter.analizeText(currentCommand);
    float percentLeftMotor = motorCommandsInterpretter.getPercentLeft();
    float percentRightMotor = motorCommandsInterpretter.getPercentRight();
    Serial.write("Left=");Serial.println(percentLeftMotor);
    Serial.write("Right=");Serial.println(percentRightMotor);
    setMotorsDirection(motorCommandsInterpretter.getDirection());
    analogWrite(LEFT_MOTOR_PWM_PIN, percentLeftMotor * maxPwmValue);
    analogWrite(RIGHT_MOTOR_PWM_PIN, percentRightMotor * maxPwmValue);    
    inMotion = true;
    lastCheckedTime = millis();
}

void setMotorsDirection(boolean forward)
{
    if (forward) {
        digitalWrite(LEFT_MOTOR_EN1_PIN, HIGH);
        digitalWrite(LEFT_MOTOR_EN2_PIN, LOW);
        digitalWrite(RIGHT_MOTOR_EN1_PIN, HIGH);
        digitalWrite(RIGHT_MOTOR_EN2_PIN, LOW);
    } else {
        digitalWrite(LEFT_MOTOR_EN1_PIN, LOW);
        digitalWrite(LEFT_MOTOR_EN2_PIN, HIGH);
        digitalWrite(RIGHT_MOTOR_EN1_PIN, LOW);
        digitalWrite(RIGHT_MOTOR_EN2_PIN, HIGH);
    }
}

void stopMotors()
{
    Serial.println("Stopping motors");
    analogWrite(LEFT_MOTOR_PWM_PIN, 0);
    analogWrite(RIGHT_MOTOR_PWM_PIN, 0);
    inMotion = false;
}

void toggleLight(char command)
{
    Serial.println("Toggle light");
    if (command == '1') {
        digitalWrite(FLASH_PIN, HIGH);
    } else {
        digitalWrite(FLASH_PIN, LOW);
    }
}
