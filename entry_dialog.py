from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QPushButton, QComboBox,
    QFrame, QProgressBar, QCheckBox, QSlider
)
from PyQt6.QtCore import Qt
import crypto_utils as cu
from theme import COLORS
CATEGORIES = ["General", "Social", "Finance", "Work", "Shopping", "Email", "Gaming", "Other"]
class EntryDialog(QDialog):
    def __init__(self, parent=None, entry=None, enc_key=None):
        super().__init__(parent)
        self.enc_key = enc_key
        self.is_editing = entry is not None
        self.entry = entry or {}
        self.build_ui()
        if self.is_editing:
            self.populate_fields(entry)
    def build_ui(self):
        title_text = "Edit Entry" if self.is_editing else "New Entry"
        self.setWindowTitle(title_text)
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMaximumWidth(560)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)
        title = QLabel(title_text)
        title.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {COLORS['text_primary']};")
        layout.addWidget(title)
        info = QLabel("All data is encrypted with AES-256-GCM before storage.")
        info.setStyleSheet(f"font-size: 11px; color: {COLORS['text_second']};")
        layout.addWidget(info)
        layout.addWidget(self.make_divider())
        row = QHBoxLayout()
        site_col = QVBoxLayout()
        site_col.addWidget(self.make_label("Site / App Name"))
        self.input_site = QLineEdit()
        self.input_site.setPlaceholderText("e.g. GitHub")
        self.input_site.setFixedHeight(40)
        site_col.addWidget(self.input_site)
        row.addLayout(site_col, 2)
        row.addSpacing(12)
        cat_col = QVBoxLayout()
        cat_col.addWidget(self.make_label("Category"))
        self.input_category = QComboBox()
        for category in CATEGORIES:
            self.input_category.addItem(category)
        self.input_category.setFixedHeight(40)
        cat_col.addWidget(self.input_category)
        row.addLayout(cat_col, 1)
        layout.addLayout(row)
        layout.addWidget(self.make_label("URL (optional)"))
        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("https://github.com")
        self.input_url.setFixedHeight(40)
        layout.addWidget(self.input_url)
        layout.addWidget(self.make_label("Username / Email"))
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("user@example.com")
        self.input_username.setFixedHeight(40)
        layout.addWidget(self.input_username)
        layout.addWidget(self.make_label("Password"))
        password_row = QHBoxLayout()
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Enter or generate a password")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setFixedHeight(40)
        self.input_password.textChanged.connect(self.update_strength_bar)
        password_row.addWidget(self.input_password)
        btn_eye = QPushButton("👁")
        btn_eye.setObjectName("btn_icon")
        btn_eye.setFixedSize(40, 40)
        btn_eye.setCheckable(True)
        btn_eye.toggled.connect(
            lambda checked: self.input_password.setEchoMode(
                QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
            )
        )
        password_row.addWidget(btn_eye)
        btn_generate = QPushButton("Generate")
        btn_generate.setObjectName("btn_ghost")
        btn_generate.setFixedHeight(40)
        btn_generate.clicked.connect(self.open_generator)
        password_row.addWidget(btn_generate)
        layout.addLayout(password_row)
        self.strength_bar = QProgressBar()
        self.strength_bar.setFixedHeight(6)
        self.strength_bar.setTextVisible(False)
        self.strength_bar.setRange(0, 100)
        layout.addWidget(self.strength_bar)
        self.lbl_strength = QLabel("")
        self.lbl_strength.setStyleSheet(f"font-size: 11px; color: {COLORS['text_second']};")
        layout.addWidget(self.lbl_strength)
        layout.addWidget(self.make_label("Notes (optional)"))
        self.input_notes = QTextEdit()
        self.input_notes.setPlaceholderText("Any extra information...")
        self.input_notes.setFixedHeight(72)
        layout.addWidget(self.input_notes)
        layout.addWidget(self.make_divider())
        button_row = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("btn_ghost")
        btn_cancel.setFixedHeight(40)
        btn_cancel.clicked.connect(self.reject)
        button_row.addWidget(btn_cancel)
        btn_save = QPushButton("Save Entry")
        btn_save.setFixedHeight(40)
        btn_save.clicked.connect(self.validate_and_save)
        button_row.addWidget(btn_save)
        layout.addLayout(button_row)
        self.lbl_error = QLabel("")
        self.lbl_error.setStyleSheet(f"color: {COLORS['red']}; font-size: 11px;")
        self.lbl_error.hide()
        layout.addWidget(self.lbl_error)
    def make_label(self, text):
        label = QLabel(text)
        label.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {COLORS['text_second']}; letter-spacing: 1px;")
        return label
    def make_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"border: none; border-top: 1px solid {COLORS['border']};")
        return line
    def populate_fields(self, entry):
        self.input_site.setText(entry.get("site_name", ""))
        self.input_url.setText(entry.get("site_url", "") or "")
        self.input_username.setText(entry.get("username", "") or "")
        self.input_notes.setPlainText(entry.get("notes", "") or "")
        index = self.input_category.findText(entry.get("category", "General"))
        if index >= 0:
            self.input_category.setCurrentIndex(index)
        if self.enc_key and entry.get("password_enc"):
            try:
                plain = cu.decrypt_password(entry["password_enc"], self.enc_key)
                self.input_password.setText(plain)
            except Exception:
                self.input_password.setPlaceholderText("(could not decrypt)")
    def update_strength_bar(self, text):
        if not text:
            self.strength_bar.setValue(0)
            self.lbl_strength.setText("")
            return
        score, label = cu.password_strength(text)
        self.strength_bar.setValue(score)
        colour_map = {
            "Weak":        COLORS["red"],
            "Fair":        COLORS["orange"],
            "Strong":      COLORS["yellow"],
            "Very Strong": COLORS["green"],
        }
        colour = colour_map.get(label, COLORS["text_second"])
        self.lbl_strength.setText(f"Strength: <span style='color:{colour}; font-weight:600;'>{label}</span>")
        self.lbl_strength.setTextFormat(Qt.TextFormat.RichText)
    def open_generator(self):
        dialog = GeneratorDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.input_password.setText(dialog.generated_password)
            self.input_password.setEchoMode(QLineEdit.EchoMode.Normal)
    def validate_and_save(self):
        if not self.input_site.text().strip():
            self.lbl_error.setText("Site name is required.")
            self.lbl_error.show()
            return
        if not self.input_password.text():
            self.lbl_error.setText("Password is required.")
            self.lbl_error.show()
            return
        self.lbl_error.hide()
        self.accept()
    def get_data(self):
        return {
            "site_name": self.input_site.text().strip(),
            "site_url":  self.input_url.text().strip(),
            "username":  self.input_username.text().strip(),
            "password":  self.input_password.text(),
            "notes":     self.input_notes.toPlainText().strip(),
            "category":  self.input_category.currentText(),
        }
class GeneratorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.generated_password = ""
        self.build_ui()
        self.generate()
    def build_ui(self):
        self.setWindowTitle("Password Generator")
        self.setModal(True)
        self.setFixedWidth(420)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(14)
        title = QLabel("Password Generator")
        title.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {COLORS['text_primary']};")
        layout.addWidget(title)
        self.lbl_password = QLabel("generating...")
        self.lbl_password.setWordWrap(True)
        self.lbl_password.setStyleSheet(f"""
            font-size: 15px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-weight: 600;
            color: {COLORS['accent']};
            background: {COLORS['bg_input']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            padding: 12px;
            letter-spacing: 1px;
        """)
        layout.addWidget(self.lbl_password)
        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setTextVisible(False)
        self.strength_bar.setFixedHeight(5)
        layout.addWidget(self.strength_bar)
        self.lbl_strength = QLabel("")
        self.lbl_strength.setStyleSheet(f"font-size: 11px; color: {COLORS['text_second']};")
        layout.addWidget(self.lbl_strength)
        length_row = QHBoxLayout()
        length_row.addWidget(QLabel("Length"))
        self.slider_length = QSlider(Qt.Orientation.Horizontal)
        self.slider_length.setRange(8, 64)
        self.slider_length.setValue(20)
        self.slider_length.valueChanged.connect(self.generate)
        length_row.addWidget(self.slider_length)
        self.lbl_length_value = QLabel("20")
        self.lbl_length_value.setFixedWidth(28)
        self.lbl_length_value.setStyleSheet(f"color: {COLORS['accent']}; font-weight: 600;")
        length_row.addWidget(self.lbl_length_value)
        layout.addLayout(length_row)
        self.chk_upper   = self.make_checkbox("Uppercase letters (A-Z)", True)
        self.chk_lower   = self.make_checkbox("Lowercase letters (a-z)", True)
        self.chk_digits  = self.make_checkbox("Numbers (0-9)", True)
        self.chk_symbols = self.make_checkbox("Symbols (!@#...)", True)
        self.chk_ambig   = self.make_checkbox("Exclude similar characters (0, O, l, I)", False)
        for checkbox in [self.chk_upper, self.chk_lower, self.chk_digits, self.chk_symbols, self.chk_ambig]:
            checkbox.stateChanged.connect(self.generate)
            layout.addWidget(checkbox)
        button_row = QHBoxLayout()
        btn_regen = QPushButton("↻  Regenerate")
        btn_regen.setObjectName("btn_ghost")
        btn_regen.setFixedHeight(40)
        btn_regen.clicked.connect(self.generate)
        button_row.addWidget(btn_regen)
        btn_use = QPushButton("Use This Password")
        btn_use.setFixedHeight(40)
        btn_use.clicked.connect(self.accept)
        button_row.addWidget(btn_use)
        layout.addLayout(button_row)
    def make_checkbox(self, text, checked):
        checkbox = QCheckBox(text)
        checkbox.setChecked(checked)
        return checkbox
    def generate(self):
        length = self.slider_length.value()
        self.lbl_length_value.setText(str(length))
        password = cu.generate_password(
            length          = length,
            use_upper       = self.chk_upper.isChecked(),
            use_lower       = self.chk_lower.isChecked(),
            use_digits      = self.chk_digits.isChecked(),
            use_symbols     = self.chk_symbols.isChecked(),
            exclude_ambiguous = self.chk_ambig.isChecked()
        )
        self.generated_password = password
        self.lbl_password.setText(password)
        score, label = cu.password_strength(password)
        self.strength_bar.setValue(score)
        colour_map = {
            "Weak":        COLORS["red"],
            "Fair":        COLORS["orange"],
            "Strong":      COLORS["yellow"],
            "Very Strong": COLORS["green"],
        }
        colour = colour_map.get(label, COLORS["text_second"])
        self.lbl_strength.setText(f"Strength: <span style='color:{colour}; font-weight:600;'>{label}</span>")
        self.lbl_strength.setTextFormat(Qt.TextFormat.RichText)
