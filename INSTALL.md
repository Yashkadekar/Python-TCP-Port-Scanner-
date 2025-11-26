# Installation Guide - Python Port Scanner

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation Methods

### Method 1: Install from Source (Recommended for Development)

1. **Clone or download the project:**
   ```bash
   cd "/Users/yash/Documents/Python TCP Port Scanner – Full Project Build"
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Install the package in development mode:**
   ```bash
   pip install -e .
   ```

### Method 2: Install as a Package

1. **Navigate to the project directory:**
   ```bash
   cd "/Users/yash/Documents/Python TCP Port Scanner – Full Project Build"
   ```

2. **Install using pip:**
   ```bash
   pip install .
   ```

## Running the Application

### Command Line Interface (CLI)

After installation, you can run the scanner from anywhere:

```bash
# Using the installed command
port-scanner google.com -p 80,443

# Or directly with Python
python3 scanner.py google.com -p 80,443
```

### Graphical User Interface (GUI)

```bash
# Using the installed command
port-scanner-gui

# Or directly with Python
python3 gui_scanner.py
```

## Platform-Specific Notes

### macOS

- tkinter is usually pre-installed with Python
- You may need to install Python from python.org if using the system Python
- For UDP scanning, you may need elevated privileges:
  ```bash
  sudo port-scanner example.com --udp -p 53,123
  ```

### Linux

- Install tkinter if not present:
  ```bash
  # Debian/Ubuntu
  sudo apt-get install python3-tk
  
  # Fedora
  sudo dnf install python3-tkinter
  
  # Arch
  sudo pacman -S tk
  ```

- For UDP scanning, use sudo:
  ```bash
  sudo port-scanner example.com --udp -p 53,123
  ```

### Windows

- Python from python.org includes tkinter
- Run Command Prompt or PowerShell as Administrator for UDP scanning
- Firewall may prompt for permissions

## Troubleshooting

### "tqdm not found" or "ttkbootstrap not found"

```bash
pip install tqdm ttkbootstrap
```

### "Permission denied" errors

- Use `sudo` on macOS/Linux for privileged ports
- Run as Administrator on Windows

### GUI doesn't start

- Verify tkinter is installed:
  ```bash
  python3 -c "import tkinter"
  ```
- If error, install tkinter for your platform (see above)

### Virtual environment issues

- Ensure you've activated the virtual environment
- Check Python version: `python3 --version`
- Recreate the virtual environment if needed:
  ```bash
  rm -rf venv
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

## Uninstallation

```bash
pip uninstall python-port-scanner
```

## Development Setup

For contributing or development:

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=scanner --cov-report=html
```

## Next Steps

- Read the [README.md](README.md) for usage examples
- Check [Documentation.md](Documentation.md) for technical details
- Review the [FINAL_REPORT.md](FINAL_REPORT.md) for project overview
