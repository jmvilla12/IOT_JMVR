// TempHumiX (Arduino UNO R4 WiFi) : LED de vie, lecture DHT22 toutes les 2 s,
// RTC synchronisé par NTP, WiFi, affichage LCD, port série, publication et souscription MQTT
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

// Topics souscrits (3.2)
const char T_COMMAND[] = GROUPE "COMMAND_" ID_PC;
const char T_BARGRAPH[] = GROUPE "BARGRAPH_" ID_PC;
const char T_BLINK[] = GROUPE "BLINK_" ID_PC;

rgb_lcd lcd;
DHT dht(PIN_DHT, DHT22);
WiFiUDP udp;
NTPClient ntp(udp, "192.168.1.254", 3600); // serveur NTP du réseau IoT, UTC+1 (heure d'hiver)
WiFiClient wifiClient;
MqttClient mqtt(wifiClient);

float temperature = 0;
float humidite = 0;
float tPrec = -100; // dernières valeurs publiées (6.1.6 b)
float hPrec = -100;
bool ntpOk = false;
bool mesureActive = true; // commandes 20 / 30
int periodeLed = 5;       // période LED en ticks : 5 = 500 ms = 2 Hz
int periodePerso = 5;     // période reçue via BLINK_ (en ticks)
unsigned int tick = 0;    // 1 tick = 100 ms

// Bargraphe piloté par MQTT : 0-1023 -> 0-10 LEDs
void afficherBargraphe(int valeur)
{
  int nb = map(constrain(valeur, 0, 1023), 0, 1023, 0, NB_LEDS);
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

// Appelée à la réception d'un message MQTT souscrit
void onMqttMessage(int tailleMessage)
{
  // acquisition du topic et du message
  String topic = mqtt.messageTopic();
  String message = "";
  while (mqtt.available())
  {
    message += (char)mqtt.read();
  }
  // conversion du message en entier
  int valeur = message.toInt();
  Serial.println(topic + " = " + message);

  if (topic.indexOf("COMMAND") >= 0)
  {
    // a) la version n'est publiée qu'après une synchro NTP réussie (commande 10)
    if (valeur == 10 && synchroNTP())
      publier(T_VERSION, VERSION);
    if (valeur == 20)
      mesureActive = true; // démarrage mesure
    if (valeur == 30)
      mesureActive = false; // arrêt mesure
    if (valeur == 40)
      periodeLed = 10; // clignotement lent (1 s)
    if (valeur == 50)
      periodeLed = 2; // clignotement rapide (200 ms)
    if (valeur == 60)
      periodeLed = periodePerso; // clignotement personnalisé
  }
  else if (topic.indexOf("BARGRAPH") >= 0)
  {
    afficherBargraphe(valeur);
  }
  else if (topic.indexOf("BLINK") >= 0)
  {
    periodePerso = max(2, valeur / 100); // ms (multiple de 100) -> ticks
  }
}

// Connexion au broker MQTT + souscription : 0 si OK, code erreur MQTT sinon
int setup_mqtt()
{
  mqtt.setId("IdO_Client_" ID_PC);
  mqtt.setUsernamePassword(MQTT_USER, MQTT_PASS);
  if (!mqtt.connect(BROKER, BROKER_PORT))
  {
    return mqtt.connectError();
  }
  // callback + souscription aux 3 topics
  mqtt.onMessage(onMqttMessage);
  mqtt.subscribe(T_COMMAND);
  mqtt.subscribe(T_BARGRAPH);
  mqtt.subscribe(T_BLINK);
  return 0;
}

// Publication température, humidité et date/heure
void publierMesures(const char *txtT, const char *txtH)
{
  char date[21];
  RTCTime now;
  RTC.getTime(now);
  sprintf(date, "%02d/%02d/%04d %02d:%02d:%02d", now.getDayOfMonth(), Month2int(now.getMonth()),
          now.getYear(), now.getHour(), now.getMinutes(), now.getSeconds());
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

  // Connexion au broker MQTT (+ souscriptions)
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

  mqtt.poll(); // maintient la connexion et appelle onMqttMessage si message reçu

  // LED de vie : allumée sur une partie de la période (5 ticks = 2 Hz par défaut)
  digitalWrite(PIN_LED_VIE, (tick % periodeLed) < periodeLed / 2 ? HIGH : LOW);

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

  // Lecture du DHT22 toutes les 2000 ms = 20 ticks (si la mesure est active)
  if (tick % 20 == 0 && mesureActive)
  {
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    if (!isnan(t) && !isnan(h))
    {
      temperature = t;
      humidite = h;
    }

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

    // b) Publication MQTT seulement si la température ou l'humidité a changé
    if (!mqtt.connected())
    {
      setup_mqtt();
    }
    if (temperature != tPrec || humidite != hPrec)
    {
      publierMesures(txtT, txtH);
      tPrec = temperature;
      hPrec = humidite;
    }
  }

  tick++;
  delay(100);
}