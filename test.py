import threading



def a():
    count = 0
    while True:
        print('1번째 ',count)
        count += 1

def b():
    count = 0
    while True:
        print('2번째 ',count)
        count += 1
def c():
    count = 0
    while True:
        print('3번째 ',count)
        count += 1

a2 = threading.Thread(target=a)
a2.daemon = True
a2.start()

b2 = threading.Thread(target=b)
b2.daemon = True
b2.start()

c2 = threading.Thread(target=c)
c2.daemon = True
c2.start()
