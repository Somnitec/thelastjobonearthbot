#include <FastLED.h>
#define LED_PIN     6
#define COLOR_ORDER GRB
#define CHIPSET     WS2812B
#define NUM_LEDS    60
#define BRIGHTNESS  255
#define FRAMES_PER_SECOND 60
CRGB leds[NUM_LEDS];

int fonkeler = 0;
int delay1 = 30;
int delay2 = 15;
int modeswitch = 0;
int pos1 = 0;
int pos2 = 0;

long timer1 = 0;
long timer2 = 0;



void setup() {
  Serial.begin(9600);
  FastLED.addLeds<CHIPSET, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( CarbonArc  );
  FastLED.setBrightness( BRIGHTNESS );

}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - timer1 > delay1) {
    timer1 = currentMillis;
    pos1++;
    Serial.print("pos1 ");
    Serial.println( pos1);
  }
  if (currentMillis - timer2 > delay2) {
    timer2 = currentMillis;
    pos2++;
    Serial.print("pos2 ");
    Serial.println( pos2);
  }



  swirling();

  //juston();



  FastLED.show(); // display this frame

  //check of brightness hoog: zoja fade. Andere optie: maak array van geactiveerde leds, laat die door een fase heen gaan
}

void juston() {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::White;
  }
  delay(100);
}


void swirling() {
  for (int i = 0; i < NUM_LEDS; i++) {
    int j = 1;//for (int j = 0; j < 9; j++) {
    if (i ==  pos1 % NUM_LEDS) {
      leds[i] = CRGB::White;

    }
    if (i ==  pos2 % NUM_LEDS) {
      //leds[i] = CRGB::White;

    }
    else  leds[i].fadeToBlackBy( 1 );
    // }
  }

  //FastLED.delay(1000 / FRAMES_PER_SECOND);
}
