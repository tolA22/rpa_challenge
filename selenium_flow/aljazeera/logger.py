import logging 

logger = logging.getLogger(__name__) #create logger
formatter = logging.Formatter() #create formatter for prefix
formatter._fmt = 'ALJAZEERA_DRIVER'
handler = logging.StreamHandler() #create handler
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.info("Aljazeera Logger Ready!!!")

