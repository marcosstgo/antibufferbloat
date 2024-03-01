import sys
import subprocess
import webbrowser
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QMessageBox, QLabel, QDesktopWidget
from PyQt5.QtCore import QUrl, Qt, QTimer, QObject, pyqtSignal
from PyQt5.QtGui import QDesktopServices, QColor, QFont, QIcon
import threading
import re

class PingUpdater(QObject):
    ping_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def start_ping(self):
        def ping():
            process = subprocess.Popen(['ping', 'google.com', '-t'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
            while True:
                output = process.stdout.readline().decode('utf-8')
                ping_time = re.search(r'time=(\d+)', output)
                if ping_time:
                    self.ping_updated.emit(f"Ping: {ping_time.group(1)}ms")

        threading.Thread(target=ping, daemon=True).start()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.version = 'by katat0nia'  # Indicación de la versión
        self.title = f'Anti-BufferBloat 1.5 - {self.version}'
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        # Establece el tamaño inicial de la ventana.
        self.resize(400, 300)
        self.center()  # Llama a la función para centrar la ventana.

        layout = QVBoxLayout()
        self.titleLabel = QLabel("Anti-BufferBloat", self)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("font-size: 20px; font-weight: bold;")
        
        layout.addWidget(self.titleLabel)
        
        # Etiqueta para mostrar el estado de Receive Window Auto Tuning Level
        self.statusLabel = QLabel("RWAT: ", self)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.statusLabel)

        # Etiqueta para mostrar leyenda | Activado=disable & No Activado=Normal
        self.subtitleLabel = QLabel("No Activado= normal  |  Activado= disable", self)
        self.subtitleLabel.setAlignment(Qt.AlignCenter)
        self.subtitleLabel.setStyleSheet("font-size: 11px; ")
        layout.addWidget(self.subtitleLabel)
        

        # Botones
        self.activateButton = QPushButton('Activar Anti-BufferBloat', self)
        self.deactivateButton = QPushButton('Desactivar Anti-BufferBloat', self)
        self.showButton = QPushButton('Actualizar estado del Auto-Tuning', self)
        self.bufferbloatTestButton = QPushButton('BufferBloat Test | Waveform.com', self)
        self.speedtestButton = QPushButton('Speedtest.net', self)
        self.fastButton = QPushButton('Fast.com', self)
        self.exitButton = QPushButton('Salir', self)

        # Ajustar el tamaño de fuente de los botones
        font = QFont()
        font.setPointSize(12)  # Tamaño de fuente aumentado
        self.activateButton.setFont(font)
        self.deactivateButton.setFont(font)
        self.showButton.setFont(font)
        self.bufferbloatTestButton.setFont(font)
        self.speedtestButton.setFont(font)
        self.fastButton.setFont(font)
        self.exitButton.setFont(font)

        # Conectar botones a las funciones
        self.activateButton.clicked.connect(self.activate_antibufferbloat)
        self.deactivateButton.clicked.connect(self.deactivate_antibufferbloat)
        self.showButton.clicked.connect(self.show_status)
        self.bufferbloatTestButton.clicked.connect(lambda: self.open_website("https://www.waveform.com/tools/bufferbloat"))
        self.speedtestButton.clicked.connect(lambda: self.open_website("https://www.speedtest.net"))
        self.fastButton.clicked.connect(lambda: self.open_website("https://www.fast.com"))
        self.exitButton.clicked.connect(self.close)

        # Añadir botones al layout
        buttons = [self.activateButton, self.deactivateButton, self.showButton, self.bufferbloatTestButton, self.speedtestButton, self.fastButton, self.exitButton]
        for button in buttons:
            layout.addWidget(button)

        self.setLayout(layout)

        # Etiqueta para mostrar el ping en tiempo real
        self.pingLabel = QLabel("Ping: ", self)
        self.pingLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pingLabel)

        # Iniciar el actualizador de ping en un hilo separado
        self.ping_updater = PingUpdater()
        self.ping_updater.ping_updated.connect(self.update_ping_label)
        self.ping_updater_thread = threading.Thread(target=self.ping_updater.start_ping, daemon=True)
        self.ping_updater_thread.start()

        # Mostrar el estado actual de Receive Window Auto Tuning Level
        self.show_status()

    def center(self):
        """Centra la ventana en la pantalla del usuario."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Error al ejecutar el comando: {e}")
            return None

    def activate_antibufferbloat(self):
        output = self.run_command("netsh int tcp set global autotuninglevel=disabled")
        if output:
            self.run_command("ipconfig /flushdns")
            QMessageBox.information(self, "Operación completada", "Anti-BufferBloat activado y caché DNS limpiada.")

    def deactivate_antibufferbloat(self):
        output = self.run_command("netsh int tcp set global autotuninglevel=normal")
        if output:
            QMessageBox.information(self, "Operación completada", "Anti-BufferBloat desactivado.")

    def show_status(self):
        output = self.run_command("netsh interface tcp show global")
        if output:
            lines = output.split('\n')
            rwat_line = [line for line in lines if "Receive Window Auto-Tuning Level" in line]
            if rwat_line:
                self.statusLabel.setText(rwat_line[0])
            else:
                self.statusLabel.setText("Información no encontrada.")

    def open_website(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def update_ping_label(self, ping_value):
        self.pingLabel.setText(ping_value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #36393F; /* Fondo similar a Discord */
            color: #DCDDDE; /* Texto similar a Discord */
        }
        QPushButton {
            background-color: #7289DA; /* Color de botón similar a Discord */
            color: #FFFFFF; /* Texto en botón similar a Discord */
            border-radius: 15px;
            padding: 15px;
            border: 10px;
        }
        QPushButton:hover {
            background-color: #677BC4; /* Cambio de color al pasar el cursor similar a Discord */
        }
        QPushButton:pressed {
            background-color: #5B6EAE; /* Cambio de color al presionar el botón similar a Discord */
        }
        QLabel {
            font-size: 20px; /* Tamaño de fuente aumentado para el título */
            font-weight: bold;
            color: #DCDDDE;
        }
    """)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
