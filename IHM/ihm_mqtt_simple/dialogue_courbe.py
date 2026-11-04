import sqlite3
from datetime import datetime

from PySide6.QtCore import QDateTime
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QGraphicsScene, QDialog, QGraphicsPixmapItem
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

from graphe import Ui_GraphWindow
from thread_mqtt import id_pc, database_name, table_name


class CourbeDialog(QDialog, Ui_GraphWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # intervalle par défaut : la dernière heure
        dte = QDateTime.currentDateTime()
        dts = dte.addSecs(-3600)
        self.dteStartTime.setDateTime(dts)
        self.dteEndTime.setDateTime(dte)

        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        self.btnLoadData.clicked.connect(self.afficher_courbe)
        self.btnClearData.clicked.connect(self.effacer_courbe)

    # Convertit une figure matplotlib en image Qt
    def figure_to_pixmap(self, fig):
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        width, height = fig.get_size_inches() * fig.get_dpi()
        width, height = int(width), int(height)
        buf = canvas.buffer_rgba()
        image = QImage(buf, width, height, QImage.Format_RGBA8888)
        return QPixmap.fromImage(image)

    def afficher_courbe(self):
        # même format que dans la base (AAAA-MM-JJ HH:MM:SS) pour que BETWEEN fonctionne
        debut = self.dteStartTime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        fin = self.dteEndTime.dateTime().toString("yyyy-MM-dd HH:mm:ss")

        conn = sqlite3.connect(database_name)
        cur = conn.cursor()
        cur.execute(f"SELECT Date, Temperature, Humidite FROM {table_name} "
                    f"WHERE Date BETWEEN ? AND ? ORDER BY Date ASC", (debut, fin))
        rows = cur.fetchall()
        conn.close()

        date_x = [datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S") for r in rows]
        temp_y = [r[1] for r in rows]
        humi_y = [r[2] for r in rows]

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.plot(date_x, temp_y, marker="o", label="Température (°C)")
        ax.plot(date_x, humi_y, marker="+", label="Humidité (%)")
        ax.set_title(f"Données capteur IdO {id_pc} ({len(rows)} mesures)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Valeurs")
        ax.grid(True)
        if rows:
            ax.legend()
        fig.autofmt_xdate()  # dates inclinées pour rester lisibles
        fig.tight_layout()

        pixmap = self.figure_to_pixmap(fig)
        plt.close(fig)  # libère la figure matplotlib

        self.scene.clear()
        self.scene.addItem(QGraphicsPixmapItem(pixmap))

    def effacer_courbe(self):
        self.scene.clear()