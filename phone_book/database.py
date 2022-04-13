import enum
import logging

from PyQt5 import QtSql
from PyQt5.QtCore import Qt

logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    pass


class DatabaseConnectionError(DatabaseError):
    pass


def process_query_error(query):
    exc_cls = DatabaseError
    if query.lastError().type() == QtSql.QSqlError.ConnectionError:
        exc_cls = DatabaseConnectionError
    raise exc_cls(query.lastError().text(), query.lastError())


def setup_db(settings, default_settings):
    try:
        settings.beginGroup("database")
        if settings is not default_settings:
            default_settings.beginGroup("database")
        qsql_driver = settings.value("qsql_driver")
        if qsql_driver is None:
            qsql_driver = default_settings.value("qsql_driver")
        db = QtSql.QSqlDatabase.addDatabase(qsql_driver, connectionName="main_database")
        if not db.isValid():
            raise RuntimeError("database driver improperly configured")
        for key, method in zip(("host_name", "port", "database_name", "username", "password"),
                               (db.setHostName, db.setPort, db.setDatabaseName, db.setUserName, db.setPassword)):
            val = settings.value(key)
            if val is None:
                val = default_settings.value(key)
            if key == "port":
                val = int(val)
            method(val)
    finally:
        settings.endGroup()
        default_settings.endGroup()


def get_opened_db():
    if not QtSql.QSqlDatabase.contains(connectionName="main_database"):
        raise RuntimeError("You must call `setup_db` at first")
    db = QtSql.QSqlDatabase.database(connectionName="main_database", open=True)
    if db.isOpenError():
        logger.error("Cannot open database: %s; Error type: %s", db.lastError().text(), db.lastError().type())
        if db.lastError().type() == QtSql.QSqlError.ConnectionError:
            raise DatabaseConnectionError(db.lastError().text(), db.lastError())
        raise DatabaseError(db.lastError().text(), db.lastError())
    return db


def check_session_exists(session_key):
    db = get_opened_db()
    try:
        query = QtSql.QSqlQuery(db)
        query.prepare("CALL check_session(:session_key, @session_exists)")
        query.bindValue(":session_key", session_key)
        if not query.exec():
            process_query_error(query)
        if not query.exec("SELECT @session_exists"):
            process_query_error(query)
        if not query.next():
            process_query_error(query)
        else:
            return bool(query.value(0))
    finally:
        db.close()


class RegisterResult(enum.Enum):
    SUCCESS = "registered_successfully"
    UNKNOWN_ERROR = "unknown_error"
    USERNAME_EXISTS = "username_already_exists"
    EMAIL_EXISTS = "email_already_exists"


def register(username, email, birth_date):
    db = get_opened_db()
    try:
        query = QtSql.QSqlQuery(db)
        query.prepare("CALL register(:username, :email, :birth_date, @result_msg, @password)")
        query.bindValue(":username", username)
        query.bindValue(":email", email)
        query.bindValue(":birth_date", birth_date)
        if not query.exec():
            process_query_error(query)
        if not query.exec("SELECT @result_msg, @password"):
            process_query_error(query)
        if not query.next():
            process_query_error(query)
        else:
            return RegisterResult(query.value(0)), query.value(1)
    finally:
        db.close()


def log_in(username_or_email, password):
    db = get_opened_db()
    try:
        query = QtSql.QSqlQuery(db)
        query.prepare("CALL log_in(:username_or_email, :password, @session_key)")
        query.bindValue(":username_or_email", username_or_email)
        query.bindValue(":password", password)
        if not query.exec():
            process_query_error(query)
        if not query.exec("SELECT @session_key"):
            process_query_error(query)
        if not query.next():
            process_query_error(query)
        else:
            return query.value(0)
    finally:
        db.close()


def log_out(session_key):
    db = get_opened_db()
    try:
        query = QtSql.QSqlQuery(db)
        query.prepare("CALL log_out(:session_key)")
        query.bindValue(":session_key", session_key)
        if not query.exec():
            process_query_error(query)
    finally:
        db.close()


def get_user_info(session_key):
    db = get_opened_db()
    try:
        query = QtSql.QSqlQuery(db)
        query.prepare("CALL get_user_info(:session_key, @username, @email)")
        query.bindValue(":session_key", session_key)
        if not query.exec():
            process_query_error(query)
        if not query.exec("SELECT @username, @email"):
            process_query_error(query)
        if not query.next():
            process_query_error(query)
        else:
            return query.value(0), query.value(1)
    finally:
        db.close()


def get_all_contacts(session_key):
    db = get_opened_db()
    try:
        query = QtSql.QSqlQuery(db)
        query.prepare("CALL get_all_contacts(:session_key)")
        query.bindValue(":session_key", session_key)
        if not query.exec():
            process_query_error(query)
        if not query.next():
            process_query_error(query)
    finally:
        db.close()


def get_contacts(session_key, letter_set, exclude):
    db = get_opened_db()
    try:
        query = QtSql.QSqlQuery(db)
        query.prepare("CALL get_contacts(:session_key, :letter_set, :exclude)")
        query.bindValue(":session_key", session_key)
        query.bindValue(":letter_set", letter_set)
        query.bindValue(":exclude", exclude)
        if not query.exec():
            process_query_error(query)
        if not query.next():
            process_query_error(query)
    finally:
        db.close()


class AddContactResult(enum.Enum):
    SUCCESS = "added_successfully"
    UNKNOWN_ERROR = "unknown_error"
    INVALID_SESSION = "invalid_session_key"
    CONTACT_EXISTS = "contact_already_exists"


def add_contact(session_key, name, phone_number, birth_date):
    db = get_opened_db()
    try:
        query = QtSql.QSqlQuery(db)
        query.prepare("CALL add_contact(:session_key, :name, :phone_number, :birth_date, @result_msg, @contact_id)")
        query.bindValue(":session_key", session_key)
        query.bindValue(":name", name)
        query.bindValue(":phone_number", phone_number)
        query.bindValue(":birth_date", birth_date)
        if not query.exec():
            process_query_error(query)
        if not query.exec("SELECT @result_msg, @contact_id"):
            process_query_error(query)
        if not query.next():
            process_query_error(query)
        else:
            result_type = AddContactResult(query.value(0))
            contact_id = query.value(1)
            if contact_id is not None:
                contact_id = int(contact_id)
            return result_type, contact_id
    finally:
        db.close()


class ContactsReadWriteModel(QtSql.QSqlQueryModel):
    def __init__(self, parent, letter_set, exclude=False):
        super().__init__(parent)
        self.letter_set = letter_set
        self.exclude = exclude

    def refresh(self, session_key):
        query = QtSql.QSqlQuery(get_opened_db())
        # Have to manually format a string for exec()
        # because using prepare(), bindValue() or addBindValue(), exec()
        # with CALL that should return a SELECT result set doesn't work properly:
        # query.isSelect() returns False and query.size() returns -1
        if not query.exec("CALL get_contacts('{}', '{}', {})".format(session_key, self.letter_set, self.exclude)):
            process_query_error(query)
        self.setQuery(query)
        for idx, value in enumerate(["Имя", "Телефон", "Дата рождения"], 1):
            self.setHeaderData(idx, Qt.Horizontal, value)
