"""
Kotli LIMS - Frontend Entry Point
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from main_window import Kotli_LIMS_MainWindow


def main():
    """Main application entry point"""
    
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Kotli LIMS")
    app.setApplicationVersion("1.0.0")
    app.setApplicationDisplayName("Kotli Laboratory Information Management System")
    
    # Create and show main window
    window = Kotli_LIMS_MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
