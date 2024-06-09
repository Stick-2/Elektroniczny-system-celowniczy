# ulogging.py
class Logger:
    def debug(self, msg):
        pass
    def info(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        pass
    def critical(self, msg):
        pass
    def setLevel(self,msg):
        pass
    def exc(self, msg, *args, **kwargs):
        pass

def getLogger(name):
    return Logger()

# Definiowanie poziomów logowania
DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50
EXCEPTION = 60

def basicConfig(level):
    pass
