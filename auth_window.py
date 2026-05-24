from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QPainterPath, QLinearGradient, QColor, QPen
import database as db
import crypto_utils as cu
from theme import COLORS
class ShieldLogo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(72, 72)
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        shield = QPainterPath()
        shield.moveTo(36, 4)
        shield.lineTo(64, 16)
        shield.lineTo(64, 38)
        shield.cubicTo(64, 56, 50, 66, 36, 70)
        shield.cubicTo(22, 66, 8, 56, 8, 38)
        shield.lineTo(8, 16)
        shield.closeSubpath()
        gradient = QLinearGradient(0, 0, 0, 72)
        gradient.setColorAt(0, QColor(COLORS["accent"]))
        gradient.setColorAt(1, QColor(COLORS["accent_dark"]))
        painter.fillPath(shield, gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawRoundedRect(24, 36, 24, 18, 3, 3)
        pen = QPen(QColor("#FFFFFF"), 3)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        arc = QPainterPath()
        arc.addEllipse(28, 26, 16, 16)
        painter.drawPath(arc)
        painter.end()
class AuthWindow(QWidget):
    login_successful = pyqtSignal(int, bytes)
    def __init__(self):
        super().__init__()
        self.is_register_mode = False
        self.build_ui()
        self.check_which_mode()
    def build_ui(self):
        self.setWindowTitle("PassSafe")
        self.setMinimumSize(440, 580)
        self.setMaximumSize(440, 640)
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet(f"""
            QFrame
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['bg_panel']},
                    stop:1 {COLORS['bg_deep']});
                border: 1px solid {COLORS['border']};
                border-radius: 20px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(48, 48, 48, 48)
        card_layout.setSpacing(0)
        logo_row = QHBoxLayout()
        logo_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_row.addWidget(ShieldLogo())
        card_layout.addLayout(logo_row)
        card_layout.addSpacing(20)
        app_name = QLabel("PassSafe")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_name.setStyleSheet(f"font-size: 26px; font-weight: 700; color: {COLORS['text_primary']}; letter-spacing: 2px;")
        card_layout.addWidget(app_name)
        card_layout.addSpacing(4)
        tagline = QLabel("Your secrets, encrypted & safe.")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline.setStyleSheet(f"font-size: 12px; color: {COLORS['text_second']};")
        card_layout.addWidget(tagline)
        card_layout.addSpacing(36)
        self.lbl_heading = QLabel("Welcome back")
        self.lbl_heading.setStyleSheet(f"font-size: 16px; font-weight: 600; color: {COLORS['text_primary']};")
        card_layout.addWidget(self.lbl_heading)
        card_layout.addSpacing(4)
        self.lbl_subheading = QLabel("Enter your master password to unlock the vault.")
        self.lbl_subheading.setStyleSheet(f"font-size: 12px; color: {COLORS['text_second']};")
        self.lbl_subheading.setWordWrap(True)
        card_layout.addWidget(self.lbl_subheading)
        card_layout.addSpacing(24)
        self.lbl_username = QLabel("Username")
        self.lbl_username.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {COLORS['text_second']}; letter-spacing: 1px;")
        card_layout.addWidget(self.lbl_username)
        card_layout.addSpacing(6)
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Choose a username")
        self.input_username.setFixedHeight(42)
        card_layout.addWidget(self.input_username)
        card_layout.addSpacing(14)
        lbl_password = QLabel("Master Password")
        lbl_password.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {COLORS['text_second']}; letter-spacing: 1px;")
        card_layout.addWidget(lbl_password)
        card_layout.addSpacing(6)
        password_row = QHBoxLayout()
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Enter master password")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setFixedHeight(42)
        self.input_password.returnPressed.connect(self.handle_submit)
        password_row.addWidget(self.input_password)
        btn_eye = QPushButton("👁")
        btn_eye.setObjectName("btn_icon")
        btn_eye.setFixedSize(42, 42)
        btn_eye.setCheckable(True)
        btn_eye.toggled.connect(self.toggle_password_visibility)
        password_row.addWidget(btn_eye)
        card_layout.addLayout(password_row)
        card_layout.addSpacing(8)
        self.lbl_confirm = QLabel("Confirm Password")
        self.lbl_confirm.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {COLORS['text_second']}; letter-spacing: 1px;")
        card_layout.addWidget(self.lbl_confirm)
        card_layout.addSpacing(6)
        self.input_confirm = QLineEdit()
        self.input_confirm.setPlaceholderText("Re-enter master password")
        self.input_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_confirm.setFixedHeight(42)
        card_layout.addWidget(self.input_confirm)
        card_layout.addSpacing(24)
        self.lbl_error = QLabel("")
        self.lbl_error.setStyleSheet(f"color: {COLORS['red']}; font-size: 12px;")
        self.lbl_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_error.hide()
        card_layout.addWidget(self.lbl_error)
        card_layout.addSpacing(4)
        self.btn_submit = QPushButton("Unlock Vault")
        self.btn_submit.setFixedHeight(46)
        self.btn_submit.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLORS['accent']}, stop:1 {COLORS['accent_light']});
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background: {COLORS['accent_light']};
            }}
            QPushButton:pressed {{
                background: {COLORS['accent_dark']};
            }}
        """)
        self.btn_submit.clicked.connect(self.handle_submit)
        card_layout.addWidget(self.btn_submit)
        card_layout.addSpacing(16)
        self.btn_switch = QPushButton("New to PassSafe? Create your vault →")
        self.btn_switch.setFlat(True)
        self.btn_switch.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {COLORS['accent']};
                border: none;
                font-size: 12px;
            }}
            QPushButton:hover {{ color: {COLORS['accent_light']}; }}
        """)
        self.btn_switch.clicked.connect(self.switch_mode)
        card_layout.addWidget(self.btn_switch, alignment=Qt.AlignmentFlag.AlignCenter)
        root_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
    def check_which_mode(self):
        if not db.master_user_exists():
            self.set_mode(register=True)
    def set_mode(self, register):
        self.is_register_mode = register
        self.lbl_username.setVisible(register)
        self.input_username.setVisible(register)
        self.lbl_confirm.setVisible(register)
        self.input_confirm.setVisible(register)
        if register:
            self.lbl_heading.setText("Create your vault")
            self.lbl_subheading.setText("Set a strong master password. It cannot be recovered if forgotten.")
            self.btn_submit.setText("Create Vault")
            self.btn_switch.setText("Already have a vault? Sign in →")
        else:
            self.lbl_heading.setText("Welcome back")
            self.lbl_subheading.setText("Enter your master password to unlock the vault.")
            self.btn_submit.setText("Unlock Vault")
            self.btn_switch.setText("New to PassSafe? Create your vault →")
        self.lbl_error.hide()
    def switch_mode(self):
        self.set_mode(not self.is_register_mode)
    def toggle_password_visibility(self, is_checked):
        if is_checked:
            self.input_password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.input_confirm.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.input_confirm.setEchoMode(QLineEdit.EchoMode.Password)
    def show_error(self, message):
        self.lbl_error.setText(message)
        self.lbl_error.show()
    def handle_submit(self):
        self.lbl_error.hide()
        password = self.input_password.text().strip()
        if not password:
            self.show_error("Please enter your master password.")
            return
        if self.is_register_mode:
            self.register(password)
        else:
            self.login(password)
    def register(self, password):
        username = self.input_username.text().strip()
        confirm  = self.input_confirm.text().strip()
        if not username:
            self.show_error("Please choose a username.")
            return
        if len(password) < 8:
            self.show_error("Password must be at least 8 characters.")
            return
        if password != confirm:
            self.show_error("Passwords do not match.")
            return
        try:
            password_hash, salt = cu.hash_master_password(password)
            user_id = db.create_master_user(username, password_hash, salt)
            encryption_key = cu.derive_key(password, salt)
            self.login_successful.emit(user_id, encryption_key)
        except Exception as error:
            self.show_error(f"Registration failed: {error}")
    def login(self, password):
        try:
            user = db.get_first_user()
            if not user:
                self.show_error("No vault found. Please create one first.")
                return
            if cu.verify_master_password(password, user["password_hash"], user["salt"]):
                encryption_key = cu.derive_key(password, bytes(user["salt"]))
                self.login_successful.emit(user["id"], encryption_key)
            else:
                self.show_error("Incorrect master password.")
        except Exception as error:
            self.show_error(f"Login error: {error}")
