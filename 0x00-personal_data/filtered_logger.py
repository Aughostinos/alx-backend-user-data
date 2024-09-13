#!/usr/bin/env python3
"""
Module 0x00-personal_data
"""
import re
import logging
from typing import List
import os
import mysql.connector
from mysql.connector import connection


def get_db() -> connection.MySQLConnection:
    """
    Connect to a secure MySQL database
    """
    # Retrieve environment variables with defaults
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    # Connect to the MySQL database
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates specific fields in a log message.
    """
    pattern = '|'.join([f'{field}=[^{separator}]*' for field in fields])
    return re.sub(pattern, lambda m: m.group(0).split('=')[0]
                  + '=' + redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Creates a logger with PII filtering.

    Returns:
        logging.Logger: Configured logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a StreamHandler
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    # Adding handler to the logger
    logger.addHandler(stream_handler)

    return logger


def main() -> None:
    """
    Main function to retrieve data from the database
    """
    # database connection
    db = get_db()
    cursor = db.cursor()

    # retrieve all rows from the 'users' table
    cursor.execute(("SELECT name, email, phone, ssn, password, ip, last_login, user_agent FROM users;"))
    rows = cursor.fetchall()

    # the logger
    logger = get_logger()

    # Log each row in the required format
    for row in rows:
        name, email, phone, ssn, password, ip, last_login, user_agent = row
        message = (f"name={name}; email={email}; phone={phone}; ssn={ssn}; "
                   f"password={password}; ip={ip}; last_login={last_login}; "
                   f"user_agent={user_agent};")
        # Log the messag
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
