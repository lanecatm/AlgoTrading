# -*- encoding:UTF-8 -*-
import sys
#from enum import Enum
#class ErrorCode(Enum):
#    SUCC = "succ"
#    PARAM_ERROR = "param error"
#
def enum(**enums):
    return type('Enum', (), enums)

Status= enum(
    SUCC="succ",
    PARAM_ERROR="param error",
    READ_FILE_ERROR = "read file error"
)
