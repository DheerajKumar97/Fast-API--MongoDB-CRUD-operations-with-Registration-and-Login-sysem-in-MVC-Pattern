from flask import Flask
import re
import os



app = Flask(__name__)


class ErrorTable:
    Data = {'validator.InvalidToken': 'ER_AUT009',
            'validator.InvalidAuthentication': 'ER_AUT010',
            }


def verify_ErrorReason(ErrorReason):
    for Reason, ErrorCode in ErrorTable.Data.items():
        if Reason == ErrorReason:
            return ErrorCode


def get_ErrorCode(ErrorReason):
    if ErrorReason in ErrorTable.Data:
        return ErrorTable.Data[ErrorReason]
    else:
        None

def get_ErrorClass(sys_exec):
    error_class = str(sys_exec[0])
    error_class = error_class[8:-2]
    return error_class




class InvalidToken(Exception):
    pass


class InvalidAuthentication(Exception):
    pass


