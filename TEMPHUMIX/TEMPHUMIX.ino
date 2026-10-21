// TempHumiX (Arduino UNO R4 WiFi) : LED de vie 2 Hz, lecture DHT22 toutes les 2 s,
// date/heure du RTC, affichage LCD et envoi sur le port série
#include "rgb_lcd.h"
#include <DHT.h>
#include <RTC.h>

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

  // a) RTC initialisé à une date de départ (sera remplacé par le NTP en 6.1.3)
  RTC.begin();
  RTCTime debut(21, Month::OCTOBER, 2026, 14, 0, 0, DayOfWeek::WEDNESDAY, SaveLight::SAVING_TIME_ACTIVE);
  RTC.setTime(debut);
}

void loop()
{
  char date[21];
  char ligne[21];
  char txtT[8];
  char txtH[8];
  RTCTime now;

  // LED de vie à 2 Hz : période 500 ms = 5 ticks
  digitalWrite(PIN_LED_VIE, (tick % 5) < 2 ? HIGH : LOW);

  // b) Ligne 1 du LCD : date et heure du RTC (chaque seconde = 10 ticks)
  if (tick % 10 == 0)
  {
    RTC.getTime(now);
    sprintf(date, "%02d/%02d %02d:%02d:%02d", now.getDayOfMonth(), Month2int(now.getMonth()),
            now.getHour(), now.getMinutes(), now.getSeconds());
    lcd.setCursor(0, 0);
    lcd.print(date);
  }

  // Lecture du DHT22 toutes les 2000 ms = 20 ticks
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
    Serial.println(date);
    Serial.print("Temperature : ");
    Serial.print(txtT);
    Serial.println(" oC");
    Serial.print("Humidite    : ");
    Serial.print(txtH);
    Serial.println(" %");
    Serial.println();

    // Ligne 2 du LCD : température et humidité
    sprintf(ligne, "T %soC/H %s%%", txtT, txtH);
    lcd.setCursor(0, 1);
    lcd.print(ligne);
  }

  tick++;
  delay(100);
}