"""
PyQt6 Configuration and Theme Settings
Modern Dark Theme - Easy on Eyes for Lab Technicians
"""

# ============================================================================
# COLOR SCHEME - Modern Dark Clinical Theme
# ============================================================================

COLORS = {
    # Primary Colors
    "primary": "#2E86DE",          # Professional Blue
    "primary_light": "#54A0FF",    # Light Blue
    "primary_dark": "#1B5CB3",     # Dark Blue
    
    # Semantic Colors
    "success": "#26A65B",          # Green
    "warning": "#F39C12",          # Orange
    "error": "#E74C3C",            # Red
    "danger": "#C0392B",           # Dark Red
    "info": "#3498DB",             # Light Blue
    
    # Background Colors
    "bg_dark": "#1A1A2E",          # Very Dark Background
    "bg_darker": "#0F3460",        # Even Darker Background
    "bg_card": "#2A3F5F",          # Card/Panel Background
    "bg_hover": "#3A4F7F",         # Hover Background
    
    # Text Colors
    "text_primary": "#FFFFFF",     # White Text
    "text_secondary": "#B0B0B0",   # Gray Text
    "text_muted": "#808080",       # Muted Gray
    
    # Status Colors
    "normal": "#26A65B",           # Green (Normal Result)
    "abnormal": "#F39C12",         # Orange (Abnormal Result)
    "critical": "#E74C3C",         # Red (Critical Result)
    
    # Borders
    "border": "#404040",           # Dark Border
    "separator": "#505050",        # Separator Line
}

# ============================================================================
# TYPOGRAPHY
# ============================================================================

FONTS = {
    "title": {
        "family": "Segoe UI, Arial, sans-serif",
        "size": 24,
        "weight": "bold",
        "color": COLORS["text_primary"]
    },
    "heading": {
        "family": "Segoe UI, Arial, sans-serif",
        "size": 18,
        "weight": "bold",
        "color": COLORS["text_primary"]
    },
    "subheading": {
        "family": "Segoe UI, Arial, sans-serif",
        "size": 14,
        "weight": "600",
        "color": COLORS["text_primary"]
    },
    "body": {
        "family": "Segoe UI, Arial, sans-serif",
        "size": 12,
        "color": COLORS["text_primary"]
    },
    "small": {
        "family": "Segoe UI, Arial, sans-serif",
        "size": 10,
        "color": COLORS["text_secondary"]
    },
    "mono": {
        "family": "Courier New, monospace",
        "size": 11,
        "color": COLORS["text_primary"]
    }
}

# ============================================================================
# DIMENSIONS
# ============================================================================

DIMENSIONS = {
    "window_min_width": 1200,
    "window_min_height": 800,
    "sidebar_width": 250,
    "header_height": 60,
    "button_height": 40,
    "input_height": 36,
    "spacing": 12,
    "border_radius": 6,
    "shadow_blur": 10,
}

# ============================================================================
# BUTTON STYLES
# ============================================================================

BUTTON_STYLES = {
    "primary": f"""
        QPushButton {{
            background-color: {COLORS['primary']};
            color: {COLORS['text_primary']};
            border: none;
            border-radius: {DIMENSIONS['border_radius']}px;
            padding: 8px 16px;
            font-size: 12px;
            font-weight: bold;
            min-height: {DIMENSIONS['button_height']}px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['primary_light']};
        }}
        QPushButton:pressed {{
            background-color: {COLORS['primary_dark']};
        }}
        QPushButton:disabled {{
            background-color: {COLORS['bg_card']};
            color: {COLORS['text_muted']};
        }}
    """,
    
    "secondary": f"""
        QPushButton {{
            background-color: {COLORS['bg_card']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: {DIMENSIONS['border_radius']}px;
            padding: 8px 16px;
            font-size: 12px;
            min-height: {DIMENSIONS['button_height']}px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['bg_hover']};
            border-color: {COLORS['primary']};
        }}
        QPushButton:pressed {{
            background-color: {COLORS['primary_dark']};
        }}
        QPushButton:disabled {{
            background-color: {COLORS['bg_card']};
            color: {COLORS['text_muted']};
            border-color: {COLORS['border']};
        }}
    """,
    
    "success": f"""
        QPushButton {{
            background-color: {COLORS['success']};
            color: {COLORS['text_primary']};
            border: none;
            border-radius: {DIMENSIONS['border_radius']}px;
            padding: 8px 16px;
            font-size: 12px;
            font-weight: bold;
            min-height: {DIMENSIONS['button_height']}px;
        }}
        QPushButton:hover {{
            background-color: #2DB863;
        }}
        QPushButton:pressed {{
            background-color: #20844B;
        }}
    """,
    
    "danger": f"""
        QPushButton {{
            background-color: {COLORS['danger']};
            color: {COLORS['text_primary']};
            border: none;
            border-radius: {DIMENSIONS['border_radius']}px;
            padding: 8px 16px;
            font-size: 12px;
            font-weight: bold;
            min-height: {DIMENSIONS['button_height']}px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['error']};
        }}
        QPushButton:pressed {{
            background-color: #A93226;
        }}
    """,
}

# ============================================================================
# INPUT FIELD STYLES
# ============================================================================

INPUT_STYLE = f"""
    QLineEdit, QTextEdit, QComboBox {{
        background-color: {COLORS['bg_card']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        border-radius: {DIMENSIONS['border_radius']}px;
        padding: 8px 12px;
        font-size: 12px;
        min-height: {DIMENSIONS['input_height']}px;
        selection-background-color: {COLORS['primary']};
    }}
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
        border: 2px solid {COLORS['primary']};
    }}
    QLineEdit:disabled, QTextEdit:disabled, QComboBox:disabled {{
        background-color: {COLORS['bg_darker']};
        color: {COLORS['text_muted']};
        border-color: {COLORS['border']};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}
    QComboBox::down-arrow {{
        image: url(:/icons/chevron-down.png);
        width: 16px;
        height: 16px;
    }}
"""

# ============================================================================
# TABLE STYLES
# ============================================================================

TABLE_STYLE = f"""
    QTableWidget {{
        background-color: {COLORS['bg_card']};
        alternate-background-color: {COLORS['bg_darker']};
        gridline-color: {COLORS['separator']};
        border: 1px solid {COLORS['border']};
    }}
    QTableWidget::item {{
        padding: 6px;
        border: none;
    }}
    QTableWidget::item:selected {{
        background-color: {COLORS['primary']};
    }}
    QHeaderView::section {{
        background-color: {COLORS['bg_darker']};
        color: {COLORS['text_primary']};
        padding: 6px;
        border: none;
        border-right: 1px solid {COLORS['border']};
        border-bottom: 1px solid {COLORS['border']};
        font-weight: bold;
    }}
    QHeaderView::section:hover {{
        background-color: {COLORS['bg_hover']};
    }}
"""

# ============================================================================
# MAIN WINDOW STYLE
# ============================================================================

MAIN_WINDOW_STYLE = f"""
    QMainWindow {{
        background-color: {COLORS['bg_dark']};
    }}
    QFrame {{
        background-color: {COLORS['bg_dark']};
        color: {COLORS['text_primary']};
    }}
    QLabel {{
        color: {COLORS['text_primary']};
    }}
    QDialog {{
        background-color: {COLORS['bg_dark']};
    }}
    QMessageBox {{
        background-color: {COLORS['bg_dark']};
    }}
    QMenuBar {{
        background-color: {COLORS['bg_card']};
        color: {COLORS['text_primary']};
        border-bottom: 1px solid {COLORS['border']};
    }}
    QMenuBar::item:selected {{
        background-color: {COLORS['primary']};
    }}
    QMenu {{
        background-color: {COLORS['bg_card']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
    }}
    QMenu::item:selected {{
        background-color: {COLORS['primary']};
    }}
    QScrollBar:vertical {{
        background-color: {COLORS['bg_darker']};
        width: 10px;
    }}
    QScrollBar::handle:vertical {{
        background-color: {COLORS['border']};
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: {COLORS['primary']};
    }}
"""

# ============================================================================
# CARD STYLE (For grouped content)
# ============================================================================

CARD_STYLE = f"""
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: {DIMENSIONS['border_radius']}px;
    padding: 12px;
"""

# ============================================================================
# ICON PATHS (Future use)
# ============================================================================

ICONS = {
    "home": ":/icons/home.png",
    "sample": ":/icons/sample.png",
    "test": ":/icons/test.png",
    "result": ":/icons/result.png",
    "report": ":/icons/report.png",
    "user": ":/icons/user.png",
    "settings": ":/icons/settings.png",
    "export": ":/icons/export.png",
    "check": ":/icons/check.png",
    "close": ":/icons/close.png",
    "plus": ":/icons/plus.png",
    "delete": ":/icons/delete.png",
    "edit": ":/icons/edit.png",
    "search": ":/icons/search.png",
    "filter": ":/icons/filter.png",
    "print": ":/icons/print.png",
}

# ============================================================================
# ANIMATION SETTINGS
# ============================================================================

ANIMATIONS = {
    "fade_in_duration": 300,        # milliseconds
    "fade_out_duration": 300,
    "slide_duration": 350,
    "bounce_duration": 500,
}

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================

APP_CONFIG = {
    "app_name": "Kotli LIMS",
    "app_version": "1.0.0",
    "organization": "LocalMarketSoftwares",
    "api_url": "http://127.0.0.1:8000",
    "timeout": 30,  # seconds
    "session_timeout": 1800,  # 30 minutes
    "auto_logout": True,
    "remember_me": True,
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_qss_stylesheet():
    """Get complete QSS stylesheet for application"""
    return f"""
        {MAIN_WINDOW_STYLE}
        {INPUT_STYLE}
        {TABLE_STYLE}
    """


def get_color(status: str) -> str:
    """Get color based on status"""
    status_map = {
        "normal": COLORS["success"],
        "abnormal": COLORS["warning"],
        "critical": COLORS["danger"],
        "pending": COLORS["info"],
        "approved": COLORS["success"],
        "rejected": COLORS["danger"],
    }
    return status_map.get(status.lower(), COLORS["text_secondary"])
