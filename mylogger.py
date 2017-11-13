import logging
from logging.handlers import RotatingFileHandler
"""CRITICAL>ERROR>WARNING>INFO>DEBUG>NOTSET"""
def create_logging(filename):
    Rthandler = RotatingFileHandler(filename, maxBytes=204800, backupCount=5)
    Rthandler.setLevel(logging.INFO)  #write files info
    formatter = logging.Formatter('%(asctime)s [Line=%(lineno)s] %(levelname)s %(message)s')
    Rthandler.setFormatter(formatter)
    logging.basicConfig(level=logging.NOTSET)       #write to stdio all
    logger = logging.getLogger(filename)
    logger.addHandler(Rthandler)
    return logger