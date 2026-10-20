// LCD 16x2 I2C + DHT22 : affichage température et humidité
#include <LiquidCrystal_AIP31068_I2C.h>
#include <DHT.h>

#define PIN_DHT A0

LiquidCrystal_AIP31068_I2C lcd(0x3E, 16, 2);
DHT dht(PIN_DHT, DHT22);

void setup()
{
  lcd.init();
  dht.begin();
  lcd.setCursor(2, 0);
  lcd.print("IMT NE - PPI");
}

void loop()
{
  float t = dht.readTemperature();
  float h = dht.readHumidity();

  if (!isnan(t) && !isnan(h))
  {
    lcd.setCursor(0, 1);
    lcd.print("T ");
    lcd.print(t, 1); // 1 décimale
    lcd.print("oC/H ");
    lcd.print(h, 1);
    lcd.print("%");
  }

  delay(2000);
}