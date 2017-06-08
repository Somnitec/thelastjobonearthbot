#include "FastLED.h"

///settings

#define BRIGHTNESS      255
#define  waitTime       1000//in between the two vibrations
#define  ledRefreshrate 100//in Hz

///

#define DATA_PIN    6
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB
#define NUM_LEDS    60
CRGB leds[NUM_LEDS];

long ledTimer = 0;
int ledState = 0;//0 is waiting, 1 is loading
int ledPos = 0;

int motors[] = {10, 11};

int states[] = {100, 300, 700, 1500};
int odddivision[] = {10, 50, 90};


String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;

void setup() {

  FastLED.addLeds<LED_TYPE, DATA_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);

  FastLED.setBrightness(BRIGHTNESS);

  pinMode(motors[0], OUTPUT);
  pinMode(motors[1], OUTPUT);
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  inputString.reserve(200);
  lampWaiting();

}

void loop() {
  if (Serial.available() > 0)  serialEvent();

  if (stringComplete) {
    Serial.println(inputString);
    // clear the string:
    inputString = "";
    stringComplete = false;

    lampLoading();
    doVibrations();

    lampWaiting();

  }
  lampStuff();
}

void lampWaiting() {
  ledState = 0;

}

void lampLoading() {
  ledState = 1;
}

void lampStuff() {
  
  unsigned long currentMillis = millis();
  if (currentMillis - ledTimer > 100) {
    ledTimer = currentMillis;
    if (ledState == 0) {
      for (int i = 0; i < NUM_LEDS; i++) {
        leds[i] += CRGB::White;
      }
     Serial.println("waiting");
    }
    else if (ledState == 1) {

      for (int i = 0; i < NUM_LEDS; i++) {
        if (i == ledPos % NUM_LEDS)leds[i] += CRGB::White;
        else leds[i].fadeToBlackBy( 1 );
      }
      ledPos++;
      Serial.println("loading");
    }
    FastLED.show();
  }


}

void doVibrations() {
  vibrate(0, random(100));
  delay(waitTime);
  vibrate(1, random(100));
}

void vibrate(int motor, int state) {
  Serial.print("odds =");
  Serial.println(state);
  if (state < odddivision[0])state = 0;
  else if (state < odddivision[1])state = 1;
  else if (state < odddivision[2])state = 2;
  else state = 3;
  Serial.print("state =");
  Serial.println(state);
  digitalWrite(motors[motor], HIGH);
  delay(states[state]);
  digitalWrite(motors[motor], LOW);
  /*
    if (state == 0) {
    digitalWrite(motors[motor],HIGH);
    delay(100
    }
    else if (state == 0) {

    }
  */
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }


}

