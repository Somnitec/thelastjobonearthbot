#include <FastLED.h>
#define LED_PIN     6
#define COLOR_ORDER GRB
#define CHIPSET     WS2811
#define NUM_LEDS    60
#define BRIGHTNESS  150
#define FRAMES_PER_SECOND 60
CRGB leds[NUM_LEDS];

int fonkeler = 0;
int delay1 = 30;
int delay2 = 60;
int modeswitch = 0;
int pos1 = 0;
int pos2 = 0;

long timer1 = 0;
long timer2 = 0;



void setup() {
  Serial.begin(9600);
  FastLED.addLeds<CHIPSET, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
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
    Serial.print("post2 ");
    Serial.println( pos2);
  }
  
  if (modeswitch < 2000) {
    swirling();
  }
  if (modeswitch > 2000) {
    fonkel();
  }

  modeswitch++;
  if (modeswitch > 4000) {
    modeswitch = 0;
  }

  FastLED.show(); // display this frame

  //check of brightness hoog: zoja fade. Andere optie: maak array van geactiveerde leds, laat die door een fase heen gaan
}

void fonkel() {

  if (fonkeler > 3) {
    leds[random(60)] = CRGB::Grey;;
    fonkeler = 0;

    for (int i = 0; i < NUM_LEDS; i++) {
      leds[i].fadeToBlackBy( 1 );

    }
  }
  fonkeler++;
}


void swirling() {
  for (int i = 0; i < NUM_LEDS; i++) {
    int j = 1;//for (int j = 0; j < 9; j++) {
    if (i ==  pos1 % NUM_LEDS) {
      leds[i] = CRGB::White;

    }
    else  leds[i].fadeToBlackBy( 2 );
    // }
  }

  //FastLED.delay(1000 / FRAMES_PER_SECOND);
}
