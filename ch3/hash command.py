
'''
# <start id="hash-calls-1"/>
>>> conn.hmset('hash-key', {'k1':'v1', 'k2':'v2', 'k3':'v3'})   #A
True                                                            #A
>>> conn.hmget('hash-key', ['k2', 'k3'])                        #B
['v2', 'v3']                                                    #B
>>> conn.hlen('hash-key')                                       #C
3                                                               #C
>>> conn.hdel('hash-key', 'k1', 'k3')                           #D
True                                                            #D
# <end id="hash-calls-1"/>
#A We can add multiple items to the hash in one call
#B We can fetch a subset of the values in a single call
#C The HLEN command is typically used for debugging very large HASHes
#D The HDEL command handles multiple arguments without needing an HMDEL counterpart and returns True if any fields were removed
#END
'''

'''
# <start id="hash-calls-2"/>
>>> conn.hmset('hash-key2', {'short':'hello', 'long':1000*'1'}) #A
True                                                            #A
>>> conn.hkeys('hash-key2')                                     #A
['long', 'short']                                               #A
>>> conn.hexists('hash-key2', 'num')                            #B
False                                                           #B
>>> conn.hincrby('hash-key2', 'num')                            #C
1L                                                              #C
>>> conn.hexists('hash-key2', 'num')                            #C
True                                                            #C
# <end id="hash-calls-2"/>
#A Fetching keys can be useful to keep from needing to transfer large values when you are looking into HASHes
#B We can also check the existence of specific keys
#C Incrementing a previously non-existent key in a hash behaves just like on strings, Redis operates as though the value had been 0
#END
'''
