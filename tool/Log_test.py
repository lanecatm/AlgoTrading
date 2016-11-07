# -*- encoding:UTF-8 -*-
import sys, os
import ErrorCode
from Log import Log
from FileHelper import FileHelper

if __name__ == "__main__":
    log = Log()
    testSetence = "test log"
    log.info(testSetence)
    log.info(testSetence)
    log.warning(testSetence)
    log.warning(testSetence)
    log.error(testSetence)
    log.error(testSetence)
    sys.exit()
