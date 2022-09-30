# from monolg import Monolg

# mlg = Monolg()


from dataclasses import asdict
from datetime import datetime
from monolg._schemas import Base, Info

dt = datetime.now()

b = Base('asd', dt, 'warning')
print(asdict(b))

b = Info('asd', dt)
print(asdict(b))
