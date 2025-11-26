# 🛡️ Python TCP/UDP Port Scanner - Enhanced Edition

A professional, multi-threaded TCP/UDP port scanner with GUI built in Python. Designed for network reconnaissance and security auditing.

## 📂 Project Structure

```text
Python TCP Port Scanner – Full Project Build/
├── scanner.py          # Enhanced CLI scanner (TCP/UDP)
├── gui_scanner.py      # Modern GUI application
├── setup.py            # Package installation script
├── config.json         # Configuration and port lists
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── Documentation.md    # Technical documentation
├── INSTALL.md          # Installation guide
├── FINAL_REPORT.md     # Original project report
├── tests/              # Test suite
│   ├── __init__.py
│   └── test_scanner.py
├── logs/               # Scan logs directory
└── venv/               # Virtual environment
```

## ✨ Features

### Core Scanning
*   **TCP & UDP Scanning:** Full support for both protocols
*   **Multi-threaded:** Scans hundreds of ports concurrently (configurable)
*   **Service Identification:** Automatically identifies services on open ports
*   **Banner Grabbing:** Captures service banners for fingerprinting
*   **Stealth Mode:** Random delays to evade detection

### Output & Reporting
*   **Multiple Formats:** Console, CSV, and JSON export
*   **Detailed Logging:** Automatic timestamped log files
*   **Progress Tracking:** Real-time progress bars (tqdm)
*   **Verbose Mode:** Show all ports including closed/filtered

### User Interface
*   **CLI:** Powerful command-line interface with extensive options
*   **GUI:** Modern graphical interface with ttkbootstrap styling
*   **Real-time Results:** Live updates during scanning
*   **Sortable Tables:** Click column headers to sort results

## 🚀 Quick Start

### Installation

```bash
# Navigate to project directory
cd "/Users/yash/Documents/Python TCP Port Scanner – Full Project Build"

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Optional: Install as package
pip install -e .
```

For detailed installation instructions, see [INSTALL.md](INSTALL.md).

### Basic Usage

#### Command Line Interface

```bash
# Basic TCP scan
python3 scanner.py google.com -p 80,443

# UDP scan
python3 scanner.py 8.8.8.8 --udp -p 53,123

# Both TCP and UDP
python3 scanner.py example.com --both -p 20-25,80,443

# Full scan with all features
python3 scanner.py 192.168.1.1 -p 1-1000 -t 500 --stealth --output-json results.json

# Verbose mode with CSV export
python3 scanner.py localhost -p 1-100 -v --output-csv scan.csv
```

#### Graphical User Interface

```bash
# Launch GUI
python3 gui_scanner.py

# Or if installed as package
port-scanner-gui
```

## 📖 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `target` | Target IP or hostname | Required |
| `-p, --ports` | Ports to scan (e.g., `80`, `1-100`, `22,80,443`) | `1-1024` |
| `--tcp` | Perform TCP scan | `True` |
| `--udp` | Perform UDP scan | `False` |
| `--both` | Perform both TCP and UDP | `False` |
| `-t, --threads` | Number of concurrent threads | `200` |
| `--timeout` | Socket timeout in seconds | `1.0` |
| `--stealth` | Enable stealth mode (random delays) | `False` |
| `--output-csv` | Export results to CSV file | None |
| `--output-json` | Export results to JSON file | None |
| `--silent` | Suppress console output | `False` |
| `-v, --verbose` | Show closed/filtered ports | `False` |
| `--no-progress` | Disable progress bar | `False` |
| `--log` | Custom log file path | Auto-generated |

## 💡 Usage Examples

### Scenario 1: Web Server Audit
```bash
python3 scanner.py example.com -p 80,443,8080,8443
```

### Scenario 2: Database Server Check
```bash
python3 scanner.py db.example.com -p 3306,5432,27017,6379
```

### Scenario 3: Full Network Scan (Slow)
```bash
python3 scanner.py 192.168.1.1 -p 1-65535 -t 1000 --output-csv full_scan.csv
```

### Scenario 4: Stealth Reconnaissance
```bash
python3 scanner.py target.com -p 1-1000 --stealth --silent --output-json stealth_scan.json
```

### Scenario 5: DNS Server Check (UDP)
```bash
sudo python3 scanner.py 8.8.8.8 --udp -p 53
```

## 🎨 GUI Features

The graphical interface provides:
- **Easy Configuration:** Point-and-click target and port selection
- **Real-time Results:** Live table updates as ports are scanned
- **Export Options:** One-click CSV/JSON export
- **Progress Tracking:** Visual progress bar and statistics
- **Sortable Results:** Click column headers to sort
- **Modern Design:** Dark theme with ttkbootstrap styling

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=scanner --cov-report=html

# Run specific test
python -m unittest tests.test_scanner.TestPortParsing
```

## 📊 Output Formats

### Console Output
```
2025-11-26 22:30:00 - INFO - Starting TCP scan on host: google.com (142.250.193.206)
2025-11-26 22:30:00 - INFO - Port 80/TCP: OPEN | Service: HTTP
2025-11-26 22:30:00 - INFO - Port 443/TCP: OPEN | Service: HTTPS
```

### JSON Output
```json
{
  "scan_metadata": {
    "target": "google.com",
    "resolved_ip": "142.250.193.206",
    "timestamp": "2025-11-26T22:30:00",
    "total_ports_scanned": 2,
    "open_ports_count": 2
  },
  "results": [
    {
      "port": 80,
      "protocol": "TCP",
      "status": "OPEN",
      "service": "HTTP",
      "banner": "HTTP/1.0 200 OK"
    }
  ]
}
```

### CSV Output
```csv
timestamp,target,resolved_ip,port,protocol,status,service,banner
2025-11-26T22:30:00,google.com,142.250.193.206,80,TCP,OPEN,HTTP,HTTP/1.0 200 OK
```

## ⚠️ Legal Disclaimer

**CRITICAL WARNING:** Port scanning is classified as active reconnaissance and may be illegal without authorization.

*   **Permission Required:** Only scan networks you own or have explicit written permission to test
*   **Legal Risks:** Unauthorized scanning may violate laws such as:
    - Computer Fraud and Abuse Act (CFAA) in the US
    - Computer Misuse Act in the UK
    - Similar cyber laws internationally
*   **Detection:** Port scans are easily detected by Intrusion Detection Systems (IDS)
*   **Liability:** You are solely responsible for your actions

**Use this tool responsibly to secure your own infrastructure.**

## 🔧 Troubleshooting

- **"Permission denied" for UDP:** Use `sudo` on macOS/Linux or run as Administrator on Windows
- **GUI won't start:** Ensure tkinter is installed (`python3 -c "import tkinter"`)
- **Slow scans:** Increase thread count with `-t 500` or higher
- **No progress bar:** Install tqdm (`pip install tqdm`)

## 📚 Documentation

- [INSTALL.md](INSTALL.md) - Detailed installation instructions
- [Documentation.md](Documentation.md) - Technical architecture and details
- [FINAL_REPORT.md](FINAL_REPORT.md) - Original project report

## 🚀 Future Enhancements

- OS fingerprinting via TCP/IP stack analysis
- Integration with CVE databases for vulnerability mapping
- Nmap XML output format support
- Distributed scanning across multiple hosts
- Web-based dashboard

## 📄 License

This project is for educational purposes only. Use at your own risk.

---

**Version:** 2.0.0  
**Last Updated:** 2025-11-26
