// TempHumiX (Arduino UNO R4 WiFi) : LED de vie 2 Hz, lecture DHT22 toutes les 2 s,
// affichage LCD et envoi sur le port série
#include "rgb_lcd.h"
#include <DHT.h>

#define PIN_LED_VIE 2
#define PIN_BARGRAPH 3 // bargraphe sur les broches 3 à 12
#define NB_LEDS 10
#define PIN_DHT A0

rgb_lcd lcd;
DHT dht(PIN_DHT, DHT22);

float temperature = 0;
float humidite = 0;
unsigned int tick = 0; // 1 tick = 100 ms

void afficherBargraphe()
{
  int nb = humidite / 10; // humidité 0-100 % -> 0-10 LEDs
  for (int i = 0; i < NB_LEDS; i++)
  {
    digitalWrite(PIN_BARGRAPH + i, i < nb ? HIGH : LOW);
  }
}

void setup()
{
  pinMode(PIN_LED_VIE, OUTPUT);
  for (int i = 0; i < NB_LEDS; i++)
  {
    pinMode(PIN_BARGRAPH + i, OUTPUT);
  }
  Serial.begin(9600);
  lcd.begin(16, 2);
  dht.begin();

  lcd.setCursor(2, 0);
  lcd.print("IMT NE - PPI");
}

void loop()
{
  char ligne[21];
  char txtT[8];
  char txtH[8];

  // a) LED de vie à 2 Hz : période 500 ms = 5 ticks
  digitalWrite(PIN_LED_VIE, (tick % 5) < 2 ? HIGH : LOW);

  // b) Lecture du DHT22 toutes les 2000 ms = 20 ticks
  if (tick % 20 == 0)
  {
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    if (!isnan(t) && !isnan(h))
    {
      temperature = t;
      humidite = h;
    }
    afficherBargraphe();

    dtostrf(temperature, 4, 1, txtT);
    dtostrf(humidite, 4, 1, txtH);

    // Envoi sur le port série
    Serial.print("Temperature : ");
    Serial.print(txtT);
    Serial.println(" oC");
    Serial.print("Humidite    : ");
    Serial.print(txtH);
    Serial.println(" %");
    Serial.println();

    // c) Ligne 2 du LCD : température et humidité
    sprintf(ligne, "T %soC/H %s%%", txtT, txtH);
    lcd.setCursor(0, 1);
    lcd.print(ligne);
  }

  tick++;
  delay(100);
}