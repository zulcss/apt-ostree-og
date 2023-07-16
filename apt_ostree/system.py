import os
import socket
import sys

from rich.console import Console

console = Console()

def check_user():
    """Check for root user"""
    if os.getuid() != 0:
        console.print("You are not root.")
        sys.exit(1)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return (s.getsockname()[0])
