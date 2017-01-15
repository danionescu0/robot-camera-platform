#include <SoftwareSerial.h>

const char MOTOR_COMMAND = 'M';
const char LIGHT_COMMAND = 'L';
const long maxDurationForMottorCommand = 300;
const byte maxPwmValue = 200;

const byte FLASH_PIN = 3;
const byte RIGHT_MOTOR_PWM_PIN = 5;
const byte RIGHT_MOTOR_EN1_PIN = A4;
const byte RIGHT_MOTOR_EN2_PIN = A5;
const byte LEFT_MOTOR_PWM_PIN = 6;
const byte LEFT_MOTOR_EN1_PIN = A3;
const byte LEFT_MOTOR_EN2_PIN = A2;

SoftwareSerial masterComm(11, 10); // RX, TX
char buffer[] = {' ',' ',' ', ' ',' ', ' ', ' ', ' '};
long lastCheckedTime;
boolean inMotion = false;

void setup() 
{
    Serial.begin(9600);
    masterComm.begin(9600);  
    pinMode(FLASH_PIN, OUTPUT);
    pinMode(LEFT_MOTOR_PWM_PIN, OUTPUT);
    pinMode(LEFT_MOTOR_EN1_PIN, OUTPUT);
    pinMode(LEFT_MOTOR_EN2_PIN, OUTPUT);
    pinMode(RIGHT_MOTOR_PWM_PIN, OUTPUT);
    pinMode(RIGHT_MOTOR_EN1_PIN, OUTPUT);
    pinMode(RIGHT_MOTOR_EN2_PIN, OUTPUT);
    lastCheckedTime = millis();
}

void loop() 
{
    if (masterComm.available() > 0) {   
        masterComm.readBytesUntil(';', buffer, 10);
        processCommand();
        clearBuffer();  
    }
    if (inMotion && millis() - lastCheckedTime > maxDurationForMottorCommand) {
        stopMotors();
    }
    /*buffer[0] = 'M';buffer[1] = ':';buffer[2] = '4';buffer[3] = '5';buffer[4] = ':';buffer[5] = '-';buffer[6] = '2';buffer[7] = '1';
    processCommand();
    delay(10000);*/
}

void processCommand() 
{
    switch (buffer[0]) {
        case (MOTOR_COMMAND):
            steerCar(getMotorPower(), getMotorDirection());
            break;
        case (LIGHT_COMMAND):
            toggleLight(buffer[1]);
            break;
    }
}

void steerCar(int power, byte direction) 
{
    Serial.print("P=");Serial.println(power);
    Serial.print("D=");Serial.println(direction);
    float leftMotor, rightMotor;
    if (direction <= 50) {
        leftMotor = map(direction, 0, 50, 0, 100);
        rightMotor = 100;
    } else {
        leftMotor = 100;
        rightMotor = map(direction, 50, 100, 100, 0);    
    }
    float realPower = map(abs(power), 0, 50, 0, 100);
    float percentLeftMotor = ((realPower / 100) * leftMotor / 100);
    float percentRightMotor = ((realPower / 100) * rightMotor / 100);
    
    Serial.write("Left=");Serial.println(percentLeftMotor * maxPwmValue);
    Serial.write("Right=");Serial.println(percentRightMotor * maxPwmValue);
    setMotorsDirection(power > 0 ? true : false);
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
    
}

byte getMotorDirection()
{
    String message = getMessage();
    byte splitPosition = message.indexOf(':', 2);

    return (byte) message.substring(2, splitPosition).toInt();
}

int getMotorPower()
{
    String message = getMessage();
    byte splitPosition = message.indexOf(':', 2);
    byte endPosition = message.indexOf(' ');
    
    return (int) message.substring(splitPosition+1, endPosition).toInt();  
}

void clearBuffer()
{
    for (int i=0; i < sizeof(buffer); i++) {
        buffer[i] = ' ';
    }
}

String getMessage() 
{
    int i = 0;
    String message = "";
    for (i=0;i < sizeof(buffer);i++) {
        message += String(buffer[i]);
    }

    return message;
}

