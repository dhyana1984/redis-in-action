import os
import time
import unittest
import uuid

import redis

'''
# <start id="persistence-options"/>
save 60 1000                        #A
stop-writes-on-bgsave-error no      #A
rdbcompression yes                  #A
dbfilename dump.rdb                 #A

appendonly no                       #B
appendfsync everysec                #B
no-appendfsync-on-rewrite no        #B
auto-aof-rewrite-percentage 100     #B
auto-aof-rewrite-min-size 64mb      #B

dir ./                              #C
# <end id="persistence-options"/>
#A Snapshotting persistence options
#B Append-only file persistence options
#C Shared option, where to store the snapshot or append-only file
#END
'''

# <start id="process-logs-progress"/>


def process_logs(conn, path, callback):  # K
    current_file, offset = conn.mget(  # A
        'progress:file', 'progress:position')  # A

    pipe = conn.pipeline()

    def update_progress():  # H
        pipe.mset({  # I
            'progress:file': fname,  # I
            'progress:position': offset  # I
        })
        pipe.execute()  # J

    for fname in sorted(os.listdir(path)):  # B
        if fname < current_file:  # C
            continue

        inp = open(os.path.join(path, fname), 'rb')
        if fname == current_file:  # D
            inp.seek(int(offset, 10))  # D
        else:
            offset = 0

        current_file = None

        for lno, line in enumerate(inp):  # L
            callback(pipe, line)  # E
            offset = int(offset) + len(line)  # F

            if not (lno+1) % 1000:  # G
                update_progress()  # G
        update_progress()  # G

        inp.close()
# <end id="process-logs-progress"/>
# A Get the current progress
# B Iterate over the logfiles in sorted order
# C Skip over files that are before the current file
# D If we are continuing a file, skip over the parts that we've already processed
# E Handle the log line
# F Update our information about the offset into the file
# G Write our progress back to Redis every 1000 lines, or when we are done with a file
# H This closure is meant primarily to reduce the number of duplicated lines later
# I We want to update our file and line number offsets into the logfile
# J This will execute any outstanding log updates, as well as to actually write our file and line number updates to Redis
# K Our function will be provided with a callback that will take a connection and a log line, calling methods on the pipeline as necessary
# L The enumerate function iterates over a sequence (in this case lines from a file), and produces pairs consisting of a numeric sequence starting from 0, and the original data
# END

# <start id="wait-for-sync"/>


def wait_for_sync(mconn, sconn):
    identifier = str(uuid.uuid4())
    mconn.zadd('sync:wait', {identifier: time.time()})  # A

    while not sconn.info()['master_link_status'] != 'up':  # B
        time.sleep(.001)

    while not sconn.zscore('sync:wait', identifier):  # C
        time.sleep(.001)

    deadline = time.time() + 1.01  # D
    while time.time() < deadline:  # D
        if sconn.info()['aof_pending_bio_fsync'] == 0:  # E
            break  # E
        time.sleep(.001)

    mconn.zrem('sync:wait', identifier)  # F
    mconn.zremrangebyscore('sync:wait', 0, time.time()-900)  # F
# <end id="wait-for-sync"/>
# A Add the token to the master
# B Wait for the slave to sync (if necessary)
# C Wait for the slave to receive the data change
# D Wait up to 1 second
# E Check to see if the data is known to be on disk
# F Clean up our status and clean out older entries that may have been left there
# END
