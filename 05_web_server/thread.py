import time
import threading

def test1():
    time.sleep(3)
    print('test1 exited')

print([x.name for x in threading.enumerate()])
threading.Thread(
    target=test1
).start()
print([x.name for x in threading.enumerate()])

time.sleep(5)
print([x.name for x in threading.enumerate()])
