#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <IRremote.h>

#define Zero_button 16738455
#define One_button     16724175
#define Two_button 16718055

const int irReceiverPin = 4;
int motorPin = 9;
IRrecv irrecv(irReceiverPin);
decode_results output; 


// The TinyGPS++ object
TinyGPSPlus gps;

// The serial connection to the GSM/GPRS/GPS board
SoftwareSerial gprsSerial(2,3);

void setup()
{
  gprsSerial.begin(9600);  // the GPRS baud rate   
  Serial.begin(9600);

  irrecv.enableIRIn();   // enable ir reciever
  pinMode(motorPin, OUTPUT);
}

void loop() 
{
  //If the ir recieves an output check if it
  //matches with the defined values. If it does
  //then run the vibration motor sequence
  if (irrecv.decode(&output)) {
  Serial.println(output.value);
  unsigned int value = output.value;
  switch(value) {
    case Zero_button:
     digitalWrite(motorPin, HIGH);
     delay(500); 
     digitalWrite(motorPin, LOW);
     delay(500);
     
     digitalWrite(motorPin, HIGH);
     delay(500); 
     digitalWrite(motorPin, LOW);
     delay(500);
     
     digitalWrite(motorPin, HIGH);
     delay(500); 
     digitalWrite(motorPin, LOW);
      break;
   case One_button:
     digitalWrite(motorPin, HIGH);
     delay(500); 
     digitalWrite(motorPin, LOW);
     delay(500);
     
     digitalWrite(motorPin, HIGH);
     delay(500); 
     digitalWrite(motorPin, LOW);
     break;
   case Two_button:
     digitalWrite(motorPin, HIGH);
     delay(1500); 
     digitalWrite(motorPin, LOW);
     break;
  }

  irrecv.resume(); 

  // following code was based on an example provided at https://how2electronics.com/send-gsm-sim800-900-gprs-data-thingspeak-arduino/
   if (gprsSerial.available())
      gprsSerial.println("AT+CGATT=1"); //attatch to packet domain service
      gprsSerial.println("AT+CSTT=finding-fido.herokuapp.com/locations/"); //sets up the apn
      gprsSerial.println("AT+CIICR");//bring up wireless connection
      gprsSerial.println("AT+CIFSR");//get local IP adress
      gprsSerial.println("AT+CIPSTART=\"TCP\",\"finding-fido.herokuapp.com/locations/\",\"80\"");//start up the connection
      gprsSerial.println("AT+CIPSEND");//begin send data to remote server

      //building the JSON coordinates
      String coords = "{\"lat\":";
      coords.concat(gps.location.lat());
      coords.concat("\"long\":");
      coords.concat(gps.location.lng());
      coords.concat("\"harness\":3}");
      
      gprsSerial.println(coords); //sending the data to the webapp
      
      gprsSerial.println("AT+CIPSHUT");//close the connection
  }
}
