#include "FastLED.h"

///settings

#define BRIGHTNESS      30
#define  waitTime       1000//in between the two vibrations
#define  ledRefreshrate 30//in Hz

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
int delayTimes[] = {0, 0, waitTime, 0};
int vibratestate = 5;
long vibrationTimer = 0;

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;

void setup() {

  FastLED.addLeds<LED_TYPE, DATA_PIN, COLOR_ORDER>(leds, NUM_LEDS);//.setCorrection(TypicalLEDStrip);

  FastLED.setBrightness(BRIGHTNESS);

  pinMode(motors[0], OUTPUT);
  pinMode(motors[1], OUTPUT);
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  //lampWaiting();

}

void loop() {
  if (Serial.available() > 0) {
    char readCharacter = Serial.read();

    if (readCharacter == '0') {
      Serial.println("0 sent");
      ledState = 1;// to loading state
      makeVibrations();

    } else {
      Serial.print(readCharacter);
      Serial.println(" -> something else sent");
      ledState = 0;//to waiting state
    }
  }
  vibrationStuff();
  lampStuff();
  Serial.flush();
}

void vibrationStuff() {
  unsigned long currentMillis = millis();
  if (currentMillis - vibrationTimer > delayTimes[vibratestate]) {
    vibrationTimer = currentMillis;
    Serial.println(vibrationTimer);
    if (vibratestate == 0) {
      digitalWrite(motors[0], HIGH);
      Serial.println("motor 1");
    } else if (vibratestate == 1) {
      digitalWrite(motors[0], LOW);
      Serial.println("waiting");
    } else if (vibratestate == 2) {
      digitalWrite(motors[1], HIGH);
      Serial.println("motor 2");
    } else if (vibratestate == 3) {
      digitalWrite(motors[1], LOW);
      Serial.println("stopped");
    }
    vibratestate++;
  }
}
void lampStuff() {

  unsigned long currentMillis = millis();
  if (currentMillis - ledTimer > 1000 / ledRefreshrate) {

    ledTimer = currentMillis;
    if (ledState == 0) {
      //FastLED.clear();
      for (int i = 0; i < NUM_LEDS; i++) {
        if (i == ledPos % NUM_LEDS) {
          leds[i] = CHSV( 224, 0, 255);
        }

        //leds[i] = CRGB::White;
        //leds[i] = CRGB(110,200,255);
        //leds[i] += 1000;
      }
      //Serial.println("waiting");
    }
    else if (ledState == 1) {
      for (int i = 0; i < NUM_LEDS; i++) {
        if (i == ledPos % NUM_LEDS || i == (ledPos+1) % NUM_LEDS || i == (ledPos+2) % NUM_LEDS || i == (ledPos+3) % NUM_LEDS) {
          leds[i] = CHSV( 224, 0, 255);
        }
        else {
          leds[i].fadeToBlackBy( 20 );
        }
      }

      //Serial.println("loading");
    }
    ledPos++;

  }

  FastLED.show();
}

void makeVibrations() {
  delayTimes[1] = chooseState();
  delayTimes[3] = chooseState();
  vibratestate = 0;
  Serial.print("motor 1 = ");
  Serial.print(delayTimes[1]);
  Serial.print("  motor 2 = ");
  Serial.print(delayTimes[3]);
  Serial.println();
}


int chooseState() {
  int state = random(100);
  if (state < odddivision[0])state = 0;
  else if (state < odddivision[1])state = 1;
  else if (state < odddivision[2])state = 2;
  else state = 3;
  return states[state];
}


