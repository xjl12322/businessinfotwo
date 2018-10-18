#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"
import logging, os





class Logger(object):
    path = "C:\\Users\\Administrator\\Desktop\\项目代码\\businessinfotwo\\businessinfotwo\\utils_common\\log.txt"
    clevel = logging.DEBUG
    Flevel = logging.DEBUG
    logger = logging.getLogger(path)
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter('[%(asctime)s]-%(filename)s-%(levelname)s : %(message)s',
                            '%Y-%m-%d %H:%M:%S')
    # 设置CMD日志
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    sh.setLevel(clevel)
    # 设置文件日志
    fh = logging.FileHandler(path, encoding="utf-8")
    fh.setFormatter(fmt)
    fh.setLevel(Flevel)
    logger.addHandler(sh)
    logger.addHandler(fh)



    @staticmethod
    def debug(message):
        Logger.logger.debug(message)

    @staticmethod
    def info(message):
        Logger.logger.info(message)

    @staticmethod
    def war(message):

        Logger.logger.warn(message)

    @staticmethod
    def error(message):
        Logger.logger.error(message)

    @staticmethod
    def cri( message):
        Logger.logger.critical(message)


if __name__ == '__main__':

    Logger.debug('一个debug信息')
    Logger.info('一个info信息')
    Logger.war('一个warning信息')
    Logger.error('一个error信息')
    Logger.cri('一个致命critical信息')






#################################################################################################
#定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M

################################################################################################













