import redis
import time
import threading

conn = redis.Redis()


def notrans():
    print(conn.incr('notrans:'))
    time.sleep(.1)
    conn.incr('notrans:', -1)


def runnotrans():
    if 1:
        for i in range(3):
            threading.Thread(target=notrans).start()
        time.sleep(.5)


def trans():
    pipeline = conn.pipeline()
    pipeline.incr('trans:')
    time.sleep(.1)

    pipeline.incr('trans:', -1)
    print(pipeline.execute()[0])


def runtrans():
    if 1:
        for i in range(3):
            threading.Thread(target=trans).start()
        time.sleep(.5)


# runnotrans()
runtrans()
