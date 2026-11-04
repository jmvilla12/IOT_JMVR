import os
import sys

from PySide6.QtCore import QTimer
from PySide6.QtGui import QIntValidator, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from client_mqtt import ClientMQTT
from thread_mqtt import ThreadMQTT
from mon_ihm import Ui_MainWindow

id_pc = 42906

topic_commande = f"/iot/COMMAND_{id_pc}"
topic_bargraphe = f"/iot/BARGRAPH_{id_pc}"
topic_periode = f"/iot/BLINK_{id_pc}"


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.mqtt = None
        self.thread_mqtt = None

        # (nouveau) logo IMT, cherché à côté de main.py
        logo = QPixmap(os.path.join(os.path.dirname(__file__), "imt_logo.png"))
        if not logo.isNull():
            self.lblLogo.setPixmap(logo.scaledToWidth(140))

        # seules des valeurs entières sont acceptées
        self.lneBargraph.setValidator(QIntValidator(0, 1023))
        self.lneBlink.setValidator(QIntValidator(100, 10000))

        # timer d'affichage des données (démarré à la connexion)
        self.timer = QTimer()
        self.timer.timeout.connect(self.display)

        self.btnConnect.clicked.connect(self.connectMQTT)
        self.btnDisconnect.clicked.connect(self.disconnectMQTT)
        self.btnSynchroDateTime.clicked.connect(self.synchroDateTime)
        self.btnStartMeasure.clicked.connect(self.startMeasure)
        self.btnStopMeasure.clicked.connect(self.stopMeasure)
        self.btnFastBlink.clicked.connect(self.fastBlink)
        self.btnSlowBlink.clicked.connect(self.slowBlink)
        self.btnBlink.clicked.connect(self.customBlink)
        self.lneBargraph.returnPressed.connect(self.setBargraph)
        self.btnBargraph.clicked.connect(self.setBargraph)        # (nouveau)
        self.actionQuitter.triggered.connect(self.quit)
        self.actionAPropos.triggered.connect(self.aPropos)        # (nouveau)

    # Affiche les dernières valeurs reçues du capteur
    def display(self):
        self.lblDateTime.setText(self.mqtt.date_IdO)
        self.lblTemperature.setText(f"{self.mqtt.temperature} °C")
        self.lblHumidite.setText(f"{self.mqtt.humidite} %")

    # Lit les paramètres, se connecte, lance le thread de lecture et le timer (1000 ms)
    def connectMQTT(self):
        if self.mqtt is not None:
            return
        try:
            self.mqtt = ClientMQTT(self.lneIpAddress.text(), int(self.lnePort.text()),
                                   f"Client_{id_pc}", self.lneUser.text(), self.lnePassword.text())
            self.mqtt.connect_mqtt()
        except Exception as e:
            self.mqtt = None
            self.statusbar.showMessage(f"Erreur de connexion au broker MQTT : {e}")
            return
        self.thread_mqtt = ThreadMQTT(self.mqtt)
        self.thread_mqtt.start()
        self.timer.start(1000)
        self.statusbar.showMessage("Connection au broker MQTT OK")

    # Arrête le timer, le thread de lecture puis se déconnecte
    def disconnectMQTT(self):
        if self.mqtt is None:
            return
        self.timer.stop()
        self.thread_mqtt.stopthread()
        self.thread_mqtt.join()
        self.mqtt.disconnect_mqtt()
        self.mqtt = None
        self.statusbar.showMessage("Déconnecté du broker MQTT")

    # Publie une valeur si on est connecté
    def envoyer(self, topic, valeur):
        if self.mqtt is None:
            self.statusbar.showMessage("Pas de connexion au broker MQTT")
            return
        self.mqtt.publish_mqtt(topic, valeur)
        self.statusbar.showMessage(f"Publication : {valeur} sur {topic}")

    def synchroDateTime(self):
        self.envoyer(topic_commande, 10)

    def startMeasure(self):
        self.envoyer(topic_commande, 20)
        self.envoyer(topic_commande, 50)  # mesure démarrée => clignotement rapide

    def stopMeasure(self):
        self.envoyer(topic_commande, 30)
        self.envoyer(topic_commande, 40)  # mesure arrêtée => clignotement lent

    def fastBlink(self):
        self.envoyer(topic_commande, 50)

    def slowBlink(self):
        self.envoyer(topic_commande, 40)

    def customBlink(self):
        self.envoyer(topic_periode, self.lneBlink.text())
        self.envoyer(topic_commande, 60)

    def setBargraph(self):
        self.envoyer(topic_bargraphe, self.lneBargraph.text())

    # (nouveau) menu Aide > À propos
    def aPropos(self):
        QMessageBox.about(self, "À propos",
                          f"Mon capteur IdO via MQTT\nIMT Nord Europe - PPI\nCapteur {id_pc}")

    def quit(self):
        self.close()

    # Fermeture de la fenêtre (croix ou Fichier > Quitter) : on arrête proprement le thread
    def closeEvent(self, event):
        self.disconnectMQTT()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())