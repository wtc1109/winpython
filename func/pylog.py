import logging
from logging.handlers import RotatingFileHandler

#logging.basicConfig(format='%s(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s', datefmt='%a, %d %b %Y %H:%M:%S')
Rthandler = RotatingFileHandler("pylog.log", maxBytes=2048, backupCount=5)
Rthandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [Line=%(lineno)s] %(levelname)s %(message)s')
Rthandler.setFormatter(formatter)
mylog = logging.getLogger('').addHandler(Rthandler)
#logging.debug("debug")

logging.info("info")
logging.warning("warning")
logging.error("esafbhiu")
