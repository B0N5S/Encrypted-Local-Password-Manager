import csv
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QFrame, QFileDialog,
    QMessageBox, QAbstractItemView, QApplication, QDialog
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
import database as db
import crypto_utils as cu
from entry_dialog import EntryDialog
from theme import COLORS
CATEGORY_ICONS = {
    "General":  "🔑",
    "Social":   "💬",
    "Finance":  "💳",
    "Work":     "💼",
    "Shopping": "🛒",
    "Email":    "📧",
    "Gaming":   "🎮",
    "Other":    "📦",
}
class SidebarButton(QPushButton):
    def __init__(self, icon, label, parent=None):
        super().__init__(f"  {icon}  {label}", parent)
        self.setCheckable(True)
        self.setFixedHeight(44)
        self.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 0 16px;
                border: none;
                border-radius: 8px;
                color: {COLORS['text_second']};
                font-size: 13px;
                background: transparent;
            }}
            QPushButton:hover {{
                background: {COLORS['bg_hover']};
                color: {COLORS['text_primary']};
            }}
            QPushButton:checked {{
                background: {COLORS['bg_hover']};
                color: {COLORS['accent']};
                font-weight: 600;
            }}
        """)
class VaultWindow(QMainWindow):
    def __init__(self, user_id, enc_key):
        super().__init__()
        self.user_id = user_id
        self.enc_key = enc_key
        self.all_entries = []
        self.current_category = "All"
        self.clipboard_timer = None
        self.build_ui()
        self.load_entries()
    def build_ui(self):
        self.setWindowTitle("PassSafe — Vault")
        self.resize(1100, 700)
        self.setMinimumSize(900, 580)
        central = QWidget()
        self.setCentralWidget(central)
        main_row = QHBoxLayout(central)
        main_row.setContentsMargins(0, 0, 0, 0)
        main_row.setSpacing(0)
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 24, 16, 24)
        sidebar_layout.setSpacing(4)
        logo_row = QHBoxLayout()
        logo_row.addWidget(QLabel("🛡", styleSheet="font-size: 22px;"))
        logo_label = QLabel("PassSafe")
        logo_label.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {COLORS['text_primary']}; letter-spacing: 1px;")
        logo_row.addWidget(logo_label)
        logo_row.addStretch()
        sidebar_layout.addLayout(logo_row)
        sidebar_layout.addSpacing(24)
        filter_label = QLabel("FILTER")
        filter_label.setStyleSheet(f"font-size: 10px; font-weight: 600; color: {COLORS['text_muted']}; letter-spacing: 2px; padding-left: 8px;")
        sidebar_layout.addWidget(filter_label)
        sidebar_layout.addSpacing(6)
        self.category_buttons = []
        btn_all = SidebarButton("🗂", "All Passwords")
        btn_all.setChecked(True)
        btn_all.clicked.connect(lambda: self.filter_by_category("All"))
        sidebar_layout.addWidget(btn_all)
        self.category_buttons.append(("All", btn_all))
        for category, icon in CATEGORY_ICONS.items():
            btn = SidebarButton(icon, category)
            btn.clicked.connect(lambda checked, c=category: self.filter_by_category(c))
            sidebar_layout.addWidget(btn)
            self.category_buttons.append((category, btn))
        sidebar_layout.addStretch()
        stats_box = QFrame()
        stats_box.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: 10px;
            }}
        """)
        stats_layout = QVBoxLayout(stats_box)
        stats_layout.setContentsMargins(12, 12, 12, 12)
        stats_layout.setSpacing(4)
        self.lbl_count = QLabel("0 passwords")
        self.lbl_count.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {COLORS['text_primary']};")
        stats_layout.addWidget(self.lbl_count)
        stored_label = QLabel("stored in vault")
        stored_label.setStyleSheet(f"font-size: 11px; color: {COLORS['text_second']};")
        stats_layout.addWidget(stored_label)
        sidebar_layout.addWidget(stats_box)
        sidebar_layout.addSpacing(12)
        btn_lock = QPushButton("🔒  Lock Vault")
        btn_lock.setObjectName("btn_ghost")
        btn_lock.setFixedHeight(40)
        btn_lock.clicked.connect(self.lock_vault)
        sidebar_layout.addWidget(btn_lock)
        main_row.addWidget(sidebar)
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 28, 32, 24)
        content_layout.setSpacing(0)
        top_bar = QHBoxLayout()
        self.lbl_page_title = QLabel("All Passwords")
        self.lbl_page_title.setStyleSheet(f"font-size: 22px; font-weight: 700; color: {COLORS['text_primary']};")
        top_bar.addWidget(self.lbl_page_title)
        top_bar.addStretch()
        self.input_search = QLineEdit()
        self.input_search.setPlaceholderText("🔍  Search passwords...")
        self.input_search.setFixedWidth(260)
        self.input_search.setFixedHeight(38)
        self.input_search.textChanged.connect(self.on_search_changed)
        top_bar.addWidget(self.input_search)
        top_bar.addSpacing(10)
        btn_import = QPushButton("⬆  Import")
        btn_import.setObjectName("btn_ghost")
        btn_import.setFixedHeight(38)
        btn_import.clicked.connect(self.import_csv)
        top_bar.addWidget(btn_import)
        btn_export = QPushButton("⬇  Export")
        btn_export.setObjectName("btn_ghost")
        btn_export.setFixedHeight(38)
        btn_export.clicked.connect(self.export_csv)
        top_bar.addWidget(btn_export)
        top_bar.addSpacing(10)
        btn_add = QPushButton("＋  New Entry")
        btn_add.setFixedHeight(38)
        btn_add.clicked.connect(self.add_entry)
        top_bar.addWidget(btn_add)
        content_layout.addLayout(top_bar)
        content_layout.addSpacing(20)
        self.lbl_status = QLabel("")
        self.lbl_status.setStyleSheet(f"""
            color: {COLORS['green']};
            font-size: 12px;
            font-weight: 600;
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['green']};
            border-radius: 6px;
            padding: 6px 14px;
        """)
        self.lbl_status.hide()
        content_layout.addWidget(self.lbl_status)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["", "Site / App", "Username", "Category", "Last Updated", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 36)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 130)
        self.table.setColumnWidth(5, 180)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setDefaultSectionSize(52)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        content_layout.addWidget(self.table)
        self.lbl_empty = QLabel("No passwords yet.\nClick '＋ New Entry' to add your first one.")
        self.lbl_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_empty.setStyleSheet(f"font-size: 14px; color: {COLORS['text_muted']}; line-height: 1.6;")
        self.lbl_empty.hide()
        content_layout.addWidget(self.lbl_empty, alignment=Qt.AlignmentFlag.AlignCenter)
        main_row.addWidget(content)
    def load_entries(self, search_query=""):
        if search_query:
            entries = db.search_entries(self.user_id, search_query)
        else:
            self.all_entries = db.get_all_entries(self.user_id)
            entries = list(self.all_entries)
        if self.current_category != "All" and not search_query:
            entries = [e for e in entries if e["category"] == self.current_category]
        self.display_entries(entries)
        total = len(self.all_entries)
        self.lbl_count.setText(f"{total} password{'s' if total != 1 else ''}")
    def display_entries(self, entries):
        self.table.setRowCount(0)
        if not entries:
            self.table.hide()
            self.lbl_empty.show()
            return
        self.lbl_empty.hide()
        self.table.show()
        self.table.setRowCount(len(entries))
        for row_index, entry in enumerate(entries):
            icon = CATEGORY_ICONS.get(entry.get("category", "General"), "🔑")
            icon_item = QTableWidgetItem(icon)
            icon_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_item.setFont(QFont("Segoe UI Emoji", 16))
            self.table.setItem(row_index, 0, icon_item)
            site_item = QTableWidgetItem(entry["site_name"])
            site_item.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
            self.table.setItem(row_index, 1, site_item)
            user_item = QTableWidgetItem(entry.get("username") or "—")
            user_item.setForeground(QColor(COLORS["text_second"]))
            self.table.setItem(row_index, 2, user_item)
            cat_item = QTableWidgetItem(entry.get("category", "General"))
            cat_item.setForeground(QColor(COLORS["text_second"]))
            self.table.setItem(row_index, 3, cat_item)
            updated = entry.get("updated_at") or entry.get("created_at") or ""
            date_str = str(updated)[:10] if updated else "—"
            date_item = QTableWidgetItem(date_str)
            date_item.setForeground(QColor(COLORS["text_muted"]))
            self.table.setItem(row_index, 4, date_item)
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(4, 4, 4, 4)
            btn_layout.setSpacing(4)
            btn_copy = QPushButton("📋 Copy")
            btn_copy.setFixedHeight(32)
            btn_copy.setStyleSheet(f"""
                QPushButton {{
                    background: {COLORS['bg_hover']};
                    color: {COLORS['accent']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 6px;
                    font-size: 11px;
                    font-weight: 600;
                    padding: 0 10px;
                }}
                QPushButton:hover {{
                    background: {COLORS['accent']};
                    color: white;
                }}
            """)
            btn_copy.clicked.connect(lambda checked, e=entry: self.copy_password(e))
            btn_layout.addWidget(btn_copy)
            btn_edit = QPushButton("✏")
            btn_edit.setObjectName("btn_icon")
            btn_edit.setFixedSize(32, 32)
            btn_edit.setToolTip("Edit entry")
            btn_edit.clicked.connect(lambda checked, e=entry: self.edit_entry(e))
            btn_layout.addWidget(btn_edit)
            btn_delete = QPushButton("🗑")
            btn_delete.setObjectName("btn_icon")
            btn_delete.setFixedSize(32, 32)
            btn_delete.setToolTip("Delete entry")
            btn_delete.setStyleSheet(btn_delete.styleSheet() + f"QPushButton:hover {{ color: {COLORS['red']}; }}")
            btn_delete.clicked.connect(lambda checked, e=entry: self.delete_entry(e))
            btn_layout.addWidget(btn_delete)
            self.table.setCellWidget(row_index, 5, btn_widget)
    def filter_by_category(self, category):
        self.current_category = category
        self.lbl_page_title.setText("All Passwords" if category == "All" else category)
        for cat, btn in self.category_buttons:
            btn.setChecked(cat == category)
        self.load_entries(self.input_search.text())
    def on_search_changed(self, text):
        self.load_entries(text)
    def add_entry(self):
        dialog = EntryDialog(self, enc_key=self.enc_key)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            encrypted = cu.encrypt_password(data["password"], self.enc_key)
            db.add_vault_entry(
                self.user_id,
                data["site_name"],
                data["site_url"],
                data["username"],
                encrypted,
                data["notes"],
                data["category"]
            )
            self.load_entries()
            self.show_status(f"✓  '{data['site_name']}' added successfully.")
    def edit_entry(self, entry):
        dialog = EntryDialog(self, entry=entry, enc_key=self.enc_key)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            encrypted = cu.encrypt_password(data["password"], self.enc_key)
            db.update_vault_entry(
                entry["id"],
                data["site_name"],
                data["site_url"],
                data["username"],
                encrypted,
                data["notes"],
                data["category"]
            )
            self.load_entries()
            self.show_status(f"✓  '{data['site_name']}' updated.")
    def delete_entry(self, entry):
        answer = QMessageBox.question(
            self,
            "Delete Entry",
            f"Delete '{entry['site_name']}'? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
        )
        if answer == QMessageBox.StandardButton.Yes:
            db.delete_vault_entry(entry["id"])
            self.load_entries()
            self.show_status(f"🗑  '{entry['site_name']}' deleted.")
    def copy_password(self, entry):
        try:
            plain_password = cu.decrypt_password(entry["password_enc"], self.enc_key)
            QApplication.clipboard().setText(plain_password)
            self.show_status("📋  Password copied! Clipboard clears in 15 seconds.", clear_after=15)
        except Exception as error:
            QMessageBox.critical(self, "Error", f"Could not decrypt password:\n{error}")
    def show_status(self, message, clear_after=3):
        self.lbl_status.setText(message)
        self.lbl_status.show()
        if self.clipboard_timer:
            self.clipboard_timer.stop()
        if clear_after > 3:
            self.seconds_remaining = clear_after
            timer = QTimer(self)
            def tick():
                self.seconds_remaining -= 1
                if self.seconds_remaining <= 0:
                    QApplication.clipboard().setText("")
                    self.lbl_status.hide()
                    timer.stop()
                else:
                    self.lbl_status.setText(f"📋  Clipboard clears in {self.seconds_remaining}s...")
            timer.timeout.connect(tick)
            timer.start(1000)
            self.clipboard_timer = timer
        else:
            QTimer.singleShot(clear_after * 1000, self.lbl_status.hide)
    def lock_vault(self):
        answer = QMessageBox.question(
            self,
            "Lock Vault",
            "Lock the vault and return to the login screen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
        )
        if answer == QMessageBox.StandardButton.Yes:
            from auth_window import AuthWindow
            self.auth_window = AuthWindow()
            self.auth_window.login_successful.connect(self.on_relogin)
            self.auth_window.show()
            self.close()
    def on_relogin(self, user_id, enc_key):
        new_vault = VaultWindow(user_id, enc_key)
        new_vault.show()
        if hasattr(self, "auth_window"):
            self.auth_window.close()
    def export_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Vault", "passsafe_export.csv", "CSV Files (*.csv)"
        )
        if not file_path:
            return
        try:
            entries = db.get_all_entries(self.user_id)
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["site_name", "site_url", "username", "password", "notes", "category"])
                writer.writeheader()
                for entry in entries:
                    try:
                        plain = cu.decrypt_password(entry["password_enc"], self.enc_key)
                    except Exception:
                        plain = ""
                    writer.writerow({
                        "site_name": entry["site_name"],
                        "site_url":  entry.get("site_url", ""),
                        "username":  entry.get("username", ""),
                        "password":  plain,
                        "notes":     entry.get("notes", ""),
                        "category":  entry.get("category", "General"),
                    })
            QMessageBox.information(
                self,
                "Export Successful",
                f"Vault exported to:\n{file_path}\n\n"
                "⚠  This file contains plain-text passwords. Keep it secure."
            )
        except Exception as error:
            QMessageBox.critical(self, "Export Failed", str(error))
    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import CSV", "", "CSV Files (*.csv)"
        )
        if not file_path:
            return
        try:
            imported_count = 0
            with open(file_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    site = row.get("site_name") or row.get("name", "")
                    if not site:
                        continue
                    plain_password = row.get("password", "")
                    encrypted = cu.encrypt_password(plain_password, self.enc_key)
                    db.add_vault_entry(
                        self.user_id,
                        site,
                        row.get("site_url") or row.get("url", ""),
                        row.get("username", ""),
                        encrypted,
                        row.get("notes", ""),
                        row.get("category", "General")
                    )
                    imported_count += 1
            self.load_entries()
            QMessageBox.information(
                self,
                "Import Successful",
                f"Imported {imported_count} entries into your vault."
            )
        except Exception as error:
            QMessageBox.critical(self, "Import Failed", str(error))
