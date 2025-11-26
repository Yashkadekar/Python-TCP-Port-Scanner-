"""
Python Port Scanner - GUI Application
--------------------------------------
Author: Cybersecurity Instructor (AI Assistant)
Date: 2025-11-26
Purpose: Graphical interface for the port scanner tool.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import socket
import json
import csv
from datetime import datetime
from typing import List, Dict
import os
import sys

try:
    import ttkbootstrap as ttkb
    from ttkbootstrap.constants import *
    TTKBOOTSTRAP_AVAILABLE = True
except ImportError:
    TTKBOOTSTRAP_AVAILABLE = False
    print("Warning: ttkbootstrap not installed. Using standard tkinter theme.")

# Import scanner functions
from scanner import scan_port, scan_udp_port, parse_ports, identify_service

class PortScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Port Scanner - Enhanced Edition")
        self.root.geometry("1000x700")
        
        # Variables
        self.scanning = False
        self.results = []
        self.current_theme = "darkly" if TTKBOOTSTRAP_AVAILABLE else "default"
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🛡️ Port Scanner", 
                               font=("Helvetica", 24, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Input Frame
        input_frame = ttk.LabelFrame(main_frame, text="Scan Configuration", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Target
        ttk.Label(input_frame, text="Target:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.target_entry = ttk.Entry(input_frame, width=40)
        self.target_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.target_entry.insert(0, "localhost")
        
        # Ports
        ttk.Label(input_frame, text="Ports:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ports_entry = ttk.Entry(input_frame, width=40)
        self.ports_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.ports_entry.insert(0, "20-25,80,443,3306,8080")
        
        # Scan Type
        ttk.Label(input_frame, text="Scan Type:").grid(row=2, column=0, sticky=tk.W, pady=5)
        scan_type_frame = ttk.Frame(input_frame)
        scan_type_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.scan_type = tk.StringVar(value="TCP")
        ttk.Radiobutton(scan_type_frame, text="TCP", variable=self.scan_type, 
                       value="TCP").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(scan_type_frame, text="UDP", variable=self.scan_type, 
                       value="UDP").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(scan_type_frame, text="Both", variable=self.scan_type, 
                       value="BOTH").pack(side=tk.LEFT, padx=5)
        
        # Options
        options_frame = ttk.Frame(input_frame)
        options_frame.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.stealth_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Stealth Mode", 
                       variable=self.stealth_var).pack(side=tk.LEFT, padx=5)
        
        self.verbose_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Verbose", 
                       variable=self.verbose_var).pack(side=tk.LEFT, padx=5)
        
        # Threads
        ttk.Label(input_frame, text="Threads:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.threads_spinbox = ttk.Spinbox(input_frame, from_=1, to=1000, width=10)
        self.threads_spinbox.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        self.threads_spinbox.set(200)
        
        # Control Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=(0, 10))
        
        self.scan_button = ttk.Button(button_frame, text="Start Scan", 
                                      command=self.start_scan, style="success.TButton" if TTKBOOTSTRAP_AVAILABLE else "TButton")
        self.scan_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop Scan", 
                                     command=self.stop_scan, state=tk.DISABLED,
                                     style="danger.TButton" if TTKBOOTSTRAP_AVAILABLE else "TButton")
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear Results", 
                  command=self.clear_results).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Export CSV", 
                  command=self.export_csv).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Export JSON", 
                  command=self.export_json).pack(side=tk.LEFT, padx=5)
        
        # Results Frame
        results_frame = ttk.LabelFrame(main_frame, text="Scan Results", padding="10")
        results_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Results Treeview
        columns = ("Port", "Protocol", "Status", "Service", "Banner")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        # Define headings
        for col in columns:
            self.results_tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            if col == "Banner":
                self.results_tree.column(col, width=300)
            elif col == "Service":
                self.results_tree.column(col, width=150)
            else:
                self.results_tree.column(col, width=80)
        
        # Scrollbars
        vsb = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        hsb = ttk.Scrollbar(results_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Status Bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=4, column=0, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(status_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.progress = ttk.Progressbar(status_frame, mode='determinate')
        self.progress.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
    def sort_treeview(self, col):
        """Sort treeview by column."""
        items = [(self.results_tree.set(item, col), item) for item in self.results_tree.get_children('')]
        items.sort()
        
        for index, (val, item) in enumerate(items):
            self.results_tree.move(item, '', index)
    
    def start_scan(self):
        """Start the port scan in a separate thread."""
        target = self.target_entry.get().strip()
        ports_str = self.ports_entry.get().strip()
        
        if not target:
            messagebox.showerror("Error", "Please enter a target host")
            return
        
        if not ports_str:
            messagebox.showerror("Error", "Please enter ports to scan")
            return
        
        # Resolve hostname
        try:
            target_ip = socket.gethostbyname(target)
        except socket.gaierror:
            messagebox.showerror("Error", f"Could not resolve hostname: {target}")
            return
        
        # Parse ports
        try:
            ports = parse_ports(ports_str)
            if not ports:
                messagebox.showerror("Error", "No valid ports specified")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Invalid port format: {e}")
            return
        
        # Update UI
        self.scanning = True
        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text=f"Scanning {target} ({target_ip})...")
        self.progress['value'] = 0
        self.progress['maximum'] = len(ports)
        
        # Start scan thread
        scan_thread = threading.Thread(target=self.perform_scan, 
                                       args=(target, target_ip, ports))
        scan_thread.daemon = True
        scan_thread.start()
    
    def perform_scan(self, target, target_ip, ports):
        """Perform the actual port scan."""
        scan_type = self.scan_type.get()
        threads = int(self.threads_spinbox.get())
        stealth = self.stealth_var.get()
        timeout = 1.0
        
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        tasks = []
        if scan_type in ["TCP", "BOTH"]:
            tasks.extend([('TCP', port) for port in ports])
        if scan_type in ["UDP", "BOTH"]:
            tasks.extend([('UDP', port) for port in ports])
        
        completed = 0
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {}
            for protocol, port in tasks:
                if protocol == 'TCP':
                    future = executor.submit(scan_port, target_ip, port, timeout, stealth)
                else:
                    future = executor.submit(scan_udp_port, target_ip, port, timeout)
                futures[future] = (protocol, port)
            
            for future in as_completed(futures):
                if not self.scanning:
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
                
                protocol, original_port = futures[future]
                try:
                    port, status, banner, service = future.result()
                    
                    # Add to results
                    result = {
                        'port': port,
                        'protocol': protocol,
                        'status': status,
                        'service': service,
                        'banner': banner[:50] if banner else ""
                    }
                    self.results.append(result)
                    
                    # Update UI (must be done in main thread)
                    if status in ["OPEN", "OPEN|FILTERED"] or self.verbose_var.get():
                        self.root.after(0, self.add_result_to_tree, result)
                    
                    completed += 1
                    self.root.after(0, self.update_progress, completed)
                    
                except Exception as e:
                    print(f"Error scanning port {original_port}: {e}")
        
        # Scan complete
        self.root.after(0, self.scan_complete)
    
    def add_result_to_tree(self, result):
        """Add a result to the treeview."""
        # Color code based on status
        tag = ""
        if result['status'] == "OPEN":
            tag = "open"
        elif result['status'] == "OPEN|FILTERED":
            tag = "filtered"
        
        self.results_tree.insert("", tk.END, values=(
            result['port'],
            result['protocol'],
            result['status'],
            result['service'],
            result['banner']
        ), tags=(tag,))
        
        # Configure tags
        self.results_tree.tag_configure("open", foreground="green")
        self.results_tree.tag_configure("filtered", foreground="orange")
    
    def update_progress(self, completed):
        """Update the progress bar."""
        self.progress['value'] = completed
        open_count = sum(1 for r in self.results if r['status'] in ["OPEN", "OPEN|FILTERED"])
        self.status_label.config(text=f"Scanned: {completed}/{self.progress['maximum']} | Open: {open_count}")
    
    def scan_complete(self):
        """Handle scan completion."""
        self.scanning = False
        self.scan_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        open_count = sum(1 for r in self.results if r['status'] in ["OPEN", "OPEN|FILTERED"])
        self.status_label.config(text=f"Scan complete! Found {open_count} open ports.")
        messagebox.showinfo("Scan Complete", f"Scan finished!\n\nOpen ports found: {open_count}")
    
    def stop_scan(self):
        """Stop the current scan."""
        self.scanning = False
        self.status_label.config(text="Scan stopped by user")
        self.scan_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def clear_results(self):
        """Clear all results."""
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.results = []
        self.status_label.config(text="Results cleared")
        self.progress['value'] = 0
    
    def export_csv(self):
        """Export results to CSV."""
        if not self.results:
            messagebox.showwarning("No Results", "No results to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Port", "Protocol", "Status", "Service", "Banner"])
                    for result in self.results:
                        writer.writerow([
                            result['port'],
                            result['protocol'],
                            result['status'],
                            result['service'],
                            result['banner']
                        ])
                messagebox.showinfo("Success", f"Results exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export CSV: {e}")
    
    def export_json(self):
        """Export results to JSON."""
        if not self.results:
            messagebox.showwarning("No Results", "No results to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                output = {
                    "scan_metadata": {
                        "target": self.target_entry.get(),
                        "timestamp": datetime.now().isoformat(),
                        "total_ports_scanned": len(self.results),
                        "open_ports_count": sum(1 for r in self.results if r['status'] in ["OPEN", "OPEN|FILTERED"])
                    },
                    "results": self.results
                }
                
                with open(filename, 'w') as f:
                    json.dump(output, f, indent=2)
                
                messagebox.showinfo("Success", f"Results exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export JSON: {e}")

def main():
    """Main entry point for the GUI application."""
    if TTKBOOTSTRAP_AVAILABLE:
        root = ttkb.Window(themename="darkly")
    else:
        root = tk.Tk()
    
    app = PortScannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
