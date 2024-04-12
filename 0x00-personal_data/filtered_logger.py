#!/usr/bin/env python3
"""
filtered_logger module
"""

import logging
import re
from typing import List, Tuple

PII_FIELDS: Tuple[str] = ("email", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Tuple[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log message with redaction.
        """
        return filter_datum(
            self.fields,
            self.REDACTION,
            super().format(record),
            self.SEPARATOR
        )


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """
    Filter sensitive data from log message.
    """
    return re.sub(r'(?:^|{})({})(?={}|$)'.format(
        '|'.join([separator, '^']), '|'.join(fields), separator),
        redaction,
        message
    )


def get_logger() -> logging.Logger:
    """
    Get logger with RedactingFormatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
