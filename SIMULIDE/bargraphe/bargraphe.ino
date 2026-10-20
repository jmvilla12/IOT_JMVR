// Chenillard sur un bargraphe de 10 LEDs (broches 3 a 12), pas de 100 ms
#define PREMIERE_LED 3
#define NB_LEDS      10
#define PERIODE_MS   100

void setup() {
  for (int i = 0; i < NB_LEDS; i++) {
    pinMode(PREMIERE_LED + i, OUTPUT);
    digitalWrite(PREMIERE_LED + i, LOW);
  }
}

void loop() {
  for (int i = 0; i < NB_LEDS; i++) {
    digitalWrite(PREMIERE_LED + i, HIGH);
    delay(PERIODE_MS);
    digitalWrite(PREMIERE_LED + i, LOW);
  }
}
