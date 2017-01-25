import logging
import logging.config

logging.config.fileConfig('logger.conf')
logger = logging.getLogger('filerotate')
logger.debug(" this is a debug message")
class pyLogger:
    def __init__(self):
        pass
    def debug(self,message)
        logging.debug(message)


if __name__ == '__main__':
    pass
    
