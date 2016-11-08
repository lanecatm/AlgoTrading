#-*- encoding:utf-8 -*-

import sys, os, time
import ErrorCode
from FileHelper import FileHelper

class Log:
    def __init__(self, isOpen = False, saveInfo = True, saveWarning = True, saveError = True, logDirName = "log"):
        self.saveInfo = saveInfo
        self.saveError = saveError
        self.saveWarning = saveWarning
        # 获取当前"运行"目录
        logDir = os.getcwd() + "/" + logDirName + "/"
        if not os.path.exists(logDir):
            os.mkdir(logDir)
        timeFormat= "%Y_%m_%d_%H_%M_%S"
        timeStr = time.strftime(timeFormat, time.localtime())
        fileNameStr = self.__get_parent_filename()
        fileNameStr = os.path.basename(fileNameStr)
        fileNameStr, ext = os.path.splitext(fileNameStr)
        self.infoFilename = logDir + "INFO_" + fileNameStr + "_" +timeStr + ".log"
        self.infoNowName = logDir + "INFO_" + fileNameStr + ".log"
        self.errorFilename = logDir + "ERROR_" + fileNameStr + "_" + timeStr + ".log"
        self.errorNowName = logDir + "ERROR_" + fileNameStr + ".log"
        self.warningFilename = logDir + "WARNING_" + fileNameStr + "_" + timeStr + ".log"
        self.warningNowName = logDir + "WARNING_" + fileNameStr + ".log"
        self.fileHelper = FileHelper()
        self.isOpen = isOpen
        return

    def __del__(self):
        try:
            os.remove(self.infoNowName)
            os.remove(self.errorNowName)
            os.remove(self.warningNowName)
        except:
            self.info("no old log file to remove")

        os.symlink(self.infoFilename, self.infoNowName)
        os.symlink(self.errorFilename, self.errorNowName)
        os.symlink(self.warningFilename, self.warningNowName)
        return

    # @param maeeage string
    # @return None
    def info(self, message=""):
        if not self.isOpen:
            return
        outputInfo = "[INFO] " + self.__get_parent_filename() + " " + self.__get_parent_lineno() + ": " + message
        print outputInfo
        self.fileHelper.append(self.infoFilename, outputInfo + "\n", isAbs = True)
        return

    # @param message string
    # @return None
    def warning(self, message=""):
        if not self.isOpen:
            return
        outputInfo = "[WARNING] " + self.__get_parent_filename() + " " + self.__get_parent_lineno() + ": " + message
        print outputInfo
        self.fileHelper.append(self.warningFilename, outputInfo + "\n", isAbs = True)
        return

    # @param message string
    # @return None
    def error(self, message=""):
        if not self.isOpen:
            return
        outputInfo = "[ERROR] " + self.__get_parent_filename() + " " + self.__get_parent_lineno() + ": " + message
        print outputInfo
        self.fileHelper.append(self.errorFilename, outputInfo + "\n", isAbs = True)
        return

    # @param errorStatus ErrorCode
    def check_rtn(self, errorStatus, message=""):
        if errorStatus != ErrorCode.Status.SUCC:
            print "[ERROR RTN] " + self.__get_parent_filename() + " " + self.__get_parent_lineno() + ": error " + errorStatus + " " + message

    def assert_eq(self, input1, input2):
        if input1!=input2:
            print "[ASSERT EQ] " + self.__get_parent_filename() + " " + self.__get_parent_lineno() + ": [expect] " + str(input1) + ", [actual] " + str(input2)



    #def __get_parent_class_name(self):
    #    return sys._getframe().f_back.f_code

    def __get_parent_function_name(self):
        return sys._getframe().f_back.f_back.f_code.co_name

    def __get_parent_filename(self):
        filename = sys._getframe().f_back.f_back.f_code.co_filename
        return os.path.expanduser(filename)

    def __get_parent_lineno(self):
        return str(sys._getframe().f_back.f_back.f_lineno)
