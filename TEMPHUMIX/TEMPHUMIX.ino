// TempHumiX (Arduino UNO R4 WiFi) : LED de vie 2 Hz, lecture DHT22 toutes les 2 s,
// RTC synchronisé par NTP, WiFi, affichage LCD, port série et publication MQTT
#include "rgb_lcd.h"
#include <DHT.h>
#include <RTC.h>
#include <WiFiS3.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <ArduinoMqttClient.h>

#define VERSION "1.0"
#define ID_PC "42906" // numéro sous le code-barres du PC
#define GROUPE "/iot/"

#define PIN_LED_VIE 2
#define PIN_BARGRAPH 3 // bargraphe sur les broches 3 à 12
#define NB_LEDS 10
#define PIN_DHT A0

// Paramètres WiFi (5.1.1)
const char WIFI_SSID[] = "IoT IMT Nord Europe";
const char WIFI_PASS[] = "72Hin@R*";

// Paramètres broker Mosquitto (5.1.2)
const char BROKER[] = "192.168.1.1";
const int BROKER_PORT = 1883;
const char MQTT_USER[] = "mos_user";
const char MQTT_PASS[] = "mos_user";

// Topics publiés (3.2)
const char T_VERSION[] = GROUPE "VERSION_" ID_PC;
const char T_TEMP[] = GROUPE "TEMPERATURE_" ID_PC;
const char T_HUM[] = GROUPE "HUMIDITY_" ID_PC;
const char T_DATE[] = GROUPE "GET_DATE_" ID_PC;

rgb_lcd lcd;
DHT dht(PIN_DHT, DHT22);
WiFiUDP udp;
NTPClient ntp(udp, "10.12.130.1", 7200); // serveur NTP IMT, UTC+2 (heure d'été)
WiFiClient wifiClient;
MqttClient mqtt(wifiClient);

float temperature = 0;
float humidite = 0;
bool ntpOk = false;
unsigned int tick = 0; // 1 tick = 100 ms

void afficherBargraphe()
{
  int nb = humidite / 10; // humidité 0-100 % -> 0-10 LEDs
  for (int i = 0; i < NB_LEDS; i++)
  {
    digitalWrite(PIN_BARGRAPH + i, i < nb ? HIGH : LOW);
  }
}

// Connexion WiFi : true si OK, false sinon
bool setup_wifi()
{
  for (int i = 0; i < 5; i++)
  {
    if (WiFi.begin(WIFI_SSID, WIFI_PASS) == WL_CONNECTED)
    {
      break;
    }
    delay(2000);
  }
  if (WiFi.status() != WL_CONNECTED)
  {
    return false;
  }
  // attendre que le DHCP donne l'adresse IP
  for (int i = 0; i < 50 && WiFi.localIP() == IPAddress(0, 0, 0, 0); i++)
  {
    delay(100);
  }
  return true;
}

// Synchronisation NTP -> RTC : true si OK
bool synchroNTP()
{
  ntp.begin();
  ntpOk = ntp.forceUpdate();
  if (ntpOk)
  {
    RTCTime t(ntp.getEpochTime());
    RTC.setTime(t);
  }
  return ntpOk;
}

// Publie une valeur sur un topic
void publier(const char *topic, const char *valeur)
{
  mqtt.beginMessage(topic);
  mqtt.print(valeur);
  mqtt.endMessage();
}

// b) Connexion au broker MQTT : 0 si OK, code erreur MQTT sinon
int setup_mqtt()
{
  mqtt.setId("IdO_Client_" ID_PC);
  mqtt.setUsernamePassword(MQTT_USER, MQTT_PASS);
  if (!mqtt.connect(BROKER, BROKER_PORT))
  {
    return mqtt.connectError();
  }
  return 0;
}

// d) Publication des 4 topics
void publierMesures(const char *txtT, const char *txtH)
{
  char date[21];
  RTCTime now;
  RTC.getTime(now);
  sprintf(date, "%02d/%02d/%04d %02d:%02d:%02d", now.getDayOfMonth(), Month2int(now.getMonth()),
          now.getYear(), now.getHour(), now.getMinutes(), now.getSeconds());
  publier(T_VERSION, VERSION);
  publier(T_TEMP, txtT);
  publier(T_HUM, txtH);
  publier(T_DATE, date);
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
  RTC.begin();

  // Connexion au WiFi puis mise à l'heure par NTP
  lcd.print("Connexion WiFi..");
  bool wifiOk = setup_wifi();
  synchroNTP();

  // Écran d'accueil : version + date / adresse IP (3 s)
  char accueil[21];
  RTCTime now;
  RTC.getTime(now);
  sprintf(accueil, "V%s  %02d/%02d/%04d", VERSION, now.getDayOfMonth(), Month2int(now.getMonth()), now.getYear());
  String ip = wifiOk ? WiFi.localIP().toString() : String("WiFi KO");
  lcd.clear();
  lcd.print(accueil);
  lcd.setCursor(0, 1);
  lcd.print(ip);
  Serial.println(accueil);
  Serial.println(ip);
  delay(3000);
  lcd.clear();

  // c) Connexion au broker MQTT
  int err = setup_mqtt();
  Serial.print("MQTT : ");
  Serial.println(err);
}

void loop()
{
  char date[21];
  char ligne[21];
  char txtT[8];
  char txtH[8];
  RTCTime now;

  mqtt.poll(); // maintient la connexion MQTT (keep alive)

  // LED de vie à 2 Hz : période 500 ms = 5 ticks
  digitalWrite(PIN_LED_VIE, (tick % 5) < 2 ? HIGH : LOW);

  // Ligne 1 du LCD : date et heure (chaque seconde), ou message si pas de NTP
  if (tick % 10 == 0)
  {
    RTC.getTime(now);
    sprintf(date, "%02d/%02d %02d:%02d:%02d", now.getDayOfMonth(), Month2int(now.getMonth()),
            now.getHour(), now.getMinutes(), now.getSeconds());
    lcd.setCursor(0, 0);
    if (ntpOk)
    {
      lcd.print(date);
    }
    else
    {
      lcd.print("Pas de synch NTP");
    }
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

    // e) Publication MQTT toutes les 2 s (reconnexion si besoin)
    if (!mqtt.connected())
    {
      setup_mqtt();
    }
    publierMesures(txtT, txtH);
  }

  tick++;
  delay(100);
}