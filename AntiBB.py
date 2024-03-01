import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QMessageBox, QLabel, QDesktopWidget
from PyQt5.QtCore import QUrl, Qt, QObject, pyqtSignal
from PyQt5.QtGui import QDesktopServices, QFont
import threading
import re

class PingUpdater(QObject):
    ping_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        threading.Thread(target=self.start_ping, daemon=True).start()

    def start_ping(self):
        process = subprocess.Popen(['ping', '8.8.4.4', '-t'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        while True:
            output = process.stdout.readline().decode('utf-8')
            ping_time = re.search(r'time=(\d+)', output)
            if ping_time:
                self.ping_updated.emit(f"Ping: {ping_time.group(1)}ms")

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.version = 'by katat0nia'
        self.title = f'Anti-BufferBloat 1.6 - {self.version}'
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(400, 300)
        self.center()

        layout = QVBoxLayout()
        self.titleLabel = QLabel("Anti-BufferBloat", self)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.titleLabel)

        self.statusLabel = QLabel("RWAT: ", self)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setStyleSheet("font-size: 15px;")
        layout.addWidget(self.statusLabel)

        self.subtitleLabel = QLabel("No Activado= normal  |  Activado= disable", self)
        self.subtitleLabel.setAlignment(Qt.AlignCenter)
        self.subtitleLabel.setStyleSheet("font-size: 12px;")
        layout.addWidget(self.subtitleLabel)

        self.setupButtons(layout)

        self.pingLabel = QLabel("Ping: ", self)
        self.pingLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pingLabel)

        self.setLayout(layout)

        self.ping_updater = PingUpdater()
        self.ping_updater.ping_updated.connect(self.update_ping_label)

        self.show_status()

    def setupButtons(self, layout):
        self.activateButton = QPushButton('Activar Anti-BufferBloat', self)
        self.deactivateButton = QPushButton('Desactivar Anti-BufferBloat', self)
        self.bufferbloatTestButton = QPushButton('BufferBloat Test | Waveform.com', self)
        self.speedtestButton = QPushButton('Speedtest.net', self)
        self.fastButton = QPushButton('Fast.com', self)
        self.exitButton = QPushButton('Salir', self)

        buttons = [self.activateButton, self.deactivateButton, self.bufferbloatTestButton, self.speedtestButton, self.fastButton, self.exitButton]
        for button in buttons:
            button.setFont(QFont("Arial", 12))
            layout.addWidget(button)

        self.activateButton.clicked.connect(self.activate_antibufferbloat)
        self.deactivateButton.clicked.connect(self.deactivate_antibufferbloat)
        self.bufferbloatTestButton.clicked.connect(lambda: self.open_website("https://www.waveform.com/tools/bufferbloat"))
        self.speedtestButton.clicked.connect(lambda: self.open_website("https://www.speedtest.net"))
        self.fastButton.clicked.connect(lambda: self.open_website("https://www.fast.com"))
        self.exitButton.clicked.connect(self.close)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Error al ejecutar el comando: {e}")
            return None

    def activate_antibufferbloat(self):
        output = self.run_command("netsh int tcp set global autotuninglevel=disabled")
        if output is not None:
            self.run_command("ipconfig /flushdns")
            QMessageBox.information(self, "Operación completada", "Anti-BufferBloat activado y caché DNS limpiada.")
        self.show_status()

    def deactivate_antibufferbloat(self):
        output = self.run_command("netsh int tcp set global autotuninglevel=normal")
        if output is not None:
            QMessageBox.information(self, "Operación completada", "Anti-BufferBloat desactivado.")
        self.show_status()

    def show_status(self):
        output = self.run_command("netsh interface tcp show global")
        if output:
            lines = output.split('\n')
            rwat_line = next((line for line in lines if "Receive Window Auto-Tuning Level" in line), "Información no encontrada.")
            self.statusLabel.setText(rwat_line)

    def open_website(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def update_ping_label(self, ping_value):
        self.pingLabel.setText(f"{ping_value}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        /* Establece el color de fondo y de texto general de los widgets */
        QWidget {
            background-color: #2C2F33; /* Color de fondo oscuro */
            color: #CCCCCC; /* Texto claro */
        }

        /* Personaliza los botones para que coincidan con el estilo de Discord */
        QPushButton {
            background-color: #7289DA; /* Color de botón principal de Discord */
            color: #FFFFFF; /* Texto del botón */
            border-radius: 5px; /* Bordes redondeados */
            padding: 10px 10px; /* Padding */
            margin: 2px; /* Margen entre botones */
            border: none; /* Sin bordes */
        }
        QPushButton:hover {
            background-color: #677BC4; /* Color al pasar el mouse */
        }
        QPushButton:pressed {
            background-color: #5B6EAE; /* Color al hacer clic */
        }

        /* Estilo para las etiquetas (labels) */
        QLabel {
            font-size: 15px; /* Tamaño de fuente para las etiquetas */
            color: #FFFFFF; /* Color del texto de las etiquetas */
        }

        /* Estilo para la etiqueta del título */
        QLabel#titleLabel {
            font-size: 20px; /* Tamaño de fuente más grande para el título */
            font-weight: bold; /* Texto en negrita */
        }

        /* Estilo para las cajas de mensaje (MessageBox) */
        QMessageBox {
            background-color: #36393F; /* Fondo de la caja de mensaje */
        }
        QMessageBox QLabel {
            color: #FFFFFF; /* Color del texto dentro de la caja de mensaje */
        }
        QMessageBox QPushButton {
            background-color: #7289DA; /* Botones dentro de la caja de mensaje */
            color: #FFFFFF; /* Texto de los botones dentro de la caja de mensaje */
            border-radius: 5px; /* Bordes redondeados para los botones */
            padding: 5px 10px; /* Padding para los botones */
            margin: 5px; /* Margen alrededor de los botones */
        }
    """)

    ex = App()
    ex.show()
    sys.exit(app.exec_())
