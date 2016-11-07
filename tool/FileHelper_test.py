# -*- encoding:UTF-8 -*-
import sys, os
import ErrorCode
from Log import Log
from FileHelper import FileHelper

if __name__ == "__main__":
    log = Log()
    log.info("start test FileHelper")

    testContent = "hello abc"
    fileHelper = FileHelper()
    rtn = fileHelper.write("hello.txt", testContent)
    log.check_rtn(rtn)
    rtn, content = fileHelper.read("hello.txt")
    log.check_rtn(rtn)
    log.assert_eq(testContent, content)
    testContentNew = "def"
    rtn = fileHelper.append("hello.txt", testContentNew)
    log.check_rtn(rtn)
    rtn, content = fileHelper.read("hello.txt")
    log.check_rtn(rtn)
    log.assert_eq(testContent + testContentNew, content)

    rtn = fileHelper.append("hello2.txt", testContentNew)
    log.check_rtn(rtn)
    rtn, content = fileHelper.read("hello2.txt")
    log.check_rtn(rtn)
    log.assert_eq(testContentNew, content)

    os.remove("hello.txt")
    os.remove("hello2.txt")
    sys.exit()
