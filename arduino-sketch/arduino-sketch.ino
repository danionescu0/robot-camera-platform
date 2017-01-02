#include <SoftwareSerial.h>

const byte pwmPower = 160;
const byte powerPwmPin = 9;
const byte relay1StatePin = 8;
const byte relay2StatePin = 7;

SoftwareSerial bluetooth(11, 10); // RX, TX
char buffer[] = {' ',' ',' ', ' ',' ', ' ', ' ', ' '};

void setup() 
{
    Serial.begin(9600);
    bluetooth.begin(9600);
  
}

void loop() 
{
  if (bluetooth.available() > 0) {   
      bluetooth.readBytesUntil(';', buffer, 10);
      processCommand();
      clearBuffer();  
  } 
}

void processCommand() 
{
    for (int i=0;i<=7;i++) {
        Serial.print(buffer[i]);
    }
}


void clearBuffer()
{
    for (int i=0; i<=2; i++) {
        buffer[i] = ' ';
    }
}

