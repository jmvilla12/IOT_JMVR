import sqlite3
from datetime import datetime
from paho.mqtt import client as mqtt_client


class ClientMQTT:
    def __init__(self, ip_address, port, client_id, username, password):
        super().__init__()
        self.ip_address = ip_address
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password
        self.client = None

        # dernières valeurs reçues du capteur
        self.version = ""
        self.temperature = ""
        self.humidite = ""
        self.date_IdO = ""

        # base SQLite d'archivage
        self.conn = None
        self.tablename = None

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc, properties):
            if rc == 0:
                print(f"Connecté au broker MQTT : {self.ip_address} {self.port}")
            else:
                print(f"Echec de la connexion, code : {rc}")

        self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id=self.client_id)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = on_connect
        self.client.connect(self.ip_address, self.port)
        return self.client

    def disconnect_mqtt(self) -> None:
        self.client.disconnect()

    # a) Connexion à la base (créée si elle n'existe pas) et création de la table
    def connect_sqlite(self, database_name, tablename):
        self.tablename = tablename
        self.conn = sqlite3.connect(database_name)
        self.conn.cursor().execute(f"CREATE TABLE IF NOT EXISTS {self.tablename} "
                                   f"(Id_capteur integer, Date text, Version text, Temperature real, Humidite real)")
        self.conn.commit()

    # b) Déconnexion de la base
    def disconnect_sqlite(self):
        self.conn.close()
        self.conn = None

    def publish_mqtt(self, topic, message, qos=0):
        self.client.publish(topic, message, qos)
        print(f"Publication : `{message}` sur `{topic}`")

    def subscribe_mqtt(self, topic, qos=0):
        def on_message(client, userdata, msg):
            # on stocke les valeurs au lieu de les afficher
            if "VERSION_" in msg.topic:
                self.version = msg.payload.decode()
            elif "TEMPERATURE_" in msg.topic:
                self.temperature = msg.payload.decode()
            elif "HUMIDITY_" in msg.topic:
                self.humidite = msg.payload.decode()
            elif "GET_DATE_" in msg.topic:
                self.date_IdO = msg.payload.decode()
                # d) GET_DATE_ est le dernier topic publié par le capteur => on archive
                self.archiver(int(msg.topic[-5:]))

        self.client.on_message = on_message
        self.client.subscribe(topic, qos)
        print(f"Attente du topic : `{topic}`")

    # Enregistre une mesure dans la base (date stockée en AAAA-MM-JJ pour pouvoir la trier)
    def archiver(self, id_capteur):
        if self.conn is None or self.temperature == "":
            return
        try:
            date = datetime.strptime(self.date_IdO, "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            self.conn.cursor().execute(f"INSERT INTO {self.tablename} VALUES (?,?,?,?,?)",
                                       (id_capteur, date, self.version,
                                        float(self.temperature), float(self.humidite)))
            self.conn.commit()
        except ValueError as e:
            print(f"Mesure non archivée : {e}")

    def wait_mqtt(self, timeout=0):
        if timeout == 0:
            self.client.loop_forever()
        else:
            self.client.loop(timeout=timeout)