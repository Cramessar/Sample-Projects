# Network Analysis Tool

## Overview
This project is a **Network Analysis Tool** designed to help users perform common network tasks such as pinging IP addresses, scanning ports, viewing routes, and tracing paths. It is a simple and free-to-use desktop application, built as a **working prototype** and **proof of concept**.

The app features four key functionalities:
1. **Connectivity (Ping)**: Enter an IP address and number of pings to check connectivity.
2. **Ports**: Scan a range of ports on a given IP address and test Telnet connections.
3. **Routes**: View and manage routes, including printing the routing table, adding, finding, and deleting specific routes.
4. **Path**: Perform trace routes and run MTR to analyze network paths.

## Installation
To run the application, download the standalone executable from the `dist/` directory, or follow the instructions below to build the application from source.

### Build from Source
If you want to build the application yourself, follow these steps:
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Cramessar/Sample-Projects/tree/main/octoberprojects/Network%20Monitor
   cd sample-projects
   ```

2. **Install dependencies**:
   Ensure you have Python and PyQt5 installed. You can install PyQt5 using:
   ```bash
   pip install PyQt5
   ```

3. **Run the app**:
   Simply run `main.py`:
   ```bash
   python main.py
   ```

4. **Build the standalone executable** (Optional):
   To create a standalone executable using PyInstaller, run:
   ```bash
   pyinstaller --onefile --noconsole --add-data "octoberprojects/Network Monitor/ping.py;." --add-data "octoberprojects/Network Monitor/ports.py;." --add-data "octoberprojects/Network Monitor/routes.py;." --add-data "octoberprojects/Network Monitor/path.py;." "octoberprojects/Network Monitor/main.py"
   ```

   The executable will be located in the `dist/` directory.

## Features
- **Ping**: Test connectivity to a specified IP address.
- **Port Scanning**: Scan a range of ports and test Telnet connections.
- **Route Management**: View, find, add, and delete routes in the routing table.
- **Trace Route and MTR**: Trace the network path and run MTR for detailed analysis.

## License and Contribution
This project is free to use, and contributions are **strongly encouraged**. Feel free to make any changes, enhancements, or submit recommendations. This tool is provided as a **working prototype** and can be expanded upon to suit various use cases.

We welcome feedback and pull requests to improve the tool and make it more robust.

## Contact
For suggestions or issues, please open an issue on GitHub or submit a pull request.
