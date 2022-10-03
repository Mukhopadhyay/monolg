from monolg import Monolg
from dataclasses import asdict
from datetime import datetime
from monolg._schemas import Base, Info, Schema

dt = datetime.now()

b = Info(
    'monolg', 'this is the test message', datetime.now(), {},
    additional_info='This is additional kwarg'
)

print(b.to_dict())

# b = Base('asd', 'message', dt, level='warning')
# print(asdict(b))

# b = Info('asd', 'message', dt)
# print(asdict(b))

# mlg = Monolg()
# mlg.connect()

# mlg.clear_logs()
# # Types of logs
# mlg.log('This is a log log')
# mlg.info('This is a info log')
# mlg.warning('This is a warning log')
# mlg.critical('This is a critical log')

# # Closing the connection
# mlg.close()
# mlg.log('This is a test log')
