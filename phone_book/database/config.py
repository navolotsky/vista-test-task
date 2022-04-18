from typing import NamedTuple

from PyQt5.QtSql import QSqlDatabase

from .errors import process_error


def setup_db(settings, default_settings):
    try:
        settings.beginGroup("database")
        if default_settings is not settings:
            default_settings.beginGroup("database")
        qsql_driver = settings.value("qsql_driver")
        if qsql_driver is None:
            qsql_driver = default_settings.value("qsql_driver")
        db = QSqlDatabase.addDatabase(qsql_driver, connectionName="main_database")
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
        if default_settings is not settings:
            default_settings.endGroup()


def get_opened_db():
    if not QSqlDatabase.contains(connectionName="main_database"):
        raise RuntimeError("You must call `setup_db()` at first")
    db = QSqlDatabase.database(connectionName="main_database", open=True)
    if db.isOpenError():
        process_error(db)
    return db


class CheckDBConnectionSettingsResult(NamedTuple):
    is_error: bool = False
    is_critical: bool = False
    message: str = ""


def check_db_connection_settings(host_name, port, database_name, username, password,
                                 qsql_driver) -> CheckDBConnectionSettingsResult:
    conn_name = "new_connection_settings_test_db"
    db = QSqlDatabase.addDatabase(qsql_driver, connectionName=conn_name)
    try:
        if not db.isValid():
            return CheckDBConnectionSettingsResult(is_error=True, is_critical=True,
                                                   message="database driver improperly configured")
        for val, method in zip((host_name, port, database_name, username, password),
                               (db.setHostName, db.setPort, db.setDatabaseName, db.setUserName, db.setPassword)):
            method(val)
        db.open()
        if db.isOpenError():
            return CheckDBConnectionSettingsResult(is_error=True, message=str(process_error(db, raise_exc=False)))
    finally:
        QSqlDatabase.removeDatabase(conn_name)
    return CheckDBConnectionSettingsResult()
