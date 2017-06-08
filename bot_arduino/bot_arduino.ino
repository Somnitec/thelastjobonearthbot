#include <Adafruit_NeoPixel.h>

///settings

int waitTime = 1000;//in between the two vibrations

///

#define NUM_LEDS 60
#define LED_PIN 6
  Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, LED_PIN, NEO_GRB + NEO_KHZ800);


int motors[] = {10, 11};

int states[] = {100, 300, 700, 1500};
int odddivision[] = {10, 50, 90};


String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;

void setup() {

  strip.begin();
  strip.show(); 
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
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, strip.Color(120,200,255));
  }
  strip.show();
}

void lampLoading() {
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, strip.Color(0,255,0));
  }
  strip.show();
}

void lampStuff() {

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

