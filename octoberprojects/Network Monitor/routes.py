import sys
import subprocess
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QProgressBar

class RoutesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Route Print button
        self.route_print_button = QPushButton("Print Routing Table")
        self.route_print_button.clicked.connect(self.route_print)

        # Find route input and button
        self.find_route_label = QLabel("Enter IP to Find Route:")
        self.find_route_input = QLineEdit()
        self.find_route_button = QPushButton("Find Route")
        self.find_route_button.clicked.connect(self.find_route)

        # Add route inputs and button
        self.add_route_label = QLabel("Enter Destination IP to Add:")
        self.add_route_input = QLineEdit()
        self.add_gateway_label = QLabel("Enter Gateway IP:")
        self.add_gateway_input = QLineEdit()
        self.add_route_button = QPushButton("Add Route")
        self.add_route_button.clicked.connect(self.add_route)

        # Delete route input and button
        self.delete_route_label = QLabel("Enter Destination IP to Delete:")
        self.delete_route_input = QLineEdit()
        self.delete_route_button = QPushButton("Delete Route")
        self.delete_route_button.clicked.connect(self.delete_route)

        # Output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # Layout setup
        self.layout.addWidget(self.route_print_button)
        self.layout.addWidget(self.find_route_label)
        self.layout.addWidget(self.find_route_input)
        self.layout.addWidget(self.find_route_button)
        self.layout.addWidget(self.add_route_label)
        self.layout.addWidget(self.add_route_input)
        self.layout.addWidget(self.add_gateway_label)
        self.layout.addWidget(self.add_gateway_input)
        self.layout.addWidget(self.add_route_button)
        self.layout.addWidget(self.delete_route_label)
        self.layout.addWidget(self.delete_route_input)
        self.layout.addWidget(self.delete_route_button)
        self.layout.addWidget(self.output_area)
        self.layout.addWidget(self.progress_bar)  # Add progress bar at the bottom

        self.setLayout(self.layout)

    def route_print(self):
        """Print the current routing table."""
        self.progress_bar.setValue(0)  # Reset progress bar
        try:
            command = ["route", "print"] if sys.platform == "win32" else ["ip", "route"]
            output = subprocess.check_output(command, universal_newlines=True)
            self.output_area.setText(output)
            self.progress_bar.setValue(100)  # Set progress to 100% after completion
        except subprocess.CalledProcessError as e:
            self.output_area.setText(f"Error printing routes: {e}")
            self.progress_bar.setValue(100)  # Even on error, complete the progress

    def find_route(self):
        """Find the route for a specific IP."""
        self.progress_bar.setValue(0)  # Reset progress bar
        ip_address = self.find_route_input.text()
        if not ip_address:
            self.output_area.setText("Please enter a valid IP address.")
            self.progress_bar.setValue(100)
            return

        try:
            command = ["route", "print", ip_address] if sys.platform == "win32" else ["ip", "route", "get", ip_address]
            output = subprocess.check_output(command, universal_newlines=True)
            self.output_area.setText(output)
            self.progress_bar.setValue(100)  # Set progress to 100% after completion
        except subprocess.CalledProcessError as e:
            self.output_area.setText(f"Error finding route for {ip_address}: {e}")
            self.progress_bar.setValue(100)

    def add_route(self):
        """Add a route for a specific destination IP."""
        self.progress_bar.setValue(0)  # Reset progress bar
        destination_ip = self.add_route_input.text()
        gateway_ip = self.add_gateway_input.text()
        if not destination_ip or not gateway_ip:
            self.output_area.setText("Please enter both destination IP and gateway IP.")
            self.progress_bar.setValue(100)
            return

        try:
            command = ["route", "add", destination_ip, gateway_ip] if sys.platform == "win32" else ["ip", "route", "add", destination_ip, "via", gateway_ip]
            subprocess.check_output(command, universal_newlines=True)
            self.output_area.setText(f"Route added for {destination_ip} via {gateway_ip}.")
            self.progress_bar.setValue(100)
        except subprocess.CalledProcessError as e:
            self.output_area.setText(f"Error adding route for {destination_ip}: {e}")
            self.progress_bar.setValue(100)

    def delete_route(self):
        """Delete a route for a specific destination IP."""
        self.progress_bar.setValue(0)  # Reset progress bar
        destination_ip = self.delete_route_input.text()
        if not destination_ip:
            self.output_area.setText("Please enter a valid destination IP.")
            self.progress_bar.setValue(100)
            return

        try:
            command = ["route", "delete", destination_ip] if sys.platform == "win32" else ["ip", "route", "del", destination_ip]
            subprocess.check_output(command, universal_newlines=True)
            self.output_area.setText(f"Route deleted for {destination_ip}.")
            self.progress_bar.setValue(100)
        except subprocess.CalledProcessError as e:
            self.output_area.setText(f"Error deleting route for {destination_ip}: {e}")
            self.progress_bar.setValue(100)

    def get_state(self):
        # Save the state of input fields
        return {
            'find_route': self.find_route_input.text(),
            'add_route': self.add_route_input.text(),
            'add_gateway': self.add_gateway_input.text(),
            'delete_route': self.delete_route_input.text()
        }

    def load_state(self, state):
        # Load the state of input fields
        self.find_route_input.setText(state.get('find_route', ''))
        self.add_route_input.setText(state.get('add_route', ''))
        self.add_gateway_input.setText(state.get('add_gateway', ''))
        self.delete_route_input.setText(state.get('delete_route', ''))
