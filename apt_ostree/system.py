import os
import sys

from rich.console import Console

console = Console()

def check_user():
    """Check for root user"""
    if os.getuid() != 0:
        console.print("You are not root.")
        sys.exit(1)

