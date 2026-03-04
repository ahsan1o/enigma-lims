"""
Kotli LIMS - PyQt6 Main Window
Modern Dark Theme Desktop Application
"""

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QSplitter, QMessageBox, QStatusBar, QMenuBar, QMenu,
    QDockWidget, QComboBox, QSpinBox, QDateEdit, QDialog,
    QFormLayout, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt, QTimer, QDateTime, QSize
from PyQt6.QtGui import QPalette, QColor, QFont, QIcon, QPixmap
from PyQt6.QtCore import pyqtSignal, QObject
import requests

from config import COLORS, BUTTON_STYLES, DIMENSIONS, APP_CONFIG, get_qss_stylesheet
from api_client import api_client


class Kotli_LIMS_MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_CONFIG['app_name']} v{APP_CONFIG['app_version']}")
        self.setMinimumSize(DIMENSIONS["window_min_width"], DIMENSIONS["window_min_height"])
        
        # Apply stylesheet
        self.setStyleSheet(get_qss_stylesheet())
        
        # Setup UI
        self.setup_ui()
        self.setup_connections()
        self.check_server_connection()
        
        # Center window
        self.center_window()
    
    def setup_ui(self):
        """Setup user interface"""
        # Main central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # ====================================================================
        # LEFT SIDEBAR NAVIGATION
        # ====================================================================
        
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar, 0)
        
        # ====================================================================
        # CONTENT AREA (Stacked Widget for screens)
        # ====================================================================
        
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack, 1)
        
        # Add screens
        self.dashboard_screen = self.create_dashboard_screen()
        self.samples_screen = self.create_samples_screen()
        self.results_screen = self.create_results_screen()
        self.reports_screen = self.create_reports_screen()
        self.settings_screen = self.create_settings_screen()
        
        self.content_stack.addWidget(self.dashboard_screen)
        self.content_stack.addWidget(self.samples_screen)
        self.content_stack.addWidget(self.results_screen)
        self.content_stack.addWidget(self.reports_screen)
        self.content_stack.addWidget(self.settings_screen)
        
        # Show dashboard by default
        self.content_stack.setCurrentIndex(0)
        
        # ====================================================================
        # STATUS BAR
        # ====================================================================
        
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        self.status_label = QLabel("Ready")
        self.server_status = QLabel("● Server")
        self.server_status.setStyleSheet(f"color: {COLORS['success']};")
        status_bar.addWidget(self.status_label, 1)
        status_bar.addPermanentWidget(self.server_status)
        
        # ====================================================================
        # MENU BAR
        # ====================================================================
        
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("Exit", self.close)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        tools_menu.addAction("Backup Database")
        tools_menu.addAction("Restore Backup")
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self.show_about)
        help_menu.addAction("Documentation")
    
    def create_sidebar(self) -> QWidget:
        """Create left sidebar navigation"""
        sidebar = QFrame()
        sidebar.setStyleSheet(f"background-color: {COLORS['bg_card']};")
        sidebar.setFixedWidth(DIMENSIONS["sidebar_width"])
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo/Title
        title = QLabel("Kotli LIMS")
        title_font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {COLORS['primary']};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(20)
        
        # Navigation buttons
        nav_buttons = [
            ("🏠 Dashboard", 0),
            ("🧪 Samples", 1),
            ("📊 Results", 2),
            ("📄 Reports", 3),
            ("⚙️  Settings", 4),
        ]
        
        for text, screen_index in nav_buttons:
            btn = self.create_nav_button(text, screen_index)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # User profile
        profile_frame = QFrame()
        profile_layout = QVBoxLayout()
        profile_label = QLabel("👤 Admin User")
        profile_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        profile_layout.addWidget(profile_label)
        profile_frame.setLayout(profile_layout)
        layout.addWidget(profile_frame)
        
        sidebar.setLayout(layout)
        return sidebar
    
    def create_nav_button(self, text: str, screen_index: int) -> QPushButton:
        """Create a navigation button"""
        btn = QPushButton(text)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_card']};
                color: {COLORS['text_primary']};
                border: none;
                border-left: 3px solid transparent;
                padding: 12px;
                text-align: left;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_hover']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['primary']};
                border-left: 3px solid {COLORS['primary_light']};
            }}
        """)
        btn.setFixedHeight(45)
        btn.clicked.connect(lambda: self.switch_screen(screen_index))
        return btn
    
    def switch_screen(self, index: int):
        """Switch to different screen"""
        self.content_stack.setCurrentIndex(index)
        screens = [
            "Dashboard",
            "Sample Management",
            "Results Review",
            "Report Generation",
            "Settings"
        ]
        self.status_label.setText(f"Screen: {screens[index]}")
    
    def create_dashboard_screen(self) -> QWidget:
        """Create dashboard screen"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Dashboard")
        header_font = QFont("Segoe UI", 20, QFont.Weight.Bold)
        header.setFont(header_font)
        layout.addWidget(header)
        
        # Quick stats
        stats_layout = QHBoxLayout()
        stats = [
            ("Pending Samples", "12", COLORS["warning"]),
            ("Completed Today", "34", COLORS["success"]),
            ("Awaiting Approval", "5", COLORS["info"]),
            ("Critical Values", "2", COLORS["danger"]),
        ]
        
        for title, value, color in stats:
            card = self.create_stat_card(title, value, color)
            stats_layout.addWidget(card)
        
        layout.addLayout(stats_layout)
        
        # Recent activity
        layout.addSpacing(20)
        activity_label = QLabel("Recent Activity")
        activity_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(activity_label)
        
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Sample ID", "Patient", "Test", "Status"])
        table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['bg_card']};
                alternate-background-color: {COLORS['bg_darker']};
                gridline-color: {COLORS['separator']};
            }}
        """)
        # Add sample data
        table.insertRow(0)
        table.setItem(0, 0, QTableWidgetItem("LAB-2026-00145"))
        table.setItem(0, 1, QTableWidgetItem("Ahmed Hassan"))
        table.setItem(0, 2, QTableWidgetItem("CBC"))
        table.setItem(0, 3, QTableWidgetItem("Completed"))
        layout.addWidget(table)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_stat_card(self, title: str, value: str, color: str) -> QFrame:
        """Create a statistics card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_darker']};
                border: 1px solid {COLORS['border']};
                border-radius: {DIMENSIONS['border_radius']}px;
                padding: 16px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_font = QFont("Segoe UI", 24, QFont.Weight.Bold)
        value_label.setFont(value_font)
        value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)
        
        card.setLayout(layout)
        return card
    
    def create_samples_screen(self) -> QWidget:
        """Create samples management screen"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        header = QLabel("Sample Management")
        header_font = QFont("Segoe UI", 20, QFont.Weight.Bold)
        header.setFont(header_font)
        layout.addWidget(header)
        
        # Search/filter bar
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(QLineEdit())
        search_layout.addWidget(QPushButton("+ New Sample"))
        layout.addLayout(search_layout)
        
        # Samples table
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Barcode", "Patient", "Type", "Date", "Status"])
        layout.addWidget(table)
        
        widget.setLayout(layout)
        return widget
    
    def create_results_screen(self) -> QWidget:
        """Create results review screen"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        header = QLabel("Results Review")
        header_font = QFont("Segoe UI", 20, QFont.Weight.Bold)
        header.setFont(header_font)
        layout.addWidget(header)
        
        layout.addWidget(QLabel("Pending approval: 5"))
        
        widget.setLayout(layout)
        return widget
    
    def create_reports_screen(self) -> QWidget:
        """Create reports generation screen"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        header = QLabel("Report Generation")
        header_font = QFont("Segoe UI", 20, QFont.Weight.Bold)
        header.setFont(header_font)
        layout.addWidget(header)
        
        layout.addWidget(QLabel("Export and print reports"))
        
        widget.setLayout(layout)
        return widget
    
    def create_settings_screen(self) -> QWidget:
        """Create settings screen"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        header = QLabel("Settings")
        header_font = QFont("Segoe UI", 20, QFont.Weight.Bold)
        header.setFont(header_font)
        layout.addWidget(header)
        
        form_layout = QFormLayout()
        form_layout.addRow("Lab Name:", QLineEdit("Kotli Clinical Lab"))
        form_layout.addRow("Lab Code:", QLineEdit("KCL"))
        form_layout.addRow("Theme:", QComboBox())
        
        layout.addLayout(form_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def setup_connections(self):
        """Setup signal/slot connections"""
        # Server status check every 30 seconds
        self.server_timer = QTimer()
        self.server_timer.timeout.connect(self.check_server_connection)
        self.server_timer.start(30000)
    
    def check_server_connection(self):
        """Check if backend server is running"""
        if api_client.health_check():
            self.server_status.setText("● Server Connected")
            self.server_status.setStyleSheet(f"color: {COLORS['success']};")
        else:
            self.server_status.setText("● Server Offline")
            self.server_status.setStyleSheet(f"color: {COLORS['danger']};")
            self.status_label.setText("⚠️  Server not responding - Running in offline mode")
    
    def center_window(self):
        """Center window on screen"""
        from PyQt6.QtGui import QScreen
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            int((screen.width() - size.width()) / 2),
            int((screen.height() - size.height()) / 2)
        )
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Kotli LIMS",
            f"""
            <b>Kotli LIMS v{APP_CONFIG['app_version']}</b><br>
            Offline-Capable Clinical Laboratory Information Management System<br><br>
            <b>Features:</b>
            • Offline functionality
            • Sample tracking with barcodes
            • Machine integration
            • Professional reports
            • Complete audit trail<br><br>
            Made with ❤️ for Kotli's healthcare
            """
        )
    
    def closeEvent(self, event):
        """Handle window close"""
        reply = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    """Main entry point"""
    app = __import__("PyQt6.QtWidgets", fromlist=["QApplication"]).QApplication(sys.argv)
    
    window = Kotli_LIMS_MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
