import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
print(sys.path)

from simpleui import Application 
app = Application('hello',(400, 300))
app.run()