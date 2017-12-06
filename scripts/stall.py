import os
import sys
import time

print(sys.version_info)
print(sys.implementation)

def hehe(arg1):
    print('hehe')
    haha(arg1)

def haha(arg2):
    print('haha')
    foo(arg2)

def foo(arg3):
    print('foo')
    ifloat = float(arg3)
    jstr = str(ifloat)
    time.sleep(arg3)

if __name__ == '__main__':
    v1 = 100000
    hehe(v1)
