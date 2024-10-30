import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from ping import PingTab  # Import PingTab class from ping.py
from ports import PortsTab  # Import PortsTab class from ports.py
from routes import RoutesTab  # Import RoutesTab class from routes.py
from path import PathTab  # Import PathTab class from path.py

class NetworkAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Network Analysis App")
        self.setGeometry(100, 100, 1280, 800)

        # Create the tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Initialize each tab
        self.ping_tab = PingTab()  # PingTab for Ping functionality
        self.ports_tab = PortsTab()  # PortsTab for Port Scan and Telnet
        self.routes_tab = RoutesTab()  # RoutesTab for route-related functionality
        self.path_tab = PathTab()  # PathTab for Trace Route and MTR

        # Add tabs to the QTabWidget
        self.tab_widget.addTab(self.ping_tab, "Connectivity (Ping)")
        self.tab_widget.addTab(self.ports_tab, "Ports")
        self.tab_widget.addTab(self.routes_tab, "Routes")
        self.tab_widget.addTab(self.path_tab, "Path")  # Add the new Path tab

        # Connect the tab change signal to the save/load state mechanism
        self.tab_widget.currentChanged.connect(self.on_tab_change)

        # Store state of the tabs
        self.tab_states = {}

    def on_tab_change(self, index):
        # Save the state of the previous tab
        current_tab = self.tab_widget.widget(index)
        previous_tab = self.tab_widget.widget(self.tab_widget.currentIndex())

        if previous_tab == self.ping_tab:
            self.tab_states['ping'] = self.ping_tab.get_state()
        elif previous_tab == self.ports_tab:
            self.tab_states['ports'] = self.ports_tab.get_state()
        elif previous_tab == self.routes_tab:
            self.tab_states['routes'] = self.routes_tab.get_state()
        elif previous_tab == self.path_tab:
            self.tab_states['path'] = self.path_tab.get_state()

        # Load the state of the new tab
        if current_tab == self.ping_tab and 'ping' in self.tab_states:
            self.ping_tab.load_state(self.tab_states['ping'])
        elif current_tab == self.ports_tab and 'ports' in self.tab_states:
            self.ports_tab.load_state(self.tab_states['ports'])
        elif current_tab == self.routes_tab and 'routes' in self.tab_states:
            self.routes_tab.load_state(self.tab_states['routes'])
        elif current_tab == self.path_tab and 'path' in self.tab_states:
            self.path_tab.load_state(self.tab_states['path'])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetworkAnalysisApp()
    window.show()
    sys.exit(app.exec_())
