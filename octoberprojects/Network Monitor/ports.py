import sys  # Import sys to handle platform detection
import socket
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QProgressBar

# Class for Port Scan and Telnet
class PortsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # IP input for both Netstat and Telnet
        self.ip_label = QLabel("Enter IP Address:")
        self.ip_input = QLineEdit()

        # Port range input for Netstat
        self.port_range_label = QLabel("Enter Port Range (e.g., 20-80):")
        self.port_range_input = QLineEdit()

        # Netstat button
        self.netstat_button = QPushButton("Run Port Scan")
        self.netstat_button.clicked.connect(self.run_netstat)

        # Telnet input and button
        self.telnet_port_label = QLabel("Enter Port for Telnet:")
        self.telnet_port_input = QLineEdit()
        self.telnet_button = QPushButton("Run Telnet")
        self.telnet_button.clicked.connect(self.run_telnet)

        # Output area
        self.output_area = QTextEdit()

        # Progress bar for port scan
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # Layout setup
        netstat_layout = QHBoxLayout()
        netstat_layout.addWidget(self.port_range_label)
        netstat_layout.addWidget(self.port_range_input)

        telnet_layout = QHBoxLayout()
        telnet_layout.addWidget(self.telnet_port_label)
        telnet_layout.addWidget(self.telnet_port_input)

        self.layout.addWidget(self.ip_label)
        self.layout.addWidget(self.ip_input)
        self.layout.addLayout(netstat_layout)
        self.layout.addWidget(self.netstat_button)
        self.layout.addLayout(telnet_layout)
        self.layout.addWidget(self.telnet_button)
        self.layout.addWidget(self.output_area)
        self.layout.addWidget(self.progress_bar)  # Add the progress bar at the bottom

        self.setLayout(self.layout)

    # Function to perform a real port scan using socket library
    def run_netstat(self):
        ip_address = self.ip_input.text()
        port_range = self.port_range_input.text()

        if not ip_address or not port_range or "-" not in port_range:
            self.output_area.setText("Please enter a valid IP address and port range (e.g., 20-80).")
            return

        start_port, end_port = port_range.split("-")
        try:
            start_port = int(start_port)
            end_port = int(end_port)
        except ValueError:
            self.output_area.setText("Invalid port range. Please enter numbers (e.g., 20-80).")
            return

        # Calculate total number of ports to scan and reset progress bar
        total_ports = end_port - start_port + 1
        self.progress_bar.setValue(0)  # Reset the progress bar
        self.progress_bar.setMaximum(total_ports)  # Set maximum value for the progress bar

        # Clear output area before starting the scan
        self.output_area.clear()
        self.output_area.append(f"Scanning IP: {ip_address} for open ports between {start_port} and {end_port}...\n")

        # Perform real port scan using socket
        for count, port in enumerate(range(start_port, end_port + 1), start=1):
            self.output_area.append(f"Checking port {port}...")
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)  # Set timeout to 1 second for each port
                result = sock.connect_ex((ip_address, port))

                if result == 0:
                    self.output_area.append(f"Port {port}: Open")
                else:
                    self.output_area.append(f"Port {port}: Closed")

                sock.close()
            except socket.error as e:
                self.output_area.append(f"Error checking port {port}: {e}")

            # Update the progress bar after each port is scanned
            self.progress_bar.setValue(count)

    # Function to perform Telnet-like connectivity check using Python's socket library
    def run_telnet(self):
        ip_address = self.ip_input.text()
        port = self.telnet_port_input.text()

        if not ip_address or not port.isdigit():
            self.output_area.setText("Please enter a valid IP address and port number.")
            return

        port = int(port)

        try:
            # Using socket to test the telnet connection
            self.output_area.append(f"Attempting to connect to {ip_address} on port {port}...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # Set timeout to 5 seconds
            result = sock.connect_ex((ip_address, port))

            if result == 0:
                self.output_area.append(f"Connection to {ip_address} on port {port} succeeded.")
            else:
                self.output_area.append(f"Connection to {ip_address} on port {port} failed. Error code: {result}")
            
            # Add a more detailed error message if the connection failed
            if result != 0:
                self.output_area.append(f"Connection attempt resulted in error code {result}. "
                                        "Make sure the IP address and port are reachable, and check for any firewalls or network issues.")
            
            sock.close()
        except socket.error as e:
            self.output_area.append(f"Socket error: {e}")

    def get_state(self):
        # Save the state of the IP address and port info
        return {'ip': self.ip_input.text(), 'port_range': self.port_range_input.text(), 'telnet_port': self.telnet_port_input.text()}

    def load_state(self, state):
        # Load the state of the IP address and port info
        self.ip_input.setText(state['ip'])
        self.port_range_input.setText(state['port_range'])
        self.telnet_port_input.setText(state['telnet_port'])
