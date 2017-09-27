import logging
from logging.handlers import RotatingFileHandler

def create_logging():
    Rthandler = RotatingFileHandler("pylog.log", maxBytes=2048, backupCount=5)
    Rthandler.setLevel(logging.INFO)  #write files info
    formatter = logging.Formatter('%s(asctime)s [Line=%(lineno)s] %(levelname)s %(message)s')
    Rthandler.setFormatter(formatter)
    logging.basicConfig(level=logging.NOTSET)       #write to stdio all
    mylogger = logging.getLogger("12")
    mylogger.addHandler(Rthandler)

    return mylogger


#logging.debug("debug")
if __name__ == '__main__':
    mylog = create_logging()
    mylog.debug("safhihi")
    mylog.error("sfui")
    """
    logging.info("info")
    logging.warning("warning")
    logging.error("esafbhiu")"""
