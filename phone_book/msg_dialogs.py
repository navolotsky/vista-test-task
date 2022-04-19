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
    return msg_box.exec()


def show_not_implemented_msg(parent):
    return QMessageBox.information(parent, "Телефонная книжка", "Очень жаль, но пока не реализовано.")


def show_invalid_input_warning(fields=None, highlighted=False, parent=None):
    field_names = []
    if fields is not None:
        for field in fields:
            try:
                text = field.placeholderText()
                if text:
                    field_names.append(text)
            except AttributeError:
                continue
    message_text = "Пожалуйста, исправьте введенные значения"
    if field_names:
        word = "подсвеченных" if highlighted else "cледующих"
        message_text += " в {} полях:\n\n{}".format(word, "\n".join(field_names))
    elif highlighted:
        message_text += " в подсвеченных полях."
    else:
        message_text += "."
    return QMessageBox.warning(parent, "Телефонная книжка", message_text)
