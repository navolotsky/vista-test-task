from enum import Enum
from typing import NamedTuple, Optional, Tuple, Union

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel

from .config import get_opened_db
from .errors import process_error


def check_session_exists(session_key):
    db = get_opened_db()
    try:
        query = QSqlQuery(db)
        query.prepare("CALL check_session(:session_key, @session_exists)")
        query.bindValue(":session_key", session_key)
        if not query.exec():
            process_error(query)
        if not query.exec("SELECT @session_exists"):
            process_error(query)
        if not query.next():
            process_error(query)
        else:
            return bool(query.value(0))
    finally:
        db.close()


class RegisterResult(Enum):
    SUCCESS = "registered_successfully"
    UNKNOWN_ERROR = "unknown_error"
    USERNAME_EXISTS = "username_already_exists"
    EMAIL_EXISTS = "email_already_exists"


def register(username, email, birth_date):
    db = get_opened_db()
    try:
        query = QSqlQuery(db)
        query.prepare("CALL register(:username, :email, :birth_date, @result_msg, @password)")
        query.bindValue(":username", username)
        query.bindValue(":email", email)
        query.bindValue(":birth_date", birth_date)
        if not query.exec():
            process_error(query)
        if not query.exec("SELECT @result_msg, @password"):
            process_error(query)
        if not query.next():
            process_error(query)
        else:
            return RegisterResult(query.value(0)), query.value(1)
    finally:
        db.close()


def log_in(username_or_email, password):
    db = get_opened_db()
    try:
        query = QSqlQuery(db)
        query.prepare("CALL log_in(:username_or_email, :password, @session_key)")
        query.bindValue(":username_or_email", username_or_email)
        query.bindValue(":password", password)
        if not query.exec():
            process_error(query)
        if not query.exec("SELECT @session_key"):
            process_error(query)
        if not query.next():
            process_error(query)
        else:
            return query.value(0)
    finally:
        db.close()


def log_out(session_key):
    db = get_opened_db()
    try:
        query = QSqlQuery(db)
        query.prepare("CALL log_out(:session_key)")
        query.bindValue(":session_key", session_key)
        if not query.exec():
            process_error(query)
    finally:
        db.close()


def get_user_info(session_key):
    db = get_opened_db()
    try:
        query = QSqlQuery(db)
        query.prepare("CALL get_user_info(:session_key, @username, @email)")
        query.bindValue(":session_key", session_key)
        if not query.exec():
            process_error(query)
        if not query.exec("SELECT @username, @email"):
            process_error(query)
        if not query.next():
            process_error(query)
        else:
            return query.value(0), query.value(1)
    finally:
        db.close()


def get_all_contacts(session_key):
    db = get_opened_db()
    try:
        query = QSqlQuery(db)
        query.prepare("CALL get_all_contacts(:session_key)")
        query.bindValue(":session_key", session_key)
        if not query.exec():
            process_error(query)
        if not query.next():
            process_error(query)
    finally:
        db.close()


def get_contacts(session_key, letter_set, exclude):
    db = get_opened_db()
    try:
        query = QSqlQuery(db)
        query.prepare("CALL get_contacts(:session_key, :letter_set, :exclude)")
        query.bindValue(":session_key", session_key)
        query.bindValue(":letter_set", letter_set)
        query.bindValue(":exclude", exclude)
        if not query.exec():
            process_error(query)
        if not query.next():
            process_error(query)
    finally:
        db.close()


class AddContactResult(Enum):
    SUCCESS = "added_successfully"
    UNKNOWN_ERROR = "unknown_error"
    INVALID_SESSION = "invalid_session_key"
    CONTACT_EXISTS = "contact_already_exists"


def _add_contact(session_key, name, phone_number, birth_date) -> Tuple[AddContactResult, Optional[int]]:
    db = get_opened_db()
    try:
        query = QSqlQuery(db)
        query.prepare("CALL add_contact(:session_key, :name, :phone_number, :birth_date, @result_msg, @contact_id)")
        query.bindValue(":session_key", session_key)
        query.bindValue(":name", name)
        query.bindValue(":phone_number", phone_number)
        query.bindValue(":birth_date", birth_date)
        if not query.exec():
            process_error(query)
        if not query.exec("SELECT @result_msg, @contact_id"):
            process_error(query)
        if not query.next():
            process_error(query)
        else:
            result_type = AddContactResult(query.value(0))
            contact_id = query.value(1)
            if contact_id is not None:
                contact_id = int(contact_id)
            return result_type, contact_id
    finally:
        db.close()


class EditContactResult(Enum):
    SUCCESS = "edited_successfully"
    UNKNOWN_ERROR = "unknown_error"
    INVALID_SESSION = "invalid_session_key"
    CONTACT_DOESNT_EXIST = "given_contact_doesnt_exist"
    NO_AUTHORITY_TO_EDIT_CONTACT = "no_authority_to_edit_given_contact"
    SAME_DATA_CONTACT_EXISTS = "same_data_contact_already_exists"


def _edit_contact(session_key, contact_id, name, phone_number, birth_date) -> Tuple[EditContactResult, Optional[int]]:
    db = get_opened_db()
    try:
        query = QSqlQuery(db)
        query.prepare(
            "CALL edit_contact(:session_key, :contact_id, :name, :phone_number, :birth_date, "
            "@result_msg, @same_data_contact_id)")
        query.bindValue(":session_key", session_key)
        query.bindValue(":contact_id", contact_id)
        query.bindValue(":name", name)
        query.bindValue(":phone_number", phone_number)
        query.bindValue(":birth_date", birth_date)
        if not query.exec():
            process_error(query)
        if not query.exec("SELECT @result_msg, @same_data_contact_id"):
            process_error(query)
        if not query.next():
            process_error(query)
        else:
            result_type = EditContactResult(query.value(0))
            same_data_contact_id = query.value(1)
            if same_data_contact_id is not None:
                same_data_contact_id = int(same_data_contact_id)
            return result_type, same_data_contact_id
    finally:
        db.close()


class DeleteContactResult(Enum):
    SUCCESS = "deleted_successfully"
    UNKNOWN_ERROR = "unknown_error"
    INVALID_SESSION = "invalid_session_key"
    CONTACT_DOESNT_EXIST = "given_contact_doesnt_exist"
    NO_AUTHORITY_TO_DELETE_CONTACT = "no_authority_to_delete_given_contact"


def _delete_contact(session_key, contact_id) -> DeleteContactResult:
    db = get_opened_db()
    try:
        query = QSqlQuery(db)
        query.prepare("CALL delete_contact(:session_key, :contact_id, @result_msg)")
        query.bindValue(":session_key", session_key)
        query.bindValue(":contact_id", contact_id)
        if not query.exec():
            process_error(query)
        if not query.exec("SELECT @result_msg"):
            process_error(query)
        if not query.next():
            process_error(query)
        else:
            return DeleteContactResult(query.value(0))
    finally:
        db.close()


class ContactData(NamedTuple):
    name: str
    phone_number: str
    birth_date: QDate


class ContactsPageReadWriteModel(QSqlQueryModel):
    class Columns(Enum):
        primary_key = 0
        name = 1
        phone_number = 2
        birth_date = 3

    def __init__(self, letter_set, exclude=False, parent=None):
        super().__init__(parent)
        self.letter_set = letter_set
        self.exclude = exclude

    def refresh(self, session_key):
        query = QSqlQuery(get_opened_db())
        # Have to manually format a string for exec()
        # because using prepare(), bindValue() or addBindValue(), exec()
        # with CALL that should return a SELECT result set doesn't work properly:
        # query.isSelect() returns False and query.size() returns -1
        if not query.exec("CALL get_contacts('{}', '{}', {})".format(session_key, self.letter_set, self.exclude)):
            process_error(query)
        self.setQuery(query)
        for idx, value in enumerate(["Имя", "Телефон", "Дата рождения"], 1):
            self.setHeaderData(idx, Qt.Horizontal, value)

    def get_contact_data(self, row_idx: int) -> ContactData:
        return ContactData(self.data(self.index(row_idx, self.Columns.name.value), role=Qt.EditRole),
                           self.data(self.index(row_idx, self.Columns.phone_number.value), role=Qt.EditRole),
                           self.data(self.index(row_idx, self.Columns.birth_date.value), role=Qt.EditRole))

    def add_contact(self, session_key, name, phone_number, birth_date):
        return _add_contact(session_key, name, phone_number, birth_date)

    def edit_contact(self, session_key, row_idx, name, phone_number, birth_date):
        contact_id = self.data(self.index(row_idx, self.Columns.primary_key.value), role=Qt.EditRole)
        return _edit_contact(session_key, contact_id, name, phone_number, birth_date)

    def delete_contact(self, session_key, row_idx):
        contact_id = self.data(self.index(row_idx, self.Columns.primary_key.value), role=Qt.EditRole)
        return _delete_contact(session_key, contact_id)


class UpcomingBirthdaysReadModel(QSqlQueryModel):
    class RangeType(Enum):
        DAY = "day"

    def __init__(self, range_type: Union[RangeType, str], range_value: int, parent):
        super().__init__(parent)

        self.range_type = self.RangeType(range_type)
        self.range_value = range_value

        if self.range_type is self.RangeType.DAY:
            self.seconds = self.range_value * 24 * 3600
        else:
            raise RuntimeError("unknown member: {}".format(self.range_type))

    def refresh(self, session_key):
        query = QSqlQuery(get_opened_db())
        if not query.exec("CALL get_contacts_having_birthday_in_range('{}', {})".format(session_key, self.seconds)):
            process_error(query)
        self.setQuery(query)
        for idx, value in enumerate(["Имя", "Телефон", "Дата рождения"], 1):
            self.setHeaderData(idx, Qt.Horizontal, value)
