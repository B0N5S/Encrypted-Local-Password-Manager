import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QPalette, QColor
import database as db
from theme import MAIN_STYLESHEET, COLORS
from auth_window import AuthWindow
from vault_window import VaultWindow
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PassSafe")
    app.setStyleSheet(MAIN_STYLESHEET)
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window,        QColor(COLORS["bg_deep"]))
    palette.setColor(QPalette.ColorRole.WindowText,    QColor(COLORS["text_primary"]))
    palette.setColor(QPalette.ColorRole.Base,          QColor(COLORS["bg_input"]))
    palette.setColor(QPalette.ColorRole.Text,          QColor(COLORS["text_primary"]))
    palette.setColor(QPalette.ColorRole.Button,        QColor(COLORS["bg_panel"]))
    palette.setColor(QPalette.ColorRole.ButtonText,    QColor(COLORS["text_primary"]))
    palette.setColor(QPalette.ColorRole.Highlight,     QColor(COLORS["accent"]))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))
    app.setPalette(palette)
    try:
        db.initialise_database()
    except Exception as error:
        QMessageBox.critical(
            None,
            "Database Error",
            f"PassSafe could not set up the database.\n\nError: {error}"
        )
        sys.exit(1)
    auth = AuthWindow()
    def on_login_success(user_id, encryption_key):
        vault = VaultWindow(user_id, encryption_key)
        vault.show()
        auth.close()
    auth.login_successful.connect(on_login_success)
    auth.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()
