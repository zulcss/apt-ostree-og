import shutil
import sys

from rich.console import Console

class Image(object):
    def __init__(self):
        self.console = Console()
    
    def build(self):
        """Build an image."""
        
        
