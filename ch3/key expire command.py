'''
# <start id="other-calls-1"/>
>>> conn.set('key', 'value')                    #A
True                                            #A
>>> conn.get('key')                             #A
'value'                                         #A
>>> conn.expire('key', 2)                       #B
True                                            #B
>>> time.sleep(2)                               #B
>>> conn.get('key')                             #B
>>> conn.set('key', 'value2')
True
>>> conn.expire('key', 100); conn.ttl('key')    #C
True                                            #C
100                                             #C
# <end id="other-calls-1"/>
#A We are starting with a very simple STRING value
#B If we set a key to expire in the future, and we wait long enough for the key to expire, when we try to fetch the key, it has already been deleted
#C We can also easily find out how long it will be before a key will expire
#END
'''
