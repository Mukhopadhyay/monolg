from monolg import Monolg
from dataclasses import asdict
from datetime import datetime
from monolg._schemas import Base, Info

dt = datetime.now()

print(__file__)

b = Base('asd', 'message', dt, level='warning')
print(asdict(b))

b = Info('asd', 'message', dt)
print(asdict(b))

mlg = Monolg()
# mlg.connect()
mlg.log()

print('a')