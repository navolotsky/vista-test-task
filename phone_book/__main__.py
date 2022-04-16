import logging.handlers
import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from .main_win import MainWindow

logger = logging.getLogger("phone_book.__main__")

if __name__ == "__main__":
    # TODO: parse args to set a logger config for debug purposes
    logging.basicConfig()
    parent_logger = logging.getLogger("phone_book")
    parent_logger.setLevel(logging.DEBUG)
    file_handler = logging.handlers.RotatingFileHandler("log.txt", maxBytes=2 ** 19, backupCount=1)
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    parent_logger.addHandler(file_handler)

    sys._original_excepthook = sys.excepthook


    def exception_hook(exctype, value, traceback):
        logger.exception("Unexpected error", exc_info=value)
        sys._original_excepthook(exctype, value, traceback)
        msg_box = QMessageBox(QMessageBox.Critical, "Телефонная книжка",
                              "Неожиданная ошибка. Приложение будет закрыто.")
        msg_box.setDetailedText(str(value))
        msg_box.exec()
        sys.exit(1)

    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
