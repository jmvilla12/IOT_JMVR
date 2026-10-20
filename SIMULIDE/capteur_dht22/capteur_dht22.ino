// Capteur DHT22 : LED verte si T < 20 °C, sinon LED rouge
#include <DHT.h>

#define PIN_DHT        A0
#define PIN_LED_VERTE 3
#define PIN_LED_ROUGE 12
#define SEUIL_TEMP    20.0

DHT dht(PIN_DHT, DHT22);

void setup() {
  pinMode(PIN_LED_VERTE, OUTPUT);
  pinMode(PIN_LED_ROUGE, OUTPUT);
  dht.begin();
}

void loop() {
  float temperature = dht.readTemperature();

  if (!isnan(temperature)) {
    if (temperature < SEUIL_TEMP) {
      digitalWrite(PIN_LED_VERTE, HIGH);
      digitalWrite(PIN_LED_ROUGE, LOW);
    } else {
      digitalWrite(PIN_LED_VERTE, LOW);
      digitalWrite(PIN_LED_ROUGE, HIGH);
    }
  }

  delay(2000);  // le DHT22 ne se lit pas plus vite que toutes les 2 s
}