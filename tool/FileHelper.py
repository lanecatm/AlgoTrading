# -*- encoding:UTF-8 -*-
import sys,shutil, os
import ErrorCode
import FileUtility

class FileHelper:
    def __init__(self):
        return

    # 备份文件文件名
    def __get_tmp_filename(self, filename, suffix = ".backup"):
        return filename + suffix

    # 从文件中读取json
    # param filename string 文件路径
    # param isAbs boolean 是否需要绝对路径转换
    # return int succ code
    # return string content
    def read(self ,filename, isAbs=False):
        if not isAbs:
            filename = FileUtility.getAbsFilePath(filename)
        file = open(filename)
        content = ""
        try:
            content = file.read()
        except:
            file.close()
            return ErrorCode.Status.READ_FILE_ERROR, content
        file.close()
        return ErrorCode.Status.SUCC, content

    def write(self, filename, content ,isAbs = False):
        processingFilename = self.__get_tmp_filename(filename)
        if not isAbs:
            processingFilename = FileUtility.getAbsFilePath(processingFilename)
        file = open(processingFilename, 'w')
        try:
            file.write(content)
        except:
            file.close()
            return ErrorCode.Status.SAVE_FILE_ERROR
        file.close()
        shutil.move(processingFilename, filename)
        return ErrorCode.Status.SUCC

    def append(self, filename, content, isAbs = False):
        processingFilename = self.__get_tmp_filename(filename)
        if os.path.exists(filename):
            shutil.copy(filename, processingFilename)
        if not isAbs:
            processingFilename = FileUtility.getAbsFilePath(processingFilename)
        file = open(processingFilename, 'a')
        try:
            # 移动到文件尾
            file.seek(0, 2)
            file.write(content)
        except:
            file.close()
            return ErrorCode.Status.SAVE_FILE_ERROR
        file.close()
        shutil.move(processingFilename, filename)
        return ErrorCode.Status.SUCC


