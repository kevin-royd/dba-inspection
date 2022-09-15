import logging


# 配置log
def logger_config(log_path, log_name):
    # 获取对象
    logger = logging.getLogger(log_name)
    # 输出DEBUG信息，针对第一层多虑
    logger.setLevel(level=logging.DEBUG)
    # 获取文件句柄并设置日志级别，进行第二层多虑
    handler = logging.FileHandler(log_path, encoding='UTF-8')
    handler.setLevel(level=logging.INFO)
    # 生产日志文件格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(level)s - %(message)s')
    handler.setFormatter(formatter)
    # console控制太输出，handler相当于文件输出
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)
    # 为logging对象添加句柄
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


