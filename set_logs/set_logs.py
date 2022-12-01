import sys
import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

top_path = Path(__file__).parent
LOG_DIR = top_path / 'logs'
LOG_DIR.mkdir(exist_ok=True)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')


def setup_logger(name, log_file=f'{top_path.name}.log', level=logging.INFO):
    """
    日志记录器，根据日志级别将日志写入不同文件
    :param name:        string -- logger name 主模块为‘main',其余子模块为‘main.submodule'
    :param log_file:    string -- 日志文件名称
    :param level:       logging level -- 默认 logging.INFO
    :return:
            logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # error 级别日志的处理
    error_th = TimedRotatingFileHandler(filename=LOG_DIR / f'error_{log_file}',
                                        when='MIDNIGHT', backupCount=7, encoding='utf-8')
    error_th.setFormatter(formatter)
    error_th.setLevel(level)
    error_filter = logging.Filter()
    error_filter.filter = lambda record: record.levelno >= logging.ERROR
    error_th.addFilter(error_filter)
    logger.addHandler(error_th)
    # 小于error界别的日志
    info_th = TimedRotatingFileHandler(filename=LOG_DIR / f'info_{log_file}',
                                       when='MIDNIGHT', backupCount=7, encoding='utf-8')
    info_th.setFormatter(formatter)
    info_th.setLevel(level)
    info_filter = logging.Filter()
    info_filter.filter = lambda record: record.levelno < logging.ERROR
    info_th.addFilter(info_filter)
    logger.addHandler(info_th)
    # 显示输出的日志
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    sh.setLevel(level)
    logger.addHandler(sh)

    return logger

if __name__ == "__main__":
    logger = setup_logger(name='dev_test')
