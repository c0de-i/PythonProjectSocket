Port Scanner by Code_I

This Python script is a simple port scanner that allows you to scan for open ports on a given host or range of hosts.
Usage

    1. Ensure you have Python 3 installed on your system.

    2. Clone the repository or download the portscanner.py file.

    3. Open a terminal or command prompt and navigate to the directory where port_scanner.py is located.

    4. Run the script using the following command format:

bash

    python port_scanner.py <host> [--ports PORTS] [--mode MODE]

Replace <host> with the target IP address, IP range, or hostname you want to scan.

Optional arguments:

    --ports PORTS: Specify a comma-separated list of ports to scan. If not provided, the script will default to scanning common ports based on the chosen mode.
    --mode MODE: Specify the scanning mode:
        1: Scan ports 1-1024.
        2: Scan common ports (20, 21, 22, 23, 25, 53, 80, 110, 123, 137, 143, 161, 162, 443, 3306).
        3: Scan a custom range of ports (user input required).
        4: Scan specific ports (user input required).

Example usage:

bash

    python port_scanner.py 192.168.1.1 --ports 80,443 --mode 3

The script will then proceed to scan the specified ports on the target host(s) and display the results.

Dependencies
    Python 3
    pyfiglet
    argparse
    ipaddress