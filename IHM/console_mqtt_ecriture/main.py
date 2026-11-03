from client_mqtt import ClientMQTT

id_pc = 42906
broker = "192.168.1.1"
port = 1883
username = "mos_user"
password = "mos_user"

topic_commande = f"/iot/COMMAND_{id_pc}"
topic_bargraphe = f"/iot/BARGRAPH_{id_pc}"
topic_periode = f"/iot/BLINK_{id_pc}"


def synchroniser(mqtt):
    mqtt.publish_mqtt(topic_commande, 10)
    print(f"Synchronisation du capteur : {id_pc}")


def clignoter_lent(mqtt):
    mqtt.publish_mqtt(topic_commande, 40)
    print(f"Clignotement lent de la led de vie du capteur : {id_pc}")


def clignoter_rapide(mqtt):
    mqtt.publish_mqtt(topic_commande, 50)
    print(f"Clignotement rapide de la led de vie du capteur : {id_pc}")


def demarrer_mesures(mqtt):
    mqtt.publish_mqtt(topic_commande, 20)
    print(f"Démarrage des mesures sur le capteur : {id_pc}")
    clignoter_rapide(mqtt)


def arreter_mesures(mqtt):
    mqtt.publish_mqtt(topic_commande, 30)
    print(f"Arrêt des mesures sur le capteur : {id_pc}")
    clignoter_lent(mqtt)


def clignoter_perso(mqtt):
    periode = input("Période de clignotement en ms (multiple de 100) : ")
    mqtt.publish_mqtt(topic_periode, periode)
    mqtt.publish_mqtt(topic_commande, 60)
    print(f"Clignotement personnalisé ({periode} ms) du capteur : {id_pc}")


def ecrire_bargraphe(mqtt):
    valeur = input("Choisir la valeur à écrire sur le bargraphe (0 à 1023) : ")
    mqtt.publish_mqtt(topic_bargraphe, valeur)
    print(f"Ecriture de la valeur {valeur} sur le bargraphe du capteur : {id_pc}")


if __name__ == '__main__':
    print("Démarrage de l'application")
    print("==========================")
    print("Instanciation de votre ClientMQTT")
    # 'E' dans l'id pour pouvoir tourner en même temps que le programme de lecture
    mqtt = ClientMQTT(broker, port, f"Client_E{id_pc}", username, password)
    mqtt.connect_mqtt()
    mqtt.client.loop_start()  # gère le réseau MQTT en arrière-plan pendant le menu

    car = ' '
    while car.upper() != 'Q':
        print("Console capteur IdO")
        print("-------------------")
        print("1 - Mise à l'heure du capteur")
        print("2 - Démarrage des mesures")
        print("3 - Arrêt des mesures")
        print("4 - Clignotement lent")
        print("5 - Clignotement rapide")
        print("6 - Clignotement personnalisé")
        print("7 - Ecriture du bargraphe")
        print("Q - Quitter")
        car = input("Votre choix : ")
        match car.upper():
            case '1':
                synchroniser(mqtt)
            case '2':
                demarrer_mesures(mqtt)
            case '3':
                arreter_mesures(mqtt)
            case '4':
                clignoter_lent(mqtt)
            case '5':
                clignoter_rapide(mqtt)
            case '6':
                clignoter_perso(mqtt)
            case '7':
                ecrire_bargraphe(mqtt)
            case 'Q':
                print("Arrêt du client MQTT")
            case _:
                print("Choix inconnu")

    mqtt.client.loop_stop()
    mqtt.disconnect_mqtt()
    print("Fin de l'application")