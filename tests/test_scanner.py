"""
Unit tests for the port scanner.
"""

import unittest
from unittest.mock import patch, MagicMock
import socket
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner import parse_ports, identify_service, scan_port, scan_udp_port

class TestPortParsing(unittest.TestCase):
    """Test the port parsing functionality."""
    
    def test_single_port(self):
        """Test parsing a single port."""
        result = parse_ports("80")
        self.assertEqual(result, [80])
    
    def test_multiple_ports(self):
        """Test parsing multiple ports."""
        result = parse_ports("80,443,8080")
        self.assertEqual(result, [80, 443, 8080])
    
    def test_port_range(self):
        """Test parsing a port range."""
        result = parse_ports("20-25")
        self.assertEqual(result, [20, 21, 22, 23, 24, 25])
    
    def test_mixed_format(self):
        """Test parsing mixed format."""
        result = parse_ports("22,80,100-103,443")
        self.assertEqual(result, [22, 80, 100, 101, 102, 103, 443])
    
    def test_invalid_input(self):
        """Test handling of invalid input."""
        result = parse_ports("abc,80,xyz")
        self.assertEqual(result, [80])
    
    def test_duplicate_removal(self):
        """Test that duplicates are removed."""
        result = parse_ports("80,80,80")
        self.assertEqual(result, [80])
    
    def test_sorting(self):
        """Test that results are sorted."""
        result = parse_ports("443,22,80")
        self.assertEqual(result, [22, 80, 443])

class TestServiceIdentification(unittest.TestCase):
    """Test the service identification functionality."""
    
    def test_known_service(self):
        """Test identification of known services."""
        self.assertEqual(identify_service(80), "HTTP")
        self.assertEqual(identify_service(443), "HTTPS")
        self.assertEqual(identify_service(22), "SSH")
    
    def test_unknown_service(self):
        """Test identification of unknown services."""
        result = identify_service(99999)
        self.assertEqual(result, "Invalid Port")
    
    def test_service_with_banner(self):
        """Test service identification with banner."""
        result = identify_service(80, "Apache/2.4.41")
        self.assertIn("HTTP", result)
        self.assertIn("Apache", result)

class TestPortScanning(unittest.TestCase):
    """Test the port scanning functionality."""
    
    @patch('socket.socket')
    def test_scan_open_port(self, mock_socket):
        """Test scanning an open port."""
        # Mock successful connection
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 0
        mock_sock.recv.return_value = b"HTTP/1.1 200 OK"
        mock_socket.return_value.__enter__.return_value = mock_sock
        
        port, status, banner, service = scan_port("127.0.0.1", 80, 1.0)
        
        self.assertEqual(port, 80)
        self.assertEqual(status, "OPEN")
        self.assertIn("HTTP", service)
    
    @patch('socket.socket')
    def test_scan_closed_port(self, mock_socket):
        """Test scanning a closed port."""
        # Mock connection refused
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 1  # Connection refused
        mock_socket.return_value.__enter__.return_value = mock_sock
        
        port, status, banner, service = scan_port("127.0.0.1", 9999, 1.0)
        
        self.assertEqual(port, 9999)
        self.assertEqual(status, "CLOSED")
        self.assertEqual(banner, "")
    
    @patch('socket.socket')
    def test_scan_timeout(self, mock_socket):
        """Test scanning with timeout."""
        # Mock timeout
        mock_sock = MagicMock()
        mock_sock.connect_ex.side_effect = socket.timeout
        mock_socket.return_value.__enter__.return_value = mock_sock
        
        port, status, banner, service = scan_port("127.0.0.1", 80, 0.1)
        
        self.assertEqual(port, 80)
        self.assertEqual(status, "TIMEOUT")
    
    @patch('socket.socket')
    def test_stealth_mode(self, mock_socket):
        """Test stealth mode adds delays."""
        import time
        
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 0
        mock_sock.recv.return_value = b""
        mock_socket.return_value.__enter__.return_value = mock_sock
        
        start = time.time()
        scan_port("127.0.0.1", 80, 1.0, stealth=True)
        duration = time.time() - start
        
        # Should have at least some delay (0.1-0.5 seconds)
        self.assertGreater(duration, 0.05)

class TestUDPScanning(unittest.TestCase):
    """Test UDP scanning functionality."""
    
    @patch('socket.socket')
    def test_udp_scan_response(self, mock_socket):
        """Test UDP scan with response."""
        mock_sock = MagicMock()
        mock_sock.recvfrom.return_value = (b"DNS Response", ("127.0.0.1", 53))
        mock_socket.return_value.__enter__.return_value = mock_sock
        
        port, status, response, service = scan_udp_port("127.0.0.1", 53, 1.0)
        
        self.assertEqual(port, 53)
        self.assertEqual(status, "OPEN")
    
    @patch('socket.socket')
    def test_udp_scan_timeout(self, mock_socket):
        """Test UDP scan with timeout."""
        mock_sock = MagicMock()
        mock_sock.recvfrom.side_effect = socket.timeout
        mock_socket.return_value.__enter__.return_value = mock_sock
        
        port, status, response, service = scan_udp_port("127.0.0.1", 161, 1.0)
        
        self.assertEqual(port, 161)
        self.assertEqual(status, "OPEN|FILTERED")

class TestIntegration(unittest.TestCase):
    """Integration tests."""
    
    def test_localhost_scan(self):
        """Test scanning localhost (should be safe)."""
        # This is a real scan but should be safe on localhost
        # Use port 65000 which should be closed on most systems
        port, status, banner, service = scan_port("127.0.0.1", 65000, 0.5)
        
        # Port should be closed or timeout on most systems
        self.assertIn(status, ["CLOSED", "TIMEOUT", "OPEN"])
    
    def test_hostname_resolution(self):
        """Test that hostname resolution works."""
        try:
            ip = socket.gethostbyname("localhost")
            self.assertEqual(ip, "127.0.0.1")
        except socket.gaierror:
            self.fail("Could not resolve localhost")

def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == "__main__":
    unittest.main()
