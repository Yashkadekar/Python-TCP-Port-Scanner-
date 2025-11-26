"""
Python TCP/UDP Port Scanner - Enhanced Edition
-----------------------------------------------
Author: Cybersecurity Instructor (AI Assistant)
Date: 2025-11-26
Purpose: Professional network reconnaissance and security auditing tool.

DISCLAIMER:
This tool is for educational purposes and authorized security testing only.
Scanning networks without permission is illegal and unethical. 
The author is not responsible for any misuse of this code.
"""

import socket
import argparse
import threading
import logging
import time
import csv
import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Tuple, List, Dict, Optional
import os

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    print("Warning: tqdm not installed. Progress bars disabled. Install with: pip install tqdm")

# Common service signatures for identification
SERVICE_SIGNATURES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Proxy",
    27017: "MongoDB",
}

# UDP probe payloads for common services
UDP_PROBES = {
    53: b'\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00',  # DNS query
    123: b'\x1b' + b'\x00' * 47,  # NTP request
    161: b'\x30\x26\x02\x01\x00\x04\x06\x70\x75\x62\x6c\x69\x63',  # SNMP
}

def setup_logging(log_file_path: Optional[str] = None, silent: bool = False) -> str:
    """
    Configures the logging system.
    
    Args:
        log_file_path: Optional custom path for the log file.
        silent: If True, suppresses console output (file logging only).
        
    Returns:
        The absolute path to the created log file.
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    if log_file_path:
        log_file = log_file_path
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"scan_{timestamp}.log")
    
    handlers = [logging.FileHandler(log_file)]
    if not silent:
        handlers.append(logging.StreamHandler())
        
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=handlers,
        force=True
    )
    return log_file

def identify_service(port: int, banner: str = "") -> str:
    """
    Identifies the service running on a port.
    
    Args:
        port: The port number.
        banner: Optional service banner.
        
    Returns:
        Service name or "Unknown".
    """
    # Validate port range
    if not (0 <= port <= 65535):
        return "Invalid Port"
    
    # Check known service signatures
    if port in SERVICE_SIGNATURES:
        service = SERVICE_SIGNATURES[port]
        if banner:
            return f"{service} ({banner[:30]})"
        return service
    
    # Try to get service name from system
    try:
        service = socket.getservbyport(port, 'tcp')
        if banner:
            return f"{service} ({banner[:30]})"
        return service
    except (OSError, socket.error):
        pass
    
    if banner:
        return f"Unknown ({banner[:30]})"
    return "Unknown"

def scan_port(ip: str, port: int, timeout: float, stealth: bool = False) -> Tuple[int, str, str, str]:
    """
    Scans a single TCP port to check if it is open.
    
    Args:
        ip: The target IP address.
        port: The port number to scan.
        timeout: Socket timeout in seconds.
        stealth: If True, adds random delays for stealth scanning.
        
    Returns:
        tuple: (port, status, banner, service)
    """
    # Validate port range
    if not (0 <= port <= 65535):
        return port, f"ERROR: connect_ex(): port must be 0-65535.", "", ""
    
    if stealth:
        time.sleep(random.uniform(0.1, 0.5))
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            
            if result == 0:
                banner = ""
                try:
                    s.send(b'HEAD / HTTP/1.0\r\n\r\n')
                    banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
                except:
                    pass
                
                service = identify_service(port, banner)
                return port, "OPEN", banner, service
            else:
                return port, "CLOSED", "", ""
    except socket.timeout:
        return port, "TIMEOUT", "", ""
    except Exception as e:
        return port, f"ERROR: {str(e)}", "", ""

def scan_udp_port(ip: str, port: int, timeout: float) -> Tuple[int, str, str, str]:
    """
    Scans a single UDP port to check if it is open.
    
    Args:
        ip: The target IP address.
        port: The port number to scan.
        timeout: Socket timeout in seconds.
        
    Returns:
        tuple: (port, status, response, service)
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(timeout)
            
            # Send protocol-specific probe if available
            probe = UDP_PROBES.get(port, b'\x00')
            s.sendto(probe, (ip, port))
            
            try:
                data, _ = s.recvfrom(1024)
                response = data.decode('utf-8', errors='ignore').strip()
                service = identify_service(port, response)
                return port, "OPEN", response, service
            except socket.timeout:
                # UDP timeout doesn't necessarily mean closed
                return port, "OPEN|FILTERED", "", identify_service(port)
    except Exception as e:
        return port, f"ERROR: {str(e)}", "", ""

def parse_ports(port_arg: str) -> List[int]:
    """
    Parses the port argument string into a list of integers.
    
    Args:
        port_arg: The port string (e.g., "80,443,1000-2000").
        
    Returns:
        A sorted list of unique integer ports.
    """
    ports = set()
    parts = port_arg.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                ports.update(range(start, end + 1))
            except ValueError:
                continue
        else:
            try:
                ports.add(int(part))
            except ValueError:
                continue
    return sorted(list(ports))

def export_json(results: List[Dict], output_file: str, target: str, target_ip: str):
    """
    Exports scan results to JSON format.
    
    Args:
        results: List of scan result dictionaries.
        output_file: Path to the output JSON file.
        target: Target hostname.
        target_ip: Resolved IP address.
    """
    output = {
        "scan_metadata": {
            "target": target,
            "resolved_ip": target_ip,
            "timestamp": datetime.now().isoformat(),
            "total_ports_scanned": len(results),
            "open_ports_count": sum(1 for r in results if r['status'] == 'OPEN')
        },
        "results": results
    }
    
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

def main():
    """
    Main execution function.
    Parses arguments, sets up logging, and manages the thread pool for scanning.
    """
    parser = argparse.ArgumentParser(
        description="Python TCP/UDP Port Scanner - Enhanced Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s google.com -p 80,443
  %(prog)s 192.168.1.1 -p 1-1000 --udp
  %(prog)s example.com -p 22,80,443 --output-json results.json
  %(prog)s 10.0.0.1 -p 1-65535 -t 1000 --stealth --output-csv scan.csv
        """
    )
    
    # Required Argument
    parser.add_argument("target", help="Target IP address or hostname")
    
    # Port Configuration
    parser.add_argument("-p", "--ports", default="1-1024", 
                       help="Port range (e.g., 1-100, 80,443) [default: 1-1024]")
    
    # Scan Type
    parser.add_argument("--tcp", action="store_true", default=True,
                       help="Perform TCP scan (default)")
    parser.add_argument("--udp", action="store_true",
                       help="Perform UDP scan")
    parser.add_argument("--both", action="store_true",
                       help="Perform both TCP and UDP scans")
    
    # Performance
    parser.add_argument("-t", "--threads", type=int, default=200,
                       help="Number of threads [default: 200]")
    parser.add_argument("--timeout", type=float, default=1.0,
                       help="Socket timeout in seconds [default: 1.0]")
    
    # Stealth Options
    parser.add_argument("--stealth", action="store_true",
                       help="Enable stealth mode (random delays)")
    
    # Output Options
    parser.add_argument("--log", help="Custom log file path")
    parser.add_argument("--output-csv", help="Output results to a CSV file")
    parser.add_argument("--output-json", help="Output results to a JSON file")
    parser.add_argument("--silent", action="store_true",
                       help="Suppress console output")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Show closed and timeout ports")
    parser.add_argument("--no-progress", action="store_true",
                       help="Disable progress bar")
    
    args = parser.parse_args()
    
    # Setup logging
    log_file = setup_logging(args.log, args.silent)
    
    # Resolve Hostname
    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        if not args.silent:
            print(f"ERROR: Could not resolve hostname: {args.target}")
        logging.error(f"Could not resolve hostname: {args.target}")
        return
    
    # Parse Ports
    ports = parse_ports(args.ports)
    
    # Determine scan types
    scan_tcp = args.tcp or not (args.udp or args.both)
    scan_udp = args.udp or args.both
    
    # Log Start Info
    scan_types = []
    if scan_tcp:
        scan_types.append("TCP")
    if scan_udp:
        scan_types.append("UDP")
    
    logging.info(f"Starting {'/'.join(scan_types)} scan on host: {args.target} ({target_ip})")
    logging.info(f"Scanning {len(ports)} ports with {args.threads} threads...")
    logging.info(f"Log file: {log_file}")
    if args.stealth:
        logging.info("Stealth mode: ENABLED")
    if args.output_csv:
        logging.info(f"CSV Output: {args.output_csv}")
    if args.output_json:
        logging.info(f"JSON Output: {args.output_json}")
    
    start_time = time.time()
    open_ports = []
    all_results = []
    
    # Initialize CSV Writer if requested
    csv_file = None
    csv_writer = None
    if args.output_csv:
        try:
            csv_file = open(args.output_csv, 'w', newline='')
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["timestamp", "target", "resolved_ip", "port", "protocol", "status", "service", "banner"])
        except IOError as e:
            logging.error(f"Could not open CSV file for writing: {e}")
            return
    
    try:
        # Prepare scan tasks
        tasks = []
        if scan_tcp:
            tasks.extend([('TCP', port) for port in ports])
        if scan_udp:
            tasks.extend([('UDP', port) for port in ports])
        
        # Use ThreadPoolExecutor for concurrency
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            # Submit all scan tasks
            futures = {}
            for protocol, port in tasks:
                if protocol == 'TCP':
                    future = executor.submit(scan_port, target_ip, port, args.timeout, args.stealth)
                else:  # UDP
                    future = executor.submit(scan_udp_port, target_ip, port, args.timeout)
                futures[future] = (protocol, port)
            
            # Setup progress bar
            if TQDM_AVAILABLE and not args.silent and not args.no_progress:
                progress_bar = tqdm(total=len(futures), desc="Scanning", unit="port")
            else:
                progress_bar = None
            
            # Process results as they complete
            for future in as_completed(futures):
                protocol, original_port = futures[future]
                port, status, banner, service = future.result()
                timestamp = datetime.now().isoformat()
                
                # Store result for JSON export
                result_dict = {
                    "timestamp": timestamp,
                    "port": port,
                    "protocol": protocol,
                    "status": status,
                    "service": service,
                    "banner": banner
                }
                all_results.append(result_dict)
                
                # Console/Log Output Logic
                if status == "OPEN" or status == "OPEN|FILTERED":
                    msg = f"Port {port}/{protocol}: {status}"
                    if service:
                        msg += f" | Service: {service}"
                    if banner and len(banner) > 0:
                        msg += f" | Banner: {banner[:50]}"
                    logging.info(msg)
                    open_ports.append(f"{port}/{protocol}")
                elif args.verbose:
                    logging.info(f"Port {port}/{protocol}: {status}")
                
                # CSV Output Logic
                if csv_writer:
                    csv_writer.writerow([timestamp, args.target, target_ip, port, protocol, status, service, banner])
                
                # Update progress bar
                if progress_bar:
                    progress_bar.update(1)
            
            # Close progress bar
            if progress_bar:
                progress_bar.close()
                    
    except KeyboardInterrupt:
        logging.warning("\nScan interrupted by user (Ctrl+C). Exiting...")
        if csv_file:
            csv_file.close()
        return
    
    # Cleanup
    if csv_file:
        csv_file.close()
    
    # Export JSON if requested
    if args.output_json:
        try:
            export_json(all_results, args.output_json, args.target, target_ip)
            logging.info(f"JSON results exported to: {args.output_json}")
        except Exception as e:
            logging.error(f"Failed to export JSON: {e}")
    
    # Summary
    duration = time.time() - start_time
    logging.info(f"Scan completed in {duration:.2f} seconds.")
    logging.info(f"Open ports found: {open_ports if open_ports else 'None'}")

if __name__ == "__main__":
    main()
