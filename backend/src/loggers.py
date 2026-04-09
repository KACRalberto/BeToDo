import logging
##
logging.getLogger().handlers.clear()
### 

class LevelFilter(logging.Filter):


    def __init__(self, level):
        self.level = level


    def filter(self, record):
        return record.levelname == self.level.upper()


class my_logger:

    #CONSTRUCTOR DE LOGGERS

    def __init__(self, name, level="DEBUG", consola=False, file_l=None):
        self.level = level.upper()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        self.logger.propagate = False


        formato = logging.Formatter(
            "%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s"
        )

        if consola:
            console_h = logging.StreamHandler()
            console_h.setLevel(self.level)
            console_h.setFormatter(formato)

            # filtro por nivel exacto
            console_h.addFilter(LevelFilter(self.level))
            self.logger.addHandler(console_h)

        if file_l:
            file_h = logging.FileHandler(file_l, mode="w")
            file_h.setLevel(self.level)
            file_h.setFormatter(formato)
            self.logger.addHandler(file_h)


            
            

    ## METODOS DEL OBJETO 
    def debug(self, msg):
        self.logger.debug(msg)
    

    def info(self, msg):
        self.logger.info(msg)
    

    def warning(self, msg):
        self.logger.warning(msg)
    

    def error(self, msg):
        self.logger.error(msg)
    

    def critical(self, msg):
        self.logger.critical(msg)

