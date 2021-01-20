'''
# <start id="list-calls-1"/>
>>> conn.rpush('list-key', 'last')          #A
1L                                          #A
>>> conn.lpush('list-key', 'first')         #B
2L
>>> conn.rpush('list-key', 'new last')
3L
>>> conn.lrange('list-key', 0, -1)          #C
['first', 'last', 'new last']               #C
>>> conn.lpop('list-key')                   #D
'first'                                     #D
>>> conn.lpop('list-key')                   #D
'last'                                      #D
>>> conn.lrange('list-key', 0, -1)
['new last']
>>> conn.rpush('list-key', 'a', 'b', 'c')   #E
4L
>>> conn.lrange('list-key', 0, -1)
['new last', 'a', 'b', 'c']
>>> conn.ltrim('list-key', 2, -1)           #F
True                                        #F
>>> conn.lrange('list-key', 0, -1)          #F
['b', 'c']                                  #F
# <end id="list-calls-1"/>
#A When we push items onto the list, it returns the length of the list after the push has completed
#B We can easily push on both ends of the list
#C Semantically, the left end of the list is the beginning, and the right end of the list is the end
#D Popping off the left items repeatedly will return items from left to right
#E We can push multiple items at the same time
#F We can trim any number of items from the start, end, or both
#END
'''

'''
# <start id="list-calls-2"/>
>>> conn.rpush('list', 'item1')             #A
1                                           #A
>>> conn.rpush('list', 'item2')             #A
2                                           #A
>>> conn.rpush('list2', 'item3')            #A
1                                           #A
>>> conn.brpoplpush('list2', 'list', 1)     #B
'item3'                                     #B
>>> conn.brpoplpush('list2', 'list', 1)     #C
>>> conn.lrange('list', 0, -1)              #D
['item3', 'item1', 'item2']                 #D
>>> conn.brpoplpush('list', 'list2', 1)
'item2'
>>> conn.blpop(['list', 'list2'], 1)        #E
('list', 'item3')                           #E
>>> conn.blpop(['list', 'list2'], 1)        #E
('list', 'item1')                           #E
>>> conn.blpop(['list', 'list2'], 1)        #E
('list2', 'item2')                          #E
>>> conn.blpop(['list', 'list2'], 1)        #E
>>>
# <end id="list-calls-2"/>
#A Let's add some items to a couple lists to start
#B Let's move an item from one list to the other, leaving it
#C When a list is empty, the blocking pop will stall for the timeout, and return None (which is not displayed in the interactive console)
#D We popped the rightmost item from 'list2' and pushed it to the left of 'list'
#E Blocking left-popping items from these will check lists for items in the order that they are passed, until they are empty
#END
'''

# <start id="exercise-update-token"/>


def update_token(conn, token, user, item=None):
    timestamp = time.time()
    conn.hset('login:', token, user)
    conn.zadd('recent:', token, timestamp)
    if item:
        key = 'viewed:' + token
        conn.lrem(key, item)  # A
        conn.rpush(key, item)  # B
        conn.ltrim(key, -25, -1)  # C
        conn.zincrby('viewed:', item, -1)
# <end id="exercise-update-token"/>
# A Remove the item from the list if it was there
# B Push the item to the right side of the LIST so that ZRANGE and LRANGE have the same result
# C Trim the LIST to only include the most recent 25 items
# END
