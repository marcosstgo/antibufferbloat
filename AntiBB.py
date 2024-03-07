import sys
import subprocess
import re
import requests
import speedtest
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QMessageBox, QLabel, QDialog, QTextEdit, QFileDialog
from PySide6.QtGui import QFont, QDesktopServices, QGuiApplication
from PySide6.QtCore import Qt, QUrl, QThread, Signal

class PingUpdater(QThread):
    ping_updated = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True

    def run(self):
        startupinfo = subprocess.STARTUPINFO() if sys.platform == "win32" else None
        if startupinfo:
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(['ping', '8.8.4.4', '-t'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)
        while self.running:
            line = process.stdout.readline()
            if not line:
                break
            output = line.decode('utf-8').strip()
            ping_time = re.search(r'time=(\d+)ms', output)
            if ping_time:
                self.ping_updated.emit(ping_time.group(1))
        process.kill()

    def stop(self):
        self.running = False

class SpeedTestThread(QThread):
    progress_signal = Signal(str)
    result_signal = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.progress_signal.emit("Iniciando prueba de velocidad...")
        try:
            s = speedtest.Speedtest()
            self.progress_signal.emit("Buscando el mejor servidor...")
            s.get_best_server()
            self.progress_signal.emit("Probando descarga...")
            s.download()
            self.progress_signal.emit("Probando subida...")
            s.upload()
            results_dict = s.results.dict()
            self.progress_signal.emit("Finalizado: D: {:.2f}mb / U: {:.2f}mb".format(results_dict['download'] / 1_000_000, results_dict['upload'] / 1_000_000))
            self.result_signal.emit(results_dict)
        except Exception as e:
            self.progress_signal.emit("Error: {}".format(e))

class InfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Información sobre Auto-Tuning y RSS")
        self.setGeometry(100, 100, 400, 250)
        layout = QVBoxLayout()
        infoText = QTextEdit()
        infoText.setReadOnly(True)
        infoText.setText(
            "Auto-Tuning mejora el rendimiento de la red ajustando dinámicamente el tamaño "
            "del buffer de recepción de TCP según las condiciones de la red.\n\n"
            "RSS (Receive Side Scaling) permite a la tarjeta de red distribuir el procesamiento "
            "de paquetes de red a través de múltiples procesadores, mejorando el rendimiento de red.\n\n"
            "Activar o desactivar estas funciones puede afectar el rendimiento de tu red. "
            "Usa estas opciones con cuidado y según tus necesidades específicas."
        )
        layout.addWidget(infoText)
        self.setLayout(layout)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.version = '2.0'
        self.title = f'Anti-BufferBloat {self.version} - by @m4rcos'
        self.initUI()
    # Otros métodos y definiciones de clase...

    def run_speed_test_cli(self):
        # Aquí se crea la instancia de Speedtest
        s = speedtest.Speedtest()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(500, 350)
        self.center()

        mainLayout = QVBoxLayout()

        self.titleLabel = QLabel("Anti-BufferBloat", self)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("font-size: 20px; font-weight: bold;")
        mainLayout.addWidget(self.titleLabel)

        self.statusLabel = QLabel("Estado: ", self)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setStyleSheet("font-size: 15px;")
        mainLayout.addWidget(self.statusLabel)

        self.pingLabel = QLabel("Ping: ", self)
        self.pingLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.pingLabel)

        self.progressLabel = QLabel("...", self)
        self.progressLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.progressLabel)

        self.setupButtons(mainLayout)

        self.setLayout(mainLayout)

        self.ping_updater = PingUpdater()
        self.ping_updater.ping_updated.connect(self.update_ping_label)
        self.ping_updater.start()

        self.show_status()

    def setupButtons(self, mainLayout):
        autoTuningLayout = QHBoxLayout()
        self.activateButton = QPushButton('Activar Auto-Tuning (Normal)', self)
        self.deactivateButton = QPushButton('Desactivar Auto-Tuning (Recomendado)', self)
        autoTuningLayout.addWidget(self.activateButton)
        autoTuningLayout.addWidget(self.deactivateButton)

        rssLayout = QHBoxLayout()
        self.rssEnableButton = QPushButton('Activar RSS (Recomendado)', self)
        self.rssDisableButton = QPushButton('Desactivar RSS', self)
        rssLayout.addWidget(self.rssEnableButton)
        rssLayout.addWidget(self.rssDisableButton)

        speedTestLayout = QHBoxLayout()
        self.speedtestButton = QPushButton('Speedtest.net', self)
        self.speedTestCliButton = QPushButton('Speedtest-Cli', self)
        speedTestLayout.addWidget(self.speedtestButton)
        speedTestLayout.addWidget(self.speedTestCliButton)

        additionalTestsLayout = QHBoxLayout()
        self.bufferbloatTestButton = QPushButton('Prueba de BufferBloat | Waveform.com', self)
        self.fastButton = QPushButton('Fast.com', self)
        additionalTestsLayout.addWidget(self.bufferbloatTestButton)
        additionalTestsLayout.addWidget(self.fastButton)

        # Nuevo botón para verificar actualizaciones
        updateButtonLayout = QHBoxLayout()
        self.updateButton = QPushButton('Verificar actualizaciones de Anti-BufferBloat', self)
        updateButtonLayout.addWidget(self.updateButton)

        mainLayout.addLayout(autoTuningLayout)
        mainLayout.addLayout(rssLayout)
        mainLayout.addLayout(speedTestLayout)
        mainLayout.addLayout(additionalTestsLayout)
        mainLayout.addLayout(updateButtonLayout)  # Agregar el nuevo botón

        self.exitButton = QPushButton('Salir', self)
        mainLayout.addWidget(self.exitButton)

        self.infoButton = QPushButton('Información sobre Auto-Tuning y RSS', self)
        mainLayout.addWidget(self.infoButton)

        # Connect buttons to their respective functions
        self.activateButton.clicked.connect(lambda: self.toggle_feature(True, "autotuninglevel"))
        self.deactivateButton.clicked.connect(lambda: self.toggle_feature(False, "autotuninglevel"))
        self.rssEnableButton.clicked.connect(lambda: self.toggle_feature(True, "rss"))
        self.rssDisableButton.clicked.connect(lambda: self.toggle_feature(False, "rss"))
        self.speedtestButton.clicked.connect(lambda: self.open_website("https://www.speedtest.net"))
        self.speedTestCliButton.clicked.connect(self.run_speed_test_cli)
        self.bufferbloatTestButton.clicked.connect(lambda: self.open_website("https://www.waveform.com/tools/bufferbloat"))
        self.fastButton.clicked.connect(lambda: self.open_website("https://www.fast.com"))
        self.updateButton.clicked.connect(self.check_update)  # Conectar el nuevo botón a la función de verificación de actualizaciones
        self.exitButton.clicked.connect(self.close)
        self.infoButton.clicked.connect(self.show_info_dialog)

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def toggle_feature(self, enable, feature):
        if feature == "autotuninglevel":
            command = "netsh int tcp set global autotuninglevel=normal" if enable else "netsh int tcp set global autotuninglevel=disabled"
            action = "activado" if enable else "desactivado"
            feature_name = "Auto-Tuning"
        elif feature == "rss":
            command = "netsh int tcp set global rss=enabled" if enable else "netsh int tcp set global rss=disabled"
            action = "activado" if enable else "desactivado"
            feature_name = "RSS"
        result = self.run_command(command)
        if "OK" in result:
            self.show_success_message(f"{feature_name} ha sido {action}.")
            self.run_command("ipconfig /flushdns")  # Flush DNS as a precaution
        else:
            QMessageBox.information(self, "Mensaje", f"Se aplico el cambio del {feature_name}.")
        self.show_status()

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout.strip()  # Remove .decode()
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"

    def show_status(self):
        output = self.run_command("netsh int tcp show global")
        autotuning_status = "Receive Window Auto-Tuning Level not found."
        rss_status = "Receive-Side Scaling State not found."

        # Buscando las cadenas correctas en inglés
        for line in output.split('\n'):
            if "Receive Window Auto-Tuning Level" in line:
                autotuning_status = line.strip()
            elif "Receive-Side Scaling State" in line:
                rss_status = line.strip()

        # Actualizar la etiqueta de estado con la información encontrada
        self.statusLabel.setText(f"{autotuning_status}\n{rss_status}")

    def open_website(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def update_ping_label(self, ping_value):
        self.pingLabel.setText(f"Ping: {ping_value}ms")

    def closeEvent(self, event):
        self.ping_updater.running = False
        self.ping_updater.wait()  # Espera a que el hilo termine
        event.accept()

    def run_speed_test_cli(self):
        self.test_thread = SpeedTestThread()
        self.test_thread.progress_signal.connect(self.update_progress_label)
        self.test_thread.result_signal.connect(self.show_speed_test_results)
        self.test_thread.start()

    def update_progress_label(self, message):
        self.progressLabel.setText(message)

    def show_speed_test_results(self, results):
        download_speed = results["download"] / 1_000_000  # Convert to Mbps
        upload_speed = results["upload"] / 1_000_000  # Convert to Mbps
        self.show_success_message(f"Descarga: {download_speed:.2f} Mbps\nSubida: {upload_speed:.2f} Mbps\nPing: {results['ping']} ms")

    def show_info_dialog(self):
        dialog = InfoDialog(self)
        dialog.exec_()

    def show_success_message(self, message):
        """
        Muestra un mensaje de éxito en la aplicación.

        Args:
            message (str): Mensaje a mostrar.
        """
        QMessageBox.information(self, "Éxito", message)

    def check_update(self):
            try:
                response = requests.get('https://raw.githubusercontent.com/marcosstgo/antibufferbloat/main/update_info.json')
                if response.status_code == 200:
                    latest_version = response.json()['version']
                    if latest_version != self.version:
                        reply = QMessageBox.question(self, "Actualización disponible", f"Versión {latest_version} disponible para descargar. ¿Desea actualizar ahora?",
                                                    QMessageBox.Yes | QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            download_url = response.json()['download_url']
                            save_path, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "archivo_nuevo.exe", "Ejecutable (*.exe)")
                            if save_path:
                                urlretrieve(download_url, save_path)
                                QMessageBox.information(self, "Descarga completa", "La actualización se ha descargado correctamente.")
                    else:
                        QMessageBox.information(self, "Sin actualizaciones", "Estás utilizando la versión más reciente.")
                else:
                    QMessageBox.warning(self, "Error", "No se pudo verificar las actualizaciones. Código de estado HTTP no válido.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al verificar actualizaciones: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
    QWidget {
        background-color: #000000;
        color: #FFFFFF;
    }
    QPushButton {
        background-color: #7289DA;
        color: #FFFFFF;
        border-radius: 5px;
        padding: 10px;
        margin: 2px;
        border: none;
    }
    QPushButton:hover {
        background-color: #677BC4;
    }
    QPushButton:pressed {
        background-color: #5B6EAE;
    }
    QLabel {
        font-size: 15px;
    }
    QLabel#titleLabel {
        font-size: 20px;
        font-weight: bold;
    }
    """)
    ex = App()
    ex.show()
    sys.exit(app.exec())
