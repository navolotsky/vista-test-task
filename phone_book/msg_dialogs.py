from typing import Optional

from PyQt5.QtWidgets import QMessageBox


def show_db_conn_err_msg(message: Optional[str] = None, details: Optional[str] = None,
                         critical: bool = False, parent=None):
    icon = QMessageBox.Critical if critical else QMessageBox.Warning
    if message:
        msg_text = message
    else:
        msg_text = "Ошибка конфигурации." if critical else ("Не удалось соединиться с базой данных.\n"
                                                            "Попробуйте позже или проверьте настройки.")
    msg_box = QMessageBox(icon, "Телефонная книжка", msg_text, parent=parent)
    if details:
        msg_box.setDetailedText(details)
    msg_box.exec()


def show_not_implemented_msg(parent):
    QMessageBox.information(parent, "Телефонная книжка", "Очень жаль, но пока не реализовано.")
