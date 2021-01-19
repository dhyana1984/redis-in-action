
'''
# <start id="string-calls-1"/>
>>> import redis
>>> conn = redis.Redis()
>>> conn.get('key')             #A
>>> conn.incr('key')            #B
1                               #B
>>> conn.incr('key', 15)        #B
16                              #B
>>> conn.decr('key', 5)         #C
11                              #C
>>> conn.get('key')             #D
'11'                            #D
>>> conn.set('key', '13')       #E
True                            #E
>>> conn.incr('key')            #E
14                              #E
# <end id="string-calls-1"/>
#A When we fetch a key that does not exist, we get the None value, which is not displayed in the interactive console
#B We can increment keys that don't exist, and we can pass an optional value to increment by more than 1
#C Like incrementing, decrementing takes an optional argument for the amount to decrement by
#D When we fetch the key it acts like a string
#E And when we set the key, we can set it as a string, but still manipulate it like an integer
#END
'''


'''
# <start id="string-calls-2"/>
>>> conn.append('new-string-key', 'hello ')     #A
6L                                              #B
>>> conn.append('new-string-key', 'world!')
12L                                             #B
>>> conn.substr('new-string-key', 3, 7)         #C
'lo wo'                                         #D
>>> conn.setrange('new-string-key', 0, 'H')     #E
12                                              #F
>>> conn.setrange('new-string-key', 6, 'W')
12
>>> conn.get('new-string-key')                  #G
'Hello World!'                                  #H
>>> conn.setrange('new-string-key', 11, ', how are you?')   #I
25
>>> conn.get('new-string-key')
'Hello World, how are you?'                     #J
>>> conn.setbit('another-key', 2, 1)            #K
0                                               #L
>>> conn.setbit('another-key', 7, 1)            #M
0                                               #M
>>> conn.get('another-key')                     #M
'!'                                             #N
# <end id="string-calls-2"/>
#A Let's append the string 'hello ' to the previously non-existent key 'new-string-key'
#B When appending a value, Redis returns the length of the string so far
#C Redis uses 0-indexing, and when accessing ranges, is inclusive of the endpoints by default
#D The string 'lo wo' is from the middle of 'hello world!'
#E Let's set a couple string ranges
#F When setting a range inside a string, Redis also returns the total length of the string
#G Let's see what we have now!
#H Yep, we capitalized our 'H' and 'W'
#I With setrange we can replace anywhere inside the string, and we can make the string longer
#J We replaced the exclamation point and added more to the end of the string
#K If you write to a bit beyond the size of the string, it is filled with nulls
#L Setting bits also returns the value of the bit before it was set
#M If you are going to try to interpret the bits stored in Redis, remember that offsets into bits are from the highest-order to the lowest-order
#N We set bits 2 and 7 to 1, which gave us '!', or character 33
#END
'''
