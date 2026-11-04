# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mon_ihm.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 800)
        self.actionQuitter = QAction(MainWindow)
        self.actionQuitter.setObjectName(u"actionQuitter")
        self.actionAPropos = QAction(MainWindow)
        self.actionAPropos.setObjectName(u"actionAPropos")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QPushButton { min-height: 44px; border: 1px solid #e0e0e0; border-radius: 3px; background-color: #3c3c3c; color: white; }\n"
"QPushButton:hover { background-color: #4a4a4a; }\n"
"QPushButton:pressed { background-color: #5a5a5a; }\n"
"QLineEdit { min-height: 28px; }")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.grpBroker = QGroupBox(self.centralwidget)
        self.grpBroker.setObjectName(u"grpBroker")
        self.grpBroker.setStyleSheet(u"QLabel { font-weight: bold; }")
        self.gridBroker = QGridLayout(self.grpBroker)
        self.gridBroker.setObjectName(u"gridBroker")
        self.lblLogo = QLabel(self.grpBroker)
        self.lblLogo.setObjectName(u"lblLogo")
        self.lblLogo.setMinimumSize(QSize(210, 0))
        self.lblLogo.setAlignment(Qt.AlignCenter)

        self.gridBroker.addWidget(self.lblLogo, 0, 0, 4, 1)

        self.lblIpAddress = QLabel(self.grpBroker)
        self.lblIpAddress.setObjectName(u"lblIpAddress")
        self.lblIpAddress.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.gridBroker.addWidget(self.lblIpAddress, 0, 1, 1, 1)

        self.lneIpAddress = QLineEdit(self.grpBroker)
        self.lneIpAddress.setObjectName(u"lneIpAddress")

        self.gridBroker.addWidget(self.lneIpAddress, 0, 2, 1, 1)

        self.lblPort = QLabel(self.grpBroker)
        self.lblPort.setObjectName(u"lblPort")
        self.lblPort.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.gridBroker.addWidget(self.lblPort, 1, 1, 1, 1)

        self.lnePort = QLineEdit(self.grpBroker)
        self.lnePort.setObjectName(u"lnePort")

        self.gridBroker.addWidget(self.lnePort, 1, 2, 1, 1)

        self.lblUser = QLabel(self.grpBroker)
        self.lblUser.setObjectName(u"lblUser")
        self.lblUser.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.gridBroker.addWidget(self.lblUser, 2, 1, 1, 1)

        self.lneUser = QLineEdit(self.grpBroker)
        self.lneUser.setObjectName(u"lneUser")

        self.gridBroker.addWidget(self.lneUser, 2, 2, 1, 1)

        self.lblPassword = QLabel(self.grpBroker)
        self.lblPassword.setObjectName(u"lblPassword")
        self.lblPassword.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.gridBroker.addWidget(self.lblPassword, 3, 1, 1, 1)

        self.lnePassword = QLineEdit(self.grpBroker)
        self.lnePassword.setObjectName(u"lnePassword")
        self.lnePassword.setEchoMode(QLineEdit.Password)

        self.gridBroker.addWidget(self.lnePassword, 3, 2, 1, 1)

        self.btnConnect = QPushButton(self.grpBroker)
        self.btnConnect.setObjectName(u"btnConnect")

        self.gridBroker.addWidget(self.btnConnect, 4, 1, 1, 1)

        self.btnDisconnect = QPushButton(self.grpBroker)
        self.btnDisconnect.setObjectName(u"btnDisconnect")

        self.gridBroker.addWidget(self.btnDisconnect, 4, 2, 1, 1)

        self.gridBroker.setColumnStretch(1, 1)
        self.gridBroker.setColumnStretch(2, 1)

        self.verticalLayout.addWidget(self.grpBroker)

        self.grpDonnees = QGroupBox(self.centralwidget)
        self.grpDonnees.setObjectName(u"grpDonnees")
        self.gridDonnees = QGridLayout(self.grpDonnees)
        self.gridDonnees.setObjectName(u"gridDonnees")
        self.lblDateTime = QLabel(self.grpDonnees)
        self.lblDateTime.setObjectName(u"lblDateTime")
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(12)
        self.lblDateTime.setFont(font)
        self.lblDateTime.setAlignment(Qt.AlignCenter)

        self.gridDonnees.addWidget(self.lblDateTime, 0, 0, 1, 4)

        self.lblTitreTemperature = QLabel(self.grpDonnees)
        self.lblTitreTemperature.setObjectName(u"lblTitreTemperature")
        font1 = QFont()
        font1.setBold(True)
        self.lblTitreTemperature.setFont(font1)

        self.gridDonnees.addWidget(self.lblTitreTemperature, 1, 0, 1, 1)

        self.lblTemperature = QLabel(self.grpDonnees)
        self.lblTemperature.setObjectName(u"lblTemperature")
        self.lblTemperature.setFont(font)

        self.gridDonnees.addWidget(self.lblTemperature, 1, 1, 1, 1)

        self.lblTitreHumidite = QLabel(self.grpDonnees)
        self.lblTitreHumidite.setObjectName(u"lblTitreHumidite")
        self.lblTitreHumidite.setFont(font1)
        self.lblTitreHumidite.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.gridDonnees.addWidget(self.lblTitreHumidite, 1, 2, 1, 1)

        self.lblHumidite = QLabel(self.grpDonnees)
        self.lblHumidite.setObjectName(u"lblHumidite")
        self.lblHumidite.setFont(font)

        self.gridDonnees.addWidget(self.lblHumidite, 1, 3, 1, 1)


        self.verticalLayout.addWidget(self.grpDonnees)

        self.grpCommandes = QGroupBox(self.centralwidget)
        self.grpCommandes.setObjectName(u"grpCommandes")
        self.gridCommandes = QGridLayout(self.grpCommandes)
        self.gridCommandes.setObjectName(u"gridCommandes")
        self.btnSynchroDateTime = QPushButton(self.grpCommandes)
        self.btnSynchroDateTime.setObjectName(u"btnSynchroDateTime")

        self.gridCommandes.addWidget(self.btnSynchroDateTime, 0, 0, 1, 2)

        self.btnStopMeasure = QPushButton(self.grpCommandes)
        self.btnStopMeasure.setObjectName(u"btnStopMeasure")

        self.gridCommandes.addWidget(self.btnStopMeasure, 1, 0, 1, 1)

        self.btnStartMeasure = QPushButton(self.grpCommandes)
        self.btnStartMeasure.setObjectName(u"btnStartMeasure")

        self.gridCommandes.addWidget(self.btnStartMeasure, 1, 1, 1, 1)

        self.btnSlowBlink = QPushButton(self.grpCommandes)
        self.btnSlowBlink.setObjectName(u"btnSlowBlink")

        self.gridCommandes.addWidget(self.btnSlowBlink, 2, 0, 1, 1)

        self.btnFastBlink = QPushButton(self.grpCommandes)
        self.btnFastBlink.setObjectName(u"btnFastBlink")

        self.gridCommandes.addWidget(self.btnFastBlink, 2, 1, 1, 1)

        self.btnBlink = QPushButton(self.grpCommandes)
        self.btnBlink.setObjectName(u"btnBlink")

        self.gridCommandes.addWidget(self.btnBlink, 3, 0, 1, 1)

        self.layoutBlink = QHBoxLayout()
        self.layoutBlink.setObjectName(u"layoutBlink")
        self.lneBlink = QLineEdit(self.grpCommandes)
        self.lneBlink.setObjectName(u"lneBlink")
        self.lneBlink.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.layoutBlink.addWidget(self.lneBlink)

        self.lblMs = QLabel(self.grpCommandes)
        self.lblMs.setObjectName(u"lblMs")
        self.lblMs.setFont(font1)

        self.layoutBlink.addWidget(self.lblMs)


        self.gridCommandes.addLayout(self.layoutBlink, 3, 1, 1, 1)

        self.btnBargraph = QPushButton(self.grpCommandes)
        self.btnBargraph.setObjectName(u"btnBargraph")

        self.gridCommandes.addWidget(self.btnBargraph, 4, 0, 1, 1)

        self.lneBargraph = QLineEdit(self.grpCommandes)
        self.lneBargraph.setObjectName(u"lneBargraph")

        self.gridCommandes.addWidget(self.lneBargraph, 4, 1, 1, 1)

        self.gridCommandes.setColumnStretch(0, 1)
        self.gridCommandes.setColumnStretch(1, 1)

        self.verticalLayout.addWidget(self.grpCommandes)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 640, 22))
        self.menuFichier = QMenu(self.menubar)
        self.menuFichier.setObjectName(u"menuFichier")
        self.menuAide = QMenu(self.menubar)
        self.menuAide.setObjectName(u"menuAide")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menuAide.menuAction())
        self.menuFichier.addAction(self.actionQuitter)
        self.menuAide.addAction(self.actionAPropos)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Mon capteur IDO via MQTT (c)2026 CERI SN - PPI", None))
        self.actionQuitter.setText(QCoreApplication.translate("MainWindow", u"Quitter", None))
        self.actionAPropos.setText(QCoreApplication.translate("MainWindow", u"\u00c0 propos", None))
        self.grpBroker.setTitle(QCoreApplication.translate("MainWindow", u"Param\u00e8tres de communication du Broker MQTT", None))
        self.lblLogo.setText(QCoreApplication.translate("MainWindow", u"IMT Nord Europe", None))
        self.lblIpAddress.setText(QCoreApplication.translate("MainWindow", u"Adresse IP :", None))
        self.lneIpAddress.setText(QCoreApplication.translate("MainWindow", u"192.168.1.1", None))
        self.lblPort.setText(QCoreApplication.translate("MainWindow", u"Port :", None))
        self.lnePort.setText(QCoreApplication.translate("MainWindow", u"1883", None))
        self.lblUser.setText(QCoreApplication.translate("MainWindow", u"Utilisateur :", None))
        self.lneUser.setText(QCoreApplication.translate("MainWindow", u"mos_user", None))
        self.lblPassword.setText(QCoreApplication.translate("MainWindow", u"Mot de passe :", None))
        self.lnePassword.setText(QCoreApplication.translate("MainWindow", u"mos_user", None))
        self.btnConnect.setText(QCoreApplication.translate("MainWindow", u"Connecter", None))
        self.btnDisconnect.setText(QCoreApplication.translate("MainWindow", u"D\u00e9connecter", None))
        self.grpDonnees.setTitle(QCoreApplication.translate("MainWindow", u"Affichage des donn\u00e9es du capteur", None))
        self.lblDateTime.setText(QCoreApplication.translate("MainWindow", u"00/00/0000 00:00:00", None))
        self.lblTitreTemperature.setText(QCoreApplication.translate("MainWindow", u"Temp\u00e9rature (en \u00b0C) :", None))
        self.lblTemperature.setText(QCoreApplication.translate("MainWindow", u"00.0", None))
        self.lblTitreHumidite.setText(QCoreApplication.translate("MainWindow", u"Humidit\u00e9 (en %) :", None))
        self.lblHumidite.setText(QCoreApplication.translate("MainWindow", u"00.0", None))
        self.grpCommandes.setTitle(QCoreApplication.translate("MainWindow", u"Commandes", None))
        self.btnSynchroDateTime.setText(QCoreApplication.translate("MainWindow", u"Synchronisation de la date et heure du capteur (NTP)", None))
        self.btnStopMeasure.setText(QCoreApplication.translate("MainWindow", u"Arr\u00eater les mesures", None))
        self.btnStartMeasure.setText(QCoreApplication.translate("MainWindow", u"D\u00e9marrer les mesures", None))
        self.btnSlowBlink.setText(QCoreApplication.translate("MainWindow", u"Clignotement lent", None))
        self.btnFastBlink.setText(QCoreApplication.translate("MainWindow", u"Clignotement rapide", None))
        self.btnBlink.setText(QCoreApplication.translate("MainWindow", u"Clignotement personnalis\u00e9", None))
        self.lneBlink.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.lblMs.setText(QCoreApplication.translate("MainWindow", u"ms", None))
        self.btnBargraph.setText(QCoreApplication.translate("MainWindow", u"Valeur du bargraphe :", None))
        self.menuFichier.setTitle(QCoreApplication.translate("MainWindow", u"Fichier", None))
        self.menuAide.setTitle(QCoreApplication.translate("MainWindow", u"Aide", None))
    # retranslateUi

