import logging
from typing import Optional, Union

from PyQt5.QtSql import QSqlDatabase, QSqlError, QSqlQuery
from PyQt5.QtWidgets import QMessageBox

from . import logger


class DatabaseError(Exception):
    @staticmethod
    def from_error(error: QSqlError):
        err_type_to_exc_cls = {
            QSqlError.NoError: None,
            QSqlError.ConnectionError: DatabaseConnectionError,
            QSqlError.StatementError: DatabaseStatementError,
            QSqlError.TransactionError: DatabaseTransactionError,
            QSqlError.UnknownError: DatabaseUnknownError
        }
        try:
            exc_cls = err_type_to_exc_cls[error.type()]
        except KeyError:
            raise RuntimeError("unknown value {} of {}".format(error.type(), QSqlError.ErrorType))
        return None if exc_cls is None else exc_cls(
            "[{}] {}; {}".format(error.nativeErrorCode(), error.databaseText(), error.driverText()), error)

    def __str__(self):
        return str(self.args[0]) if self.args else super().__str__()


class DatabaseConnectionError(DatabaseError):
    pass


class DatabaseStatementError(DatabaseError):
    pass


class DatabaseTransactionError(DatabaseError):
    pass


class DatabaseUnknownError(DatabaseError):
    pass


def process_error(value: Union[QSqlError, QSqlQuery, QSqlDatabase],
                  raise_exc=True, log=True, show_msg_if_not_conn_err=False) -> Optional[DatabaseError]:
    error = value.lastError() if isinstance(value, (QSqlQuery, QSqlDatabase)) else value
    if error.type() == QSqlError.NoError:
        raise ValueError("there was no error")
    exc = DatabaseError.from_error(error)
    if show_msg_if_not_conn_err and not isinstance(exc, DatabaseConnectionError):
        msg_box = QMessageBox(QMessageBox.Critical, "Телефонная книжка",
                              "Неожиданная ошибка при работе с базой данных.")
        msg_box.setDetailedText(str(exc))
        msg_box.exec()
    if log:
        if isinstance(exc, DatabaseConnectionError):
            logger.warning("Can't connect to database: %s", str(exc))
        else:
            logger.error("Got an unexpected database-related error: %s", str(exc))
    if raise_exc:
        raise exc
    return exc
