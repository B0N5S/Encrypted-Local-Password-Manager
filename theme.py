"""
PassSafe - Theme & Stylesheet
Central dark theme definition for all PyQt6 widgets.
"""
COLORS = {
    "bg_deep":      "#0A0C14",
    "bg_panel":     "#111520",
    "bg_card":      "#161B2E",
    "bg_input":     "#1C2338",
    "bg_hover":     "#1E2540",
    "accent":       "#4F8EF7",
    "accent_light": "#7AAEFF",
    "accent_dark":  "#2D5FC4",
    "green":        "#3DDC84",
    "red":          "#FF5370",
    "orange":       "#FFB347",
    "yellow":       "#FFD166",
    "text_primary": "#E8EBF5",
    "text_second":  "#7A84A3",
    "text_muted":   "#404869",
    "border":       "#252D4A",
    "border_focus": "#4F8EF7",
    "scrollbar":    "#252D4A",
}
MAIN_STYLESHEET = f"""
/* ── Global ─────────────────────────────────────────────────────────────── */
QWidget {{
    background-color: {COLORS['bg_deep']};
    color: {COLORS['text_primary']};
    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
    font-size: 13px;
    outline: none;
}}
QMainWindow {{
    background-color: {COLORS['bg_deep']};
}}
/* ── Labels ─────────────────────────────────────────────────────────────── */
QLabel {{
    background: transparent;
    color: {COLORS['text_primary']};
}}
QLabel
    font-size: 28px;
    font-weight: 700;
    color: {COLORS['text_primary']};
    letter-spacing: 1px;
}}
QLabel
    font-size: 13px;
    color: {COLORS['text_second']};
}}
QLabel
    font-size: 11px;
    font-weight: 600;
    color: {COLORS['text_muted']};
    letter-spacing: 2px;
    text-transform: uppercase;
}}
/* ── Inputs ─────────────────────────────────────────────────────────────── */
QLineEdit, QTextEdit, QComboBox {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    selection-background-color: {COLORS['accent']};
}}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
    border: 1px solid {COLORS['border_focus']};
    background-color: {COLORS['bg_hover']};
}}
QLineEdit::placeholder {{
    color: {COLORS['text_muted']};
}}
QComboBox::drop-down {{
    border: none;
    width: 28px;
}}
QComboBox::down-arrow {{
    image: none;
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid {COLORS['text_second']};
}}
QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    selection-background-color: {COLORS['accent']};
    color: {COLORS['text_primary']};
    padding: 4px;
}}
/* ── Buttons ─────────────────────────────────────────────────────────────── */
QPushButton {{
    background-color: {COLORS['accent']};
    color:
    border: none;
    border-radius: 8px;
    padding: 9px 20px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.3px;
}}
QPushButton:hover {{
    background-color: {COLORS['accent_light']};
}}
QPushButton:pressed {{
    background-color: {COLORS['accent_dark']};
}}
QPushButton
    background-color: transparent;
    color: {COLORS['text_second']};
    border: 1px solid {COLORS['border']};
}}
QPushButton
    background-color: {COLORS['bg_hover']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border_focus']};
}}
QPushButton
    background-color: transparent;
    color: {COLORS['red']};
    border: 1px solid {COLORS['red']};
}}
QPushButton
    background-color: {COLORS['red']};
    color:
}}
QPushButton
    background-color: {COLORS['green']};
    color:
}}
QPushButton
    background-color:
}}
QPushButton
    background-color: transparent;
    color: {COLORS['text_second']};
    border: none;
    padding: 6px;
    border-radius: 6px;
    font-size: 16px;
}}
QPushButton
    background-color: {COLORS['bg_hover']};
    color: {COLORS['accent']};
}}
/* ── Table / List ────────────────────────────────────────────────────────── */
QTableWidget {{
    background-color: transparent;
    border: none;
    gridline-color: {COLORS['border']};
    color: {COLORS['text_primary']};
    font-size: 13px;
    outline: none;
}}
QTableWidget::item {{
    padding: 10px 12px;
    border-bottom: 1px solid {COLORS['border']};
}}
QTableWidget::item:selected {{
    background-color: {COLORS['bg_hover']};
    color: {COLORS['text_primary']};
}}
QTableWidget::item:hover {{
    background-color: {COLORS['bg_card']};
}}
QHeaderView::section {{
    background-color: {COLORS['bg_panel']};
    color: {COLORS['text_muted']};
    border: none;
    border-bottom: 1px solid {COLORS['border']};
    padding: 10px 12px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}}
/* ── Scroll bars ─────────────────────────────────────────────────────────── */
QScrollBar:vertical {{
    background: transparent;
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {COLORS['scrollbar']};
    border-radius: 3px;
    min-height: 20px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background: transparent;
    height: 6px;
}}
QScrollBar::handle:horizontal {{
    background: {COLORS['scrollbar']};
    border-radius: 3px;
}}
/* ── Slider ──────────────────────────────────────────────────────────────── */
QSlider::groove:horizontal {{
    height: 4px;
    background: {COLORS['border']};
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: {COLORS['accent']};
    border: none;
    width: 16px;
    height: 16px;
    border-radius: 8px;
    margin: -6px 0;
}}
QSlider::sub-page:horizontal {{
    background: {COLORS['accent']};
    border-radius: 2px;
}}
/* ── CheckBox ────────────────────────────────────────────────────────────── */
QCheckBox {{
    color: {COLORS['text_second']};
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    background: {COLORS['bg_input']};
}}
QCheckBox::indicator:checked {{
    background: {COLORS['accent']};
    border: 1px solid {COLORS['accent']};
}}
/* ── Tooltip ─────────────────────────────────────────────────────────────── */
QToolTip {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 5px 8px;
    font-size: 12px;
}}
/* ── Dialog ──────────────────────────────────────────────────────────────── */
QDialog {{
    background-color: {COLORS['bg_panel']};
}}
/* ── Frame/Panel ─────────────────────────────────────────────────────────── */
QFrame
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
}}
QFrame
    background-color: {COLORS['bg_panel']};
    border-right: 1px solid {COLORS['border']};
}}
/* ── Progress bar (strength meter) ──────────────────────────────────────── */
QProgressBar {{
    background-color: {COLORS['border']};
    border: none;
    border-radius: 3px;
    height: 6px;
    text-align: center;
}}
QProgressBar::chunk {{
    border-radius: 3px;
    background-color: {COLORS['accent']};
}}
QProgressBar[strength="Weak"]::chunk    {{ background-color: {COLORS['red']}; }}
QProgressBar[strength="Fair"]::chunk    {{ background-color: {COLORS['orange']}; }}
QProgressBar[strength="Strong"]::chunk  {{ background-color: {COLORS['yellow']}; }}
QProgressBar[strength="Very Strong"]::chunk {{ background-color: {COLORS['green']}; }}
"""
