// LCD 16x2 I2C (AIP31068) : affichage HELLO / WORLD
#include <LiquidCrystal_AIP31068_I2C.h>

LiquidCrystal_AIP31068_I2C lcd(0x3E, 16, 2);  // adresse, colonnes, lignes

void setup() {
  lcd.init();
  lcd.setCursor(1, 0);   // colonne 0, ligne 1
  lcd.print("HELLO");
  lcd.setCursor(7, 1);   // colonne 5, ligne 2
  lcd.print("WORLD");
}

void loop() {
}