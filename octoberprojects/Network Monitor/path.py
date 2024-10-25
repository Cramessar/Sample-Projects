import sys
import subprocess
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal

# Thread for Trace Route and MTR (or Pathping on Windows)
class PathCommandThread(QThread):
    result = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, ip_address, command_type):
        super().__init__()
        self.ip_address = ip_address
        self.command_type = command_type

    def run(self):
        if self.command_type == "traceroute":
            command = ["tracert", self.ip_address] if sys.platform == "win32" else ["traceroute", self.ip_address]
        elif self.command_type == "mtr":
            # Use pathping on Windows as a substitute for mtr
            if sys.platform == "win32":
                command = ["pathping", self.ip_address]
            else:
                command = ["mtr", "--report", self.ip_address]

        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    self.result.emit(output.strip())

            process.stdout.close()
        except subprocess.CalledProcessError as e:
            self.result.emit(f"Error: {e}")
        except FileNotFoundError:
            self.result.emit(f"Error: Command '{self.command_type}' not found. Please ensure it is installed.")

# Class for Path Tab (Trace Route and MTR/Pathping)
class PathTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # IP input field
        self.ip_label = QLabel("Enter IP Address:")
        self.ip_input = QLineEdit()

        # Trace Route button
        self.traceroute_button = QPushButton("Run Trace Route")
        self.traceroute_button.clicked.connect(self.run_traceroute)

        # MTR/Pathping button
        self.mtr_button = QPushButton("Run MTR (Pathping on Windows)")
        self.mtr_button.clicked.connect(self.run_mtr)

        # Output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # Layout setup
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.ip_label)
        input_layout.addWidget(self.ip_input)

        self.layout.addLayout(input_layout)
        self.layout.addWidget(self.traceroute_button)
        self.layout.addWidget(self.mtr_button)
        self.layout.addWidget(self.output_area)
        self.layout.addWidget(self.progress_bar)  # Progress bar at the bottom

        self.setLayout(self.layout)

    def run_traceroute(self):
        ip_address = self.ip_input.text()
        if not ip_address:
            self.output_area.setText("Please enter a valid IP address.")
            return

        # Clear output and reset progress
        self.output_area.clear()
        self.progress_bar.setValue(0)

        # Run trace route in a separate thread
        self.path_thread = PathCommandThread(ip_address, "traceroute")
        self.path_thread.result.connect(self.display_result)
        self.path_thread.progress.connect(self.update_progress)
        self.path_thread.start()

    def run_mtr(self):
        ip_address = self.ip_input.text()
        if not ip_address:
            self.output_area.setText("Please enter a valid IP address.")
            return

        # Clear output and reset progress
        self.output_area.clear()
        self.progress_bar.setValue(0)

        # Run MTR/Pathping in a separate thread
        self.path_thread = PathCommandThread(ip_address, "mtr")
        self.path_thread.result.connect(self.display_result)
        self.path_thread.progress.connect(self.update_progress)
        self.path_thread.start()

    def display_result(self, result):
        self.output_area.append(result)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def get_state(self):
        # Save the state of the IP input
        return {'ip': self.ip_input.text()}

    def load_state(self, state):
        # Load the state of the IP input
        self.ip_input.setText(state.get('ip', ''))
