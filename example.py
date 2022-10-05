from monolg import Monolg
from datetime import datetime

dt = datetime.now()

mlg = Monolg(verbose=True)
mlg.connect()

mlg.clear_logs()

# Types of logs
mlg.log('This is a log log')
mlg.info('This is a info log')
mlg.warning('This is a warning log')
mlg.error('This is a error log')
mlg.critical('This is a critical log')

# Closing the connection
mlg.close()
mlg.reopen()

mlg.info('This is after reopenning the connection',)