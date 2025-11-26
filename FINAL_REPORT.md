# Python TCP Port Scanner - Final Project Report

# Python TCP Port Scanner - Final Project Report

## ⚠️ Ethical Usage & Legal Disclaimer
**STOP AND READ:** Port scanning is an active reconnaissance technique.
-   **Authorized Use Only:** Only scan networks you own or have explicit written permission to test.
-   **Legal Risks:** Unauthorized scanning can violate laws like the Computer Fraud and Abuse Act (CFAA) in the US or similar laws globally.
-   **Responsibility:** You are solely responsible for your actions. Use this tool to learn and secure your own infrastructure.

## 1. Final Python Code
The complete, fully commented source code is available in `scanner.py`.

## 2. Component Explanation

### **A. Logging Setup (`setup_logging`)**
-   **Purpose:** Handles output to both the console and a file.
-   **Logic:**
    -   Creates a `logs/` directory if it doesn't exist.
    -   Generates a timestamped filename (e.g., `scan_20251123_104500.log`).
    -   Configures `logging.basicConfig` with a `FileHandler` and an optional `StreamHandler` (controlled by `--silent`).

### **B. Port Scanning (`scan_port`)**
-   **Purpose:** The core worker function that checks a single port.
-   **Logic:**
    -   Uses `socket.socket` with `AF_INET` (IPv4) and `SOCK_STREAM` (TCP).
    -   Sets a timeout to prevent hanging.
    -   Uses `connect_ex()`: Returns `0` if successful (Open), otherwise an error code (Closed).
    -   **Banner Grabbing:** If open, sends a `HEAD / HTTP/1.0` request to elicit a response from web servers and reads 1024 bytes.

### **C. Port Parsing (`parse_ports`)**
-   **Purpose:** Converts user input strings into a list of integers.
-   **Logic:**
    -   Splits by comma (`,`).
    -   Detects ranges (`-`) and expands them using `range()`.
    -   Returns a sorted, unique list of ports.

### **D. Main Execution (`main`)**
-   **Purpose:** Orchestrates the program.
-   **Logic:**
    -   **Argparse:** Defines CLI flags (`--ports`, `--threads`, `--csv`, etc.).
    -   **DNS Resolution:** Converts hostname to IP.
    -   **Concurrency:** Uses `ThreadPoolExecutor` to run `scan_port` in parallel threads (default 200).
    -   **CSV Export:** Writes results row-by-row if requested.
    -   **Error Handling:** Catches `KeyboardInterrupt` for clean `Ctrl+C` exit.

## 3. Example Terminal Outputs

### **Basic Scan**
```bash
$ python3 scanner.py google.com -p 80,443
2025-11-23 10:50:00 - INFO - Starting scan on host: google.com (142.250.193.206)
2025-11-23 10:50:00 - INFO - Scanning 2 ports with 200 threads...
2025-11-23 10:50:00 - INFO - Port 80: OPEN | Banner: HTTP/1.0 200 OK
2025-11-23 10:50:00 - INFO - Port 443: OPEN
2025-11-23 10:50:00 - INFO - Scan completed in 0.15 seconds.
```

### **Verbose Scan (Showing Closed Ports)**
```bash
$ python3 scanner.py localhost -p 80-82 -v
...
2025-11-23 10:50:00 - INFO - Port 80: OPEN
2025-11-23 10:50:00 - INFO - Port 81: CLOSED
2025-11-23 10:50:00 - INFO - Port 82: CLOSED
...
```

## 4. Instructions to Run

1.  **Open Terminal** and navigate to the project folder:
    ```bash
    cd "/Users/yash/Documents/Python TCP Port Scanner – Full Project Build"
    ```

2.  **Run the script** (Python 3 required):
    ```bash
    python3 scanner.py <TARGET> [OPTIONS]
    ```

3.  **Common Commands:**
    -   **Scan top 1000 ports:** `python3 scanner.py 192.168.1.1`
    -   **Scan specific ports:** `python3 scanner.py google.com -p 22,80,443`
    -   **Save to CSV:** `python3 scanner.py google.com --output-csv results.csv`
    -   **Silent Mode (Log only):** `python3 scanner.py google.com --silent`

## 5. Optional Improvements
-   **UDP Scanning:** Add support for `SOCK_DGRAM` to scan UDP ports (DNS, DHCP).
-   **Service Identification:** Map port numbers to common service names (e.g., 80 -> HTTP) using `socket.getservbyport`.
-   **GUI:** Build a simple frontend using `tkinter` or `PyQt`.
