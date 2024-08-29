#!/usr/bin/env python3
"""Log filter module"""
from typing import List
import logging
import mysql.connector
import os
import re


reg = {
    'extract': lambda i, j: r'(?P<field>{})=[^{}]*'.format('|'.join(i), j),
    'replace': lambda i: r'\g<field>={}'.format(i),
}
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_danum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str,
) -> str:
    """Filters a log"""
    extract, replace = (reg["extract"], reg["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """Creates a new logger"""
    logger = logging.getLogger("user_data")
    stream_handler = logging.streamHandler()
    stream_handler.setFormatter(redactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a connector to a MySQL database"""
    db_host = os.get_env("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.get_env("PERSONAL_DATA_DB_NAME", "")
    db_user = os.get_env("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.get_env("PERSONAL_DATA_DB_PASSWORD", "")

    conn = mysql.connector.connect(
        host=db_host,
        port=3306,
        database=db_name,
        user=db_user,
        password=db_pwd,
    )
    return conn


def main():
    """Logs info about the user to a table"""
    fields = "name, email, phone, ssn, password, ip, last_login, user_agent"
    columns = fields.split(", ")
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    conn = get_db()

    with conn.cursor() as cursor:
        corsor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            message = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, message, None, None)
            record_log = logging.LogRecord(*args)
            info_logger.handle(record_log)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record"""
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_danum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt


if __name__ == "__main__":
    main()
