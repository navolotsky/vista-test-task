from PyQt5.QtWidgets import QMessageBox


def show_db_conn_err_msg(parent):
    QMessageBox.critical(parent, "Телефонная книжка",
                         "Не удалось соединиться с базой данных. Попробуйте позже или проверьте настройки.")


def show_not_implemented_msg(parent):
    QMessageBox.information(parent, "Телефонная книжка", "Очень жаль, но пока не реализовано.")
