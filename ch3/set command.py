

'''
# <start id="set-calls-1"/>
>>> conn.sadd('set-key', 'a', 'b', 'c')         #A
3                                               #A
>>> conn.srem('set-key', 'c', 'd')              #B
True                                            #B
>>> conn.srem('set-key', 'c', 'd')              #B
False                                           #B
>>> conn.scard('set-key')                       #C
2                                               #C
>>> conn.smembers('set-key')                    #D
set(['a', 'b'])                                 #D
>>> conn.smove('set-key', 'set-key2', 'a')      #E
True                                            #E
>>> conn.smove('set-key', 'set-key2', 'c')      #F
False                                           #F
>>> conn.smembers('set-key2')                   #F
set(['a'])                                      #F
# <end id="set-calls-1"/>
#A Adding items to the SET returns the number of items that weren't already in the SET
#B Removing items from the SET returns whether an item was removed - note that the client is buggy in that respect, as Redis itself returns the total number of items removed
#C We can get the number of items in the SET
#D We can also fetch the whole SET
#E We can easily move items from one SET to another SET
#F When an item doesn't exist in the first set during a SMOVE, it isn't added to the destination SET
#END
'''


'''
# <start id="set-calls-2"/>
>>> conn.sadd('skey1', 'a', 'b', 'c', 'd')  #A
4                                           #A
>>> conn.sadd('skey2', 'c', 'd', 'e', 'f')  #A
4                                           #A
>>> conn.sdiff('skey1', 'skey2')            #B
set(['a', 'b'])                             #B
>>> conn.sinter('skey1', 'skey2')           #C
set(['c', 'd'])                             #C
>>> conn.sunion('skey1', 'skey2')           #D
set(['a', 'c', 'b', 'e', 'd', 'f'])         #D
# <end id="set-calls-2"/>
#A First we'll add a few items to a couple SETs
#B We can calculate the result of removing all of the items in the second set from the first SET
#C We can also find out which items exist in both SETs
#D And we can find out all of the items that are in either of the SETs
#END
'''
