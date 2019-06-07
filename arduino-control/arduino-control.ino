///////////////////////////////////////////////////////////////////////////////
// Arduino control for rat maze - V 1.3  2019/02/12
///////////////////////////////////////////////////////////////////////////////
#define VERSIONMAY    1
#define VERSIONMIN    3

#include <Wire.h>  // Library which contains functions to have I2C Communication
#define SLAVE_ADDRESS 0x60 // Define the I2C address to Communicate to Uno
// i2c uses A4 and A5

// Uncomment next line to see debug messages through USB serial (arduino tty)
//#define DEBUG

//*****************************************************************************
// Constants definitions
//*****************************************************************************
enum LEDSTATES {
  LED_CONTINUE=0,    // continue with current mode
  LED_ON,            // system is on
  LED_OFF,           // system not powered
  LED_SLOW_BLINK,    // button being pressed
  LED_FAST_BLINK,    // system error, unplug
  LED_SLOW_FADE,     // system is off, waiting to start
  LED_FAST_FADE      // system is starting
};


enum SYSTEMSTATES {
  SYS_OFF=0,         // raspi is off
  SYS_PREBOOT_A,     // power button pressed, waiting for debounce check
  SYS_PREBOOT_B,     // debounce check completed, start booting
  SYS_BOOTING,       // raspi is booting
  SYS_RUNNING,       // raspi is running 
  SYS_PREHALT_A,     // power button pressed, waiting for debounce check
  SYS_PREHALT_B,     // debounce check completed, start halting
  SYS_HALT_INIT,     // raspi start halting
  SYS_HALTING        // system is halting
};

enum COMMANDS {
  RPI_KEEPALIVE=1,
  RPI_HALTING,
  VALVE_OPEN=4,             // second byte has valve number
  VALVE_CLOSE,              // second byte has valve number
  VALVE_DROP,               // second byte has valve number
  VALVE_MULTIDROP,          // second byte has valve number
  VALVE_SET_MULTINUM,       // second byte has multidrop number
  VALVE_SET_DELAYDROP,      // second byte has multidrop number
  VALVE_SET_DELAYMULTIDROP, // second byte has multidrop number
  HDMI_ON=16,               // second byte has pin number  0xXXXXABCD A:HDMI1 B:HDMI2 c:HDMI3 d:HDMI4
  HDMI_OFF,                 // second byte has pin number  0xXXXXABCD A:HDMI1 B:HDMI2 c:HDMI3 d:HDMI4
  LED,                      // second byte set state
  LEDTOGGLE.
  TRAINSTART=32,            //
  TRAINSTOP,                //
  TRIALSTART,               // second byte indicates trial type
  TEST1=90,                 // 0x5a 01011010
  TEST2=165                 // 0xa5 10100101
};


#define DELAYDROP        50
#define MULTIDROP         2
#define DELAYMULTIDROP  500


#define WAIT_FOR_RPI_BOOT    20000
#define WAIT_FOR_DEBUNCE        50
#define WAIT_FOR_PRESSDELAY   3000
#define WAIT_FOR_HALT_ACK     5500
#define WAIT_FOR_HALT        15000


#define LED_FAST_BLINK_TOP   10000
#define LED_SLOW_BLINK_TOP   50000
#define LED_FAST_FADE_TOP      300
#define LED_SLOW_FADE_TOP     3000

#define TRIAL_LED_TIME         100

//*****************************************************************************
// Variables definitions
//*****************************************************************************
volatile uint8_t raspiState; // define the state of raspi power and booting
volatile bool attendSystem; // flag to check system
volatile bool newRPIPacket = false;
volatile char bufferRX[2]; // buffer to receive data from raspi
volatile char bufferTX; // buffer to transmit data to raspi
char response;

uint8_t multiDrop;
uint8_t delayDrop;
uint16_t delayMultiDrop;

uint32_t timeLap, timeNow, timeTLed;
volatile uint8_t toggleToDo;

#ifdef DEBUG
volatile bool buttonSerial = false;
char incomingByte;
#endif

//*****************************************************************************
// Pin definitions
//*****************************************************************************
// #define RASPISTART 2

const int raspiRun = 2;  // raspi running. LOW shuts down raspi power. HIGH powers up raspi
const int raspiArduinoLed = LED_BUILTIN;  // is on when raspi is on. for debug.

const int powerButton = 4;
const int powerButtonLed = 5;

const int valveLeft = 14;    // A0
const int valveRight = 15;   // A1

const int hdmi1 = 11;  //hdmi 2a
const int hdmi2 = 10;  //hdmi 2b
const int hdmi3 = 12;  //hdmi 1a
const int hdmi4 = 13;  //hdmi 1b

const int trialLed = 8;

//*****************************************************************************
// Prototypes
//*****************************************************************************

void setup();
void valveOpen(const int valve);
void valveClose(const int valve);
void valveDrop(const int valve);
void raspiSendData();
void raspiReceiveData(int numBytes);
void arduinoReset(void);
void ledFunction(uint8_t newState);
bool isButtonPressed();
void SignalHaltRPI();
void trialLedToggle(int toggleN);
void trialLedRun (void);

void loop() {
#ifdef DEBUG
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();
    if (incomingByte == 'P') 
      buttonSerial = true;
    else if (incomingByte == 'U')
      buttonSerial = false;
    // say what you got:
    Serial.print("R:");
    Serial.println(incomingByte, DEC);
  }
#endif
  if (isButtonPressed()) attendSystem=true;
  if (attendSystem == true) {
    switch (raspiState) {
      case SYS_OFF:
        timeLap = millis();
        raspiState = SYS_PREBOOT_A;
#ifdef DEBUG
        Serial.print("S:");
        Serial.println(raspiState,DEC);
#endif
        break;
      case SYS_PREBOOT_A:
        timeNow = millis();
        if ((timeNow-timeLap) > WAIT_FOR_DEBUNCE){
          if (isButtonPressed()) {
            timeLap = millis();
            raspiState = SYS_PREBOOT_B;
            ledFunction(LED_FAST_BLINK);
#ifdef DEBUG
            Serial.print("S:");
            Serial.println(raspiState,DEC);
#endif
          }
          else {
            raspiState = SYS_OFF;
            attendSystem = false;
#ifdef DEBUG
            Serial.print("S:");
            Serial.println(raspiState,DEC);
#endif
          }
        }
        break;
      case SYS_PREBOOT_B:
        if (isButtonPressed()) {
          timeNow = millis();
          if ((timeNow-timeLap) > WAIT_FOR_PRESSDELAY){
            timeLap = millis();
            raspiState = SYS_BOOTING;
            ledFunction(LED_FAST_FADE);
            digitalWrite(raspiRun, HIGH);
#ifdef DEBUG
            Serial.print("S:");
            Serial.println(raspiState,DEC);
#endif
          }
        }
        else {
            raspiState = SYS_OFF;
            ledFunction(LED_ON);
            attendSystem = false;
#ifdef DEBUG
            Serial.print("S:");
            Serial.println(raspiState,DEC);
#endif
        }
        break;
      case SYS_BOOTING:
        timeNow=millis();
        if ((timeNow-timeLap) > WAIT_FOR_RPI_BOOT){
          // before 20 seconds arduino should receive a package from 
          // raspi saying it already boot.
          // If that did not happend, the system will indicate error
          // and go off
          digitalWrite(raspiArduinoLed, HIGH);
          ledFunction(LED_SLOW_BLINK);
          raspiState = SYS_OFF;
          digitalWrite(raspiRun,LOW);
          attendSystem = false;
#ifdef DEBUG
          Serial.print("S:");
          Serial.println(raspiState,DEC);
#endif
        }
        break;
      case SYS_RUNNING:
        timeLap = millis();
        raspiState = SYS_PREHALT_A;
#ifdef DEBUG
        Serial.print("S:");
        Serial.println(raspiState,DEC);
#endif
        break;
      case SYS_PREHALT_A:
        timeNow = millis();
        if ((timeNow-timeLap) > WAIT_FOR_DEBUNCE){
          if (isButtonPressed()) {
            timeLap = millis();
            raspiState = SYS_PREHALT_B;
            ledFunction(LED_FAST_BLINK);
#ifdef DEBUG
            Serial.print("S:");
            Serial.println(raspiState,DEC);
#endif
          }
          else {
            raspiState = SYS_RUNNING;
            attendSystem = false;
#ifdef DEBUG
            Serial.print("S:");
            Serial.println(raspiState,DEC);
#endif
          }
        }
        break;
      case SYS_PREHALT_B:
        if (isButtonPressed()) {
          timeNow = millis();
          if ((timeNow-timeLap) > WAIT_FOR_PRESSDELAY){
            timeLap = millis();
            raspiState = SYS_HALT_INIT;
            ledFunction(LED_FAST_FADE);
            SignalHaltRPI(); // sets response for next keep alive message to tell raspi to go off
#ifdef DEBUG
            Serial.print("S:");
            Serial.println(raspiState,DEC);
#endif
          }
        }
        else {
          raspiState = SYS_RUNNING;
          ledFunction(LED_SLOW_FADE);
          attendSystem = false;
#ifdef DEBUG
          Serial.print("S:");
          Serial.println(raspiState,DEC);
#endif
        }
        break;
      case SYS_HALT_INIT:
        timeNow = millis();
        if ( (timeNow-timeLap) > WAIT_FOR_HALT_ACK ) {
          // before 20 seconds arduino should receive a package from 
          // raspi saying its going to halt.
          // If that did not happend, the system will indicate error
          // and go off
          digitalWrite(raspiArduinoLed, HIGH);
          raspiState = SYS_OFF;
          ledFunction(LED_SLOW_BLINK);
          digitalWrite(raspiRun,LOW);
#ifdef DEBUG
          Serial.print("S:");
          Serial.println(raspiState,DEC);
          Serial.println("error 3");
#endif
        }
        break;
      case SYS_HALTING:
        timeNow = millis();
        if ( (timeNow-timeLap) > WAIT_FOR_HALT ) {
          // after halting time, its safe to go off
          raspiState = SYS_OFF;
          attendSystem = false;
          ledFunction(LED_ON);
          response = 'C'; 
          digitalWrite(raspiRun,LOW);
#ifdef DEBUG
          Serial.print("S:");
          Serial.println(raspiState,DEC);
#endif
        }
        break;
      default:
        attendSystem = false;
        break;
    }
  }

  if (newRPIPacket == true) {
    if (raspiState == SYS_RUNNING) {
      switch (bufferRX[0]) { // the first byte is the command 
        case RPI_KEEPALIVE:
          response = 'C'; 
#ifdef DEBUG
          Serial.print("S:");
          Serial.println(raspiState,DEC);
#endif
          break;
        case RPI_HALTING:
          timeLap = millis();
          raspiState = SYS_HALTING;
	        valveClose(valveRight);
	        valveClose(valveLeft);
          attendSystem = true;
#ifdef DEBUG
          Serial.print("S:");
          Serial.println(raspiState,DEC);
#endif
          break;
        case VALVE_OPEN:
          if (bufferRX[1]=='R') valveOpen(valveRight);
          else if (bufferRX[1]=='L') valveOpen(valveLeft);
          break;
        case VALVE_CLOSE:            // second byte has valve number
          if (bufferRX[1]=='R') valveClose(valveRight);
          else if (bufferRX[1]=='L') valveClose(valveLeft);
          break;
        case VALVE_DROP:             // second byte has valve number
          if (bufferRX[1]=='R') valveDrop(valveRight);
          else if (bufferRX[1]=='L') valveDrop(valveLeft);
          break;
        case VALVE_MULTIDROP:        // second byte has valve number
          if (bufferRX[1]=='R') valveMultiDrop(valveRight);
          else if (bufferRX[1]=='L') valveMultiDrop(valveLeft);
          break;
        case VALVE_SET_MULTINUM:   // multidrop should be between 2 and 9
          if ((bufferRX[1]>1) and (bufferRX[1]<10)) 
            multiDrop = bufferRX[1];
          break;
        case VALVE_SET_DELAYDROP:   // delaydrop should be between 1 and 250
          if ((bufferRX[1]>0) and (bufferRX[1]<251)) 
            delayDrop = bufferRX[1];
          break;
        case VALVE_SET_DELAYMULTIDROP:  // delaydrop should be between 1 and 100
          if ((bufferRX[1]>0) and (bufferRX[1]<101)) 
            delayMultiDrop = bufferRX[1]*500;
          break;
        case LED:  // 
          if (bufferRX[1]=='H') {
            digitalWrite(trialLed, HIGH);
          }
          else if (bufferRX[1]=='L') {
            digitalWrite(trialLed, LOW);
          }
#ifdef DEBUG
          Serial.print("LED: ");
          Serial.println(bufferRX[1]);
#endif
          break;
        case LEDTOGGLE:  // 
          if ((bufferRX[1]>0) and  (bufferRX[1]<=10)) {
            trialLedToggle(bufferRX[1]);
#ifdef DEBUG
            Serial.print("LED Toggle: ");
            Serial.println(bufferRX[1],DEC);
#endif
          }
          break;
        case HDMI_ON:
          if (bufferRX[1]&0x01)
            digitalWrite(hdmi1, HIGH);
          if (bufferRX[1]&0x02)
            digitalWrite(hdmi2, HIGH);
          if (bufferRX[1]&0x04)
            digitalWrite(hdmi3, HIGH);
          if (bufferRX[1]&0x08)
            digitalWrite(hdmi4, HIGH);
          break;
        case HDMI_OFF:
          if (bufferRX[1]&0x01)
            digitalWrite(hdmi1, LOW);
          if (bufferRX[1]&0x02)
            digitalWrite(hdmi2, LOW);
          if (bufferRX[1]&0x04)
            digitalWrite(hdmi3, LOW);
          if (bufferRX[1]&0x08)
            digitalWrite(hdmi4, LOW);
          break;
        case TRAINSTART:
          digitalWrite(hdmi1, HIGH);
          trialLedToggle(5);
#ifdef DEBUG
          Serial.println("Training start");
#endif
          break;
        case TRAINSTOP:
          digitalWrite(hdmi1, LOW);
          trialLedToggle(4);
#ifdef DEBUG
          Serial.println("Training stop");
#endif
          break;
        case TRIALSTART:
          if (bufferRX[1]=='L') trialLedToggle(2);
          else if (bufferRX[1]=='R') trialLedToggle(3);
#ifdef DEBUG
          Serial.print("Trial: ");
          Serial.println(bufferRX[1]);
#endif
          break;
        case TEST1:
          // pulse one second arduino led
          digitalWrite(raspiArduinoLed, HIGH);
          delay(1000);
          digitalWrite(raspiArduinoLed, LOW);
          break;
        case TEST2:
          uint8_t x;
          x = bufferRX[1];
          while (x) {
            digitalWrite(raspiArduinoLed, HIGH);
            delay(200);
            digitalWrite(raspiArduinoLed, LOW);
            delay(200);
            x--;
          }
          break;
        default:
          break;
          //  package not supported, ignored
      }
    }
    else if (raspiState==SYS_HALT_INIT) {
      if (bufferRX[0] = RPI_HALTING){
        timeLap = millis();
        raspiState = SYS_HALTING;
#ifdef DEBUG
        Serial.print("S:");
        Serial.println(raspiState,DEC);
#endif
        valveClose(valveRight);
        valveClose(valveLeft);
        attendSystem = true;
      }
      else {
        // should not happed
#ifdef DEBUG
        Serial.println("error 1");
#endif
      }
    }
    else if (raspiState==SYS_BOOTING) {
      if (bufferRX[0] = RPI_KEEPALIVE){
        raspiState=SYS_RUNNING;
        attendSystem = false;
        ledFunction(LED_SLOW_FADE);
      }
      else {
        // should not happed
#ifdef DEBUG
        Serial.println("error 2");
#endif
      }
    }
    newRPIPacket = false;
  }

  if (toggleToDo > 0) trialLedRun();
  ledFunction(LED_CONTINUE);
}


void setup() {
  // this two lines are the first thing to do, so it makes sure raspi dont boot
  pinMode(raspiRun, OUTPUT);
  digitalWrite(raspiRun, LOW);
  
  pinMode(raspiArduinoLed, OUTPUT);
  digitalWrite(raspiArduinoLed,LOW);
  pinMode(powerButton, INPUT_PULLUP);
  pinMode(powerButtonLed, OUTPUT);
  
  pinMode(valveLeft, OUTPUT);
  digitalWrite(valveLeft, LOW);
  pinMode(valveRight, OUTPUT);
  digitalWrite(valveRight, LOW);

  pinMode(hdmi1, OUTPUT);
  digitalWrite(hdmi1, LOW);
  pinMode(hdmi2, OUTPUT);
  digitalWrite(hdmi2, LOW);
  pinMode(hdmi3, OUTPUT);
  digitalWrite(hdmi3, LOW);
  pinMode(hdmi4, OUTPUT);
  digitalWrite(hdmi4, LOW);

  pinMode(trialLed, OUTPUT);
  digitalWrite(trialLed, LOW);

  //configure i2c
  Wire.begin(SLAVE_ADDRESS);   // this will begin I2C Connection with 0x40 address
  Wire.onRequest(raspiSendData);    // function called when Pi requests data
  Wire.onReceive(raspiReceiveData); // function called when Pi sends data
#ifdef DEBUG
  Serial.begin(9600); 
  Serial.print("Version ");
  Serial.print(VERSIONMAY);
  Serial.print('.');
  Serial.println(VERSIONMIN);
#endif

  raspiState = SYS_OFF;
  ledFunction(LED_ON);
  attendSystem = false;

  response = 0;
  bufferRX[0]=0;
  bufferRX[1]=0;
  bufferTX=0;
  newRPIPacket = false;

  multiDrop = MULTIDROP;
  delayDrop = DELAYDROP;
  delayMultiDrop = DELAYMULTIDROP;

  toggleToDo = 0;
}


void valveOpen(const int valve) {
  digitalWrite(valve, HIGH);
}

void valveClose(const int valve) {
  digitalWrite(valve, LOW);
}

void valveMultiDrop(const int valve) {
  int i = multiDrop;
  while (i) {
    valveDrop(valve);
    delay(delayMultiDrop);
    i--;
  }
}

void valveDrop(const int valve) {
  digitalWrite(valve, HIGH);
  delay(delayDrop);
  digitalWrite(valve, LOW);
}

void raspiSendData(){
  Wire.write(bufferTX); // return data to PI
#ifdef DEBUG
  Serial.print('K');
  Serial.print(bufferTX,DEC);
  Serial.print('\n');
#endif
}

void raspiReceiveData(int numBytes) {
#ifdef DEBUG
  Serial.print('T');
  Serial.print(numBytes,DEC);
  Serial.print('|');
#endif
  if (Wire.available()) bufferRX[0] = Wire.read(); //receives first byte -> command 
#ifdef DEBUG
  Serial.print(bufferRX[0],DEC);
#endif
  while(Wire.available()) { // 
    bufferRX[1] = Wire.read();    // receive a byte as character
#ifdef DEBUG
    Serial.print('|');
    Serial.print(bufferRX[1],DEC);
#endif
  }
  newRPIPacket = true;
  if (bufferRX[0] == RPI_KEEPALIVE) {
    bufferTX = response;
  }
  else bufferTX = 0;
#ifdef DEBUG
  Serial.print("\n");
#endif
}

bool isButtonPressed() {
#ifdef DEBUG
  if ((digitalRead(powerButton) == LOW) or (buttonSerial==true)) return true;
  else return false;
#else
  if (digitalRead(powerButton) == LOW) return true;
  else return false;
#endif
}

void SignalHaltRPI() {
  response = 'H';
  return;
}

void ledFunction(uint8_t newLedState){

  static uint8_t ledState = LED_ON;
  static uint32_t ledCounter;

  static uint8_t duty;
  static bool upward;

  if (newLedState != LED_CONTINUE) {
    ledState = newLedState;
    switch (ledState) {
      case LED_ON:
        digitalWrite(powerButtonLed,HIGH);
        break;
      case LED_OFF:
        digitalWrite(powerButtonLed,LOW);
        break;
      case LED_SLOW_FADE:
      case LED_FAST_FADE:
        duty = 0;
        upward = true;    // no 'break' because we also need ledCounter=0
      case LED_SLOW_BLINK:
      case LED_FAST_BLINK:
        ledCounter = 0;
        break;
      default:
        break;
    }
  }
  else {
    switch (ledState) {
      case LED_SLOW_BLINK:
        ledCounter++;
        if (ledCounter > LED_SLOW_BLINK_TOP) {
          if (digitalRead(powerButtonLed)==LOW)
            digitalWrite(powerButtonLed,HIGH);
          else
            digitalWrite(powerButtonLed,LOW);
          ledCounter=0;
        }
        break;
      case LED_FAST_BLINK:
        ledCounter++;
        if (ledCounter > LED_FAST_BLINK_TOP) {
          if (digitalRead(powerButtonLed)==LOW)
            digitalWrite(powerButtonLed,HIGH);
          else
            digitalWrite(powerButtonLed,LOW);
          ledCounter=0;
        }
        break;
      case LED_SLOW_FADE:
        ledCounter++;
        if (ledCounter > LED_SLOW_FADE_TOP) {
          if (upward == true) {
            duty++;
            if (duty == 90){
              upward = false;
            }
          }
          else {
            duty--;
            if (duty == 0){
              upward = true;
            }
          }
          ledCounter=0;
          analogWrite(powerButtonLed,duty);
        }
        break;
      case LED_FAST_FADE:
        ledCounter++;
        if (ledCounter > LED_FAST_FADE_TOP) {
          if (upward == true) {
            duty++;
            if (duty == 127){
              upward = false;
            }
          }
          else {
            duty--;
            if (duty == 0){
              upward = true;
            }
          }
          ledCounter=0;
          analogWrite(powerButtonLed,duty);
        }
        break;
      case LED_ON:
      case LED_OFF:
      default:
        break;
    }
  }
}


void trialLedToggle(int toggleN){
  toggleToDo = toggleN;
}

void trialLedRun (void){
  timeNow = millis();
  if ((timeNow -timeTLed) > TRIAL_LED_TIME) {
    timeTLed = millis();
    if (digitalRead(trialLed)==LOW) {
      digitalWrite(trialLed, HIGH);
    }
    else {
      digitalWrite(trialLed, LOW);
      toggleToDo -= 1;
    }
  }
}
