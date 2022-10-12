from monolg import Monolg

# Instantiating Monolg
mlg = Monolg(verbose=True, system_log=True)
# Connecting to locally running MongoDB
mlg.connect()

# mlg.clear_sys_logs()

# Clearing any pre-existing logs
# mlg.clear_logs()

# # Types of logs
# mlg.log('This is a log log')
# mlg.info('This is a info log')
# mlg.warning('This is a warning log')
# mlg.error('This is a error log')
# mlg.critical('This is a critical log')

# # Closing the connection
# mlg.close()
# # Reopenning connection
# mlg.reopen()
# # Logging again to check the if the connection is established
# mlg.info('This is after reopenning the connection',)
