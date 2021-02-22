#include "FastLED.h"
#define NUM_LEDS 120
#define LED_STRIPE_PORT 8

CRGB led_stripe[NUM_LEDS];
String input;
int led;
int prevLed=0;
int ind;
bool isPlaying = false;

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<WS2812, LED_STRIPE_PORT>(led_stripe, NUM_LEDS);
}


void playSong() {
  ind = input.indexOf(',');  //finds location of first ,
  String leds = input.substring(0, ind);
  int ind_leds = leds.indexOf(';');
  if(ind_leds > 0) {
    int led1 = leds.substring(0,ind_leds).toInt();
    int led2 = leds.substring(ind_leds+1, leds.length()).toInt();
    led_stripe[led1] = CRGB::Green;
    led_stripe[led2] = CRGB::Green;
    FastLED.show();
    delay(869+48);
    if (ind > 0) {
      led_stripe[led1] = CRGB::Black;
      led_stripe[led2] = CRGB::Black;
      input = input.substring(ind+1);
      playSong();
    } else {
      led_stripe[led1] = CRGB::Black;
      led_stripe[led2] = CRGB::Black;
      FastLED.show();
      isPlaying = false;
      input = "";
    }
  } else {
    led = leds.toInt();   //captures led data int
    prevLed = led;
    led_stripe[led] = CRGB::Green;
    FastLED.show();
    delay(869+48);
    if (ind > 0) {
      led_stripe[led] = CRGB::Black;
      input = input.substring(ind+1);
      playSong();
    } else {
      led_stripe[led] = CRGB::Black;
      FastLED.show();
      isPlaying = false;
      input = "";
    }
  }
}

void loop() {
  if(Serial.available()){
    input += Serial.readStringUntil('\n');
    Serial.print(input);
    if( input == "reset"){
      for(int i = 0; i < NUM_LEDS; i++) {
        led_stripe[i] = CRGB(0, 0, 0);
        FastLED.show();
      }
    } else {
      if(!isPlaying) {
        isPlaying = true;      
        playSong();
      }
    }
  }
}
