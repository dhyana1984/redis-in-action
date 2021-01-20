'''
# <start id="zset-calls-1"/>
>>> conn.zadd('zset-key', 'a', 3, 'b', 2, 'c', 1)   #A
3                                                   #A
>>> conn.zcard('zset-key')                          #B
3                                                   #B
>>> conn.zincrby('zset-key', 'c', 3)                #C
4.0                                                 #C
>>> conn.zscore('zset-key', 'b')                    #D
2.0                                                 #D
>>> conn.zrank('zset-key', 'c')                     #E
2                                                   #E
>>> conn.zcount('zset-key', 0, 3)                   #F
2L                                                  #F
>>> conn.zrem('zset-key', 'b')                      #G
True                                                #G
>>> conn.zrange('zset-key', 0, -1, withscores=True) #H
[('a', 3.0), ('c', 4.0)]                            #H
# <end id="zset-calls-1"/>
#A Adding members to ZSETs in Python has the arguments reversed compared to standard Redis, so as to not confuse users compared to HASHes
#B Knowing how large a ZSET is can tell you in some cases if it is necessary to trim your ZSET
#C We can also increment members like we can with STRING and HASH values
#D Fetching scores of individual members can be useful if you have been keeping counters or toplists
#E By fetching the 0-indexed position of a member, we can then later use ZRANGE to fetch a range of the values easily
#F Counting the number of items with a given range of scores can be quite useful for some tasks
#G Removing members is as easy as adding them
#H For debugging, we usually fetch the entire ZSET with this ZRANGE call, but real use-cases will usually fetch items a relatively small group at a time
#END
'''

'''
# <start id="zset-calls-2"/>
>>> conn.zadd('zset-1', 'a', 1, 'b', 2, 'c', 3)                         #A
3                                                                       #A
>>> conn.zadd('zset-2', 'b', 4, 'c', 1, 'd', 0)                         #A
3                                                                       #A
>>> conn.zinterstore('zset-i', ['zset-1', 'zset-2'])                    #B
2L                                                                      #B
>>> conn.zrange('zset-i', 0, -1, withscores=True)                       #B
[('c', 4.0), ('b', 6.0)]                                                #B
>>> conn.zunionstore('zset-u', ['zset-1', 'zset-2'], aggregate='min')   #C
4L                                                                      #C
>>> conn.zrange('zset-u', 0, -1, withscores=True)                       #C
[('d', 0.0), ('a', 1.0), ('c', 1.0), ('b', 2.0)]                        #C
>>> conn.sadd('set-1', 'a', 'd')                                        #D
2                                                                       #D
>>> conn.zunionstore('zset-u2', ['zset-1', 'zset-2', 'set-1'])          #D
4L                                                                      #D
>>> conn.zrange('zset-u2', 0, -1, withscores=True)                      #D
[('d', 1.0), ('a', 2.0), ('c', 4.0), ('b', 6.0)]                        #D
# <end id="zset-calls-2"/>
#A We'll start out by creating a couple ZSETs
#B When performing ZINTERSTORE or ZUNIONSTORE, our default aggregate is sum, so scores of items that are in multiple ZSETs are added
#C It is easy to provide different aggregates, though we are limited to sum, min, and max
#D You can also pass SETs as inputs to ZINTERSTORE and ZUNIONSTORE, they behave as though they were ZSETs with all scores equal to 1
#END
'''


def publisher(n):
    time.sleep(1)
    for i in range(n):
        conn.publish('channel', i)
        time.sleep(1)


def run_pubsub():
    threading.Thread(target=publisher, args=(3,)).start()
    pubsub = conn.pubsub()
    pubsub.subscribe(['channel'])
    count = 0
    for item in pubsub.listen():
        print(item)
        count += 1
        if count == 4:
            pubsub.unsubscribe()
        if count == 5:
            break


'''
# <start id="pubsub-calls-1"/>
>>> def publisher(n):
...     time.sleep(1)                                                   #A
...     for i in xrange(n):
...         conn.publish('channel', i)                                  #B
...         time.sleep(1)                                               #B
...
>>> def run_pubsub():
...     threading.Thread(target=publisher, args=(3,)).start()
...     pubsub = conn.pubsub()
...     pubsub.subscribe(['channel'])
...     count = 0
...     for item in pubsub.listen():
...         print item
...         count += 1
...         if count == 4:
...             pubsub.unsubscribe()
...         if count == 5:
...             break
... 

>>> def run_pubsub():
...     threading.Thread(target=publisher, args=(3,)).start()           #D
...     pubsub = conn.pubsub()                                          #E
...     pubsub.subscribe(['channel'])                                   #E
...     count = 0
...     for item in pubsub.listen():                                    #F
...         print item                                                  #G
...         count += 1                                                  #H
...         if count == 4:                                              #H
...             pubsub.unsubscribe()                                    #H
...         if count == 5:                                              #L
...             break                                                   #L
...
>>> run_pubsub()                                                        #C
{'pattern': None, 'type': 'subscribe', 'channel': 'channel', 'data': 1L}#I
{'pattern': None, 'type': 'message', 'channel': 'channel', 'data': '0'} #J
{'pattern': None, 'type': 'message', 'channel': 'channel', 'data': '1'} #J
{'pattern': None, 'type': 'message', 'channel': 'channel', 'data': '2'} #J
{'pattern': None, 'type': 'unsubscribe', 'channel': 'channel', 'data':  #K
0L}                                                                     #K
# <end id="pubsub-calls-1"/>
#A We sleep initially in the function to let the SUBSCRIBEr connect and start listening for messages
#B After publishing, we will pause for a moment so that we can see this happen over time
#D Let's start the publisher thread to send 3 messages
#E We'll set up the pubsub object and subscribe to a channel
#F We can listen to subscription messages by iterating over the result of pubsub.listen()
#G We'll print every message that we receive
#H We will stop listening for new messages after the subscribe message and 3 real messages by unsubscribing
#L When we receive the unsubscribe message, we need to stop receiving messages
#C Actually run the functions to see them work
#I When subscribing, we receive a message on the listen channel
#J These are the structures that are produced as items when we iterate over pubsub.listen()
#K When we unsubscribe, we receive a message telling us which channels we have unsubscribed from and the number of channels we are still subscribed to
#END
'''
