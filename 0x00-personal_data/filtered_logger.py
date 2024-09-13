#!/usr/bin/env python3
"""
Module 0x00-personal_data
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, 
                 separator: str) -> str:
    """
    Obfuscates specific fields in a log message.
    """
    pattern = '|'.join([f'{field}=[^{separator}]*' for field in fields])
    return re.sub(pattern, lambda m: m.group(0).split('=')[0] 
                  + '=' + redaction, message)
