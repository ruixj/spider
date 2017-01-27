import logging
import logging.config


class LelianLogger:
    bConfig = False
    @staticmethod
    def configLog(logConf):
        if (not LelianLogger.bConfig):
            LelianLogger.bConfig = True
            logging.config.fileConfig(logConf)
       
 
    @staticmethod        
    def debug(modulename,msg,*args,**kwargs):
        logger = logging.getLogger(modulename)
        logger.debug(msg,*args,**kwargs)
     
    @staticmethod    
    def info(modulename,msg,*args,**kwargs):
        logger = logging.getLogger(modulename)
        logger.info(msg,*args,**kwargs)
    
    @staticmethod     
    def warning(modulename,msg,*args,**kwargs):
        logger = logging.getLogger(modulename)
        logger.warning(msg,*args,**kwargs)                

    @staticmethod 
    def error(modulename,msg,*args,**kwargs):
        logger = logging.getLogger(modulename)
        logger.warning(msg,*args,**kwargs)    
        
    @staticmethod 
    def critical(modulename,msg,*args,**kwargs):
        logger = logging.getLogger(modulename)
        logger.warning(msg,*args,**kwargs)  
          
    @staticmethod 
    def log(modulename,lvl,msg,*args,**kwargs):
        logger = logging.getLogger(modulename)
        logger.log(msg,*args,**kwargs)    
  
    @staticmethod 
    def exception(modulename,msg,*args,**kwargs):
        logger = logging.getLogger(modulename)
        logger.exception(msg,*args,**kwargs)
                    
if __name__ == '__main__':
    pass
    
