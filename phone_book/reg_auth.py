from functools import partial
from types import SimpleNamespace

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLineEdit, QMessageBox

from . import database as db
from .msg_dialogs import show_db_conn_err_msg, show_not_implemented_msg
from .ui import Ui_AuthForm, Ui_RegisterForm


class RegisterForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint)
        self.ui = Ui_RegisterForm()
        self.ui.setupUi(self)
        self.ui.button_box.rejected.connect(self.reject)
        self.ui.button_box.accepted.connect(self.handle_ok_btn_clicked)

        self.result = SimpleNamespace(code=None, username=None, password=None)

    def handle_ok_btn_clicked(self):
        username = self.ui.username_ln_edt.text()
        email = self.ui.email_ln_edt.text()
        birth_date = self.ui.birth_date_dt_edt.date().toString("yyyy.MM.dd")
        # TODO: some input validation
        try:
            self.ui.button_box.button(QDialogButtonBox.Ok).setDisabled(True)
            res_code, password = db.register(username, email, birth_date)
        except db.DatabaseConnectionError as exc:
            show_db_conn_err_msg(details=str(exc), parent=self)
            self.close()
        else:
            self.result.code, self.result.username, self.result.password = res_code, username, password
            if res_code is db.RegisterResult.SUCCESS:
                self.accept()
                # TODO: send a password by an email
                ans = QMessageBox.question(
                    self, "Телефонная книжка",
                    "Регистрация успешна.\n"
                    "Ваш пароль выслан [! не реализовано] на указанную почту.\n"
                    "Скопировать в буфер обмена?")
                if ans == QMessageBox.Yes:
                    QApplication.clipboard().setText(password)
            elif res_code is db.RegisterResult.USERNAME_EXISTS:
                self.ui.username_ln_edt.setFocus()
                QMessageBox.warning(self, "Телефонная книжка", "Пользователь с таким именем уже существует.")
            elif res_code is db.RegisterResult.EMAIL_EXISTS:
                self.ui.email_ln_edt.setFocus()
                QMessageBox.warning(self, "Телефонная книжка", "Пользователь с таким e-mail уже существует.")
            elif res_code is db.RegisterResult.UNKNOWN_ERROR:
                QMessageBox.critical(self, "Телефонная книжка", "Возникла непредвиденная ошибка.")
                self.close()
            else:
                raise RuntimeError("unknown member: {}".format(res_code))
        finally:
            self.ui.button_box.button(QDialogButtonBox.Ok).setEnabled(True)


class AuthForm(QDialog):
    def __init__(self, remember_me=False, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint)
        self.ui = Ui_AuthForm()
        self.ui.setupUi(self)
        self.ui.login_btn.clicked.connect(self.handle_login_btn_clicked)
        self.ui.register_btn.clicked.connect(self.handle_register_button_clicked)
        self.ui.cancel_btn.clicked.connect(self.reject)
        self.ui.show_password_chb.clicked.connect(self.handle_show_password_chb_clicked)
        self.ui.remember_me_chb.clicked.connect(self.handle_remember_me_chb_clicked)
        self.ui.forgot_password_btn.clicked.connect(partial(show_not_implemented_msg, self))

        self.result = SimpleNamespace(session_key=None, username=None, remember_me=remember_me)

        self.ui.remember_me_chb.setChecked(self.result.remember_me)

    def handle_login_btn_clicked(self):
        uname_or_email = self.ui.username_ln_edt.text()
        password = self.ui.password_ln_edt.text()
        # TODO: some input validation
        try:
            self.ui.login_btn.setDisabled(True)
            session_key = db.log_in(uname_or_email, password)
            self.result.username, _ = db.get_user_info(session_key)
        except db.DatabaseConnectionError as exc:
            show_db_conn_err_msg(details=str(exc), parent=self)
            self.close()
        else:
            if session_key:
                self.result.session_key = session_key
                self.accept()
            else:
                self.ui.password_ln_edt.setFocus()
                QMessageBox.warning(self, "Телефонная книжка",
                                    "Не удалось войти. Такая комбинация учетных данных не найдена.")
        finally:
            self.ui.login_btn.setEnabled(True)

    def on_register_form_finished(self, form: RegisterForm, r: QDialog.DialogCode):
        if r == QDialog.Accepted:
            try:
                session_key = db.log_in(form.result.username, form.result.password)
                self.result.username = form.result.username
            except db.DatabaseConnectionError as exc:
                show_db_conn_err_msg(details=str(exc), parent=self)
                self.close()
            else:
                if session_key:
                    self.result.session_key = session_key
                    self.accept()
                else:
                    self.close()
                    QMessageBox.warning(self.parent(), "Телефонная книжка", "Автоматический вход не удался.")
        else:
            # TODO: process a case when register form closed due to db connection error
            self.show()

    def handle_register_button_clicked(self):
        form = RegisterForm(parent=self.parent())
        self.hide()
        form.finished.connect(partial(self.on_register_form_finished, form))
        form.open()

    def handle_show_password_chb_clicked(self, chb_active):
        if chb_active:
            self.ui.password_ln_edt.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.password_ln_edt.setFocus()
        else:
            self.ui.password_ln_edt.setEchoMode(QLineEdit.EchoMode.Password)

    def handle_remember_me_chb_clicked(self, chb_active):
        self.result.remember_me = chb_active
