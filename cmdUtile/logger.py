import logging
import os

import yaml


class Logger:
    def __init__(self, name=__name__):
        # 创建一个loggger
        self.__name = name
        self.logger = logging.getLogger(self.__name)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        # 执行文件为main.py 所有目录层级为main.py开始
        with open('./conf/config.yml', 'r') as f:
            yml_json = yaml.load(f.read(), Loader=yaml.Loader)
            logfile = yml_json['logger']['logfile']
            logpath = yml_json['logger']['logpath']
            f.close()
        logname = logpath + logfile
        fh = logging.FileHandler(logname, mode='a', encoding='utf-8')  # 不拆分日志文件，a指追加模式,w为覆盖模式
        fh.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)

    @property
    def get_log(self):
        """定义一个函数，回调logger实例"""
        return self.logger
