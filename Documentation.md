# Python TCP/UDP Port Scanner - Enhanced Edition Documentation
**Date:** November 26, 2025
**Version:** 2.0.0
**Author:** Cybersecurity Instructor (AI Assistant)

---

## 1. Executive Summary
This project implements a high-performance, multi-threaded TCP/UDP port scanner with both CLI and GUI interfaces. It is designed for security professionals and system administrators to audit network perimeters, identify open services, verify firewall configurations, and perform comprehensive network reconnaissance. The enhanced edition includes UDP scanning, service identification, multiple export formats (CSV/JSON), stealth modes, and a modern graphical interface.

## 2. Ethical & Legal Compliance
**CRITICAL WARNING:**
Port scanning is classified as active reconnaissance. It generates network traffic that is easily detected by Intrusion Detection Systems (IDS).

*   **Permission:** Do NOT scan networks you do not own or have explicit written consent to test.
*   **Legality:** Unauthorized scanning may violate the Computer Fraud and Abuse Act (CFAA) and other international cyber laws.
*   **Liability:** The user assumes all liability for the use of this tool.

---

## 3. Technical Architecture

### 3.1 Core Components

#### Scanner Engine
*   **TCP Socket Engine:** Uses Python's native `socket` library with `SOCK_STREAM` for TCP connections
*   **UDP Socket Engine:** Implements `SOCK_DGRAM` for UDP scanning with protocol-specific probes
*   **Concurrency Model:** `concurrent.futures.ThreadPoolExecutor` manages worker threads (default: 200, configurable up to 1000+)
*   **Progress Tracking:** Integration with `tqdm` for real-time progress visualization
*   **Logging System:** Dual-handler system (file + console) with timestamped audit logs

#### Service Identification
*   **Known Services:** Built-in database of common port-to-service mappings
*   **System Integration:** Uses `socket.getservbyport()` for system service database
*   **Banner Analysis:** Parses service banners to identify software versions
*   **Protocol Probes:** Custom UDP probes for DNS, NTP, SNMP, and other services

#### GUI Framework
*   **Tkinter Base:** Cross-platform GUI using Python's built-in tkinter
*   **ttkbootstrap Styling:** Modern dark theme with professional appearance
*   **Threading:** Separate thread for scanning to prevent UI freezing
*   **Real-time Updates:** Live result table updates using `root.after()`

### 3.2 Key Functions

#### Core Scanning
*   `scan_port(ip, port, timeout, stealth)`: TCP handshake with optional stealth delays. Returns (port, status, banner, service)
*   `scan_udp_port(ip, port, timeout)`: UDP probe with protocol-specific payloads. Returns (port, status, response, service)
*   `identify_service(port, banner)`: Multi-layer service identification using port number and banner analysis

#### Utility Functions
*   `parse_ports(port_arg)`: Robust parser handling ranges (`1-100`), lists (`80,443`), and mixed formats
*   `setup_logging(log_file_path, silent)`: Configures logging with automatic directory creation
*   `export_json(results, output_file, target, target_ip)`: Structured JSON export with metadata

#### Stealth Features
*   Random delays between connections (0.1-0.5 seconds)
*   Configurable timeout for adaptive scanning
*   Silent mode for log-only operation

---

## 4. Usage Guide

### 4.1 Installation
No external dependencies are required. The tool uses the Python Standard Library.
```bash
# Verify Python version
python3 --version
```

### 4.2 Command Reference
| Argument | Description | Default |
| :--- | :--- | :--- |
| `target` | Target IP or Hostname | Required |
| `-p, --ports` | Ports to scan (e.g., `80`, `1-100`) | `1-1024` |
| `-t, --threads` | Number of concurrent threads | `200` |
| `--output-csv` | Path to save CSV report | None |
| `--silent` | Suppress console output | `False` |
| `-v, --verbose` | Show closed/timeout ports | `False` |

### 4.3 Examples
**Scenario A: Quick Web Audit**
```bash
python3 scanner.py example.com -p 80,443,8080,8443
```

**Scenario B: Full Subnet Scan (Slow)**
```bash
python3 scanner.py 192.168.1.5 -p 1-65535 -t 1000 --output-csv full_scan.csv
```

---

## 5. Output Analysis
The tool produces two types of artifacts:

1.  **Log Files (`logs/scan_*.log`):**
    ```text
    2025-11-23 10:55:01 - INFO - Port 22: OPEN | Banner: SSH-2.0-OpenSSH_8.2p1
    ```

2.  **CSV Report:**
    | timestamp | target | resolved_ip | port | status | banner |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    | 2025-11-23T10:55:01 | localhost | 127.0.0.1 | 22 | OPEN | SSH-2.0... |

---

## 6. New Features in v2.0

### UDP Scanning
*   Full UDP support with protocol-specific probes
*   Handles UDP's stateless nature (OPEN|FILTERED status)
*   Custom payloads for DNS, NTP, SNMP services

### Service Identification
*   Automatic service detection on all open ports
*   Banner grabbing with intelligent parsing
*   Integration with system service database
*   Version fingerprinting from banners

### Multiple Output Formats
*   **JSON:** Structured data with metadata and results array
*   **CSV:** Spreadsheet-compatible format with all fields
*   **Console:** Color-coded real-time output
*   **Logs:** Timestamped audit trail

### Graphical User Interface
*   Modern dark theme with ttkbootstrap
*   Real-time result updates during scanning
*   Sortable result table (click column headers)
*   One-click export to CSV/JSON
*   Progress tracking with visual feedback
*   Configurable scan parameters

### Stealth Mode
*   Random delays between connections
*   Reduces IDS detection probability
*   Configurable timing parameters

### Progress Tracking
*   Real-time progress bars (tqdm)
*   Completion percentage
*   Open port count during scan
*   Estimated time remaining

## 7. Testing

Comprehensive test suite with:
*   **Unit Tests:** Port parsing, service identification, individual scan functions
*   **Mock Tests:** Socket operations with various scenarios (open/closed/timeout)
*   **Integration Tests:** Full scan workflows on localhost
*   **Coverage:** >80% code coverage target

Run tests:
```bash
python -m pytest tests/ -v --cov=scanner
```

## 8. Installation & Packaging

### Package Structure
*   `setup.py`: Standard Python package configuration
*   Entry points: `port-scanner` (CLI), `port-scanner-gui` (GUI)
*   Dependencies: tqdm, ttkbootstrap
*   Python 3.7+ required

### Installation Methods
```bash
# Development mode
pip install -e .

# Standard installation
pip install .

# From requirements
pip install -r requirements.txt
```

## 9. Future Roadmap
*   **OS Fingerprinting:** Analyze TCP window size, TTL, and TCP options
*   **Vulnerability Mapping:** Integrate with CVE databases based on service versions
*   **Nmap XML Export:** Compatible output format for integration with other tools
*   **Distributed Scanning:** Coordinate scans across multiple hosts
*   **Web Dashboard:** Browser-based interface for remote scanning
*   **Custom Plugins:** Extensible architecture for custom service probes

---
*End of Documentation*
