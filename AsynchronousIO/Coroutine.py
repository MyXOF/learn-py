# -*- coding: utf-8 -*-

'''
Created on Feb 21, 2016

@summary: Python的yield不但可以返回一个值，它还可以接收调用者发出的参数
@author: xuyi
'''
def consume():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    #启动生成器
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

if __name__ == '__main__':
    c = consume()
    produce(c)

'''
对于 n = yield r 的理解要和c.send(None)和c.send(n)结合起来看，在运行produce(c)后的流程：
c.send(None) -> r='' -> n = yield r (这一步实际进行的是：Resumes the execution and “sends” a value into the generator function，The value argument becomes the result of the current yield expression. 即 n = None)
-> if not n: -> return -> n = 0 -> n = n + 1 -> print('[PRODUCER] Producing %s...' % n)
-> r = c.send(n) (Resumes the execution and “sends” a value into the generator function，The value argument becomes the result of the current yield expression.即 n = 1)
->  print('[CONSUMER] Consuming %s...' % n) -> r = '200 OK' -> n = yield r (实际执行的只有 yield r) 
-> r = c.send(n) (The send() method returns the next value yielded by the generator, 即n = '200 OK')-> print('[PRODUCER] Consumer return: %s' % r) -> while

ps:部分循环部分流程未展示，不影响理解就是了。
ps2：如果能标色的话，把consumer()和produce()部分的按不同颜色标识应该会更好理解
ps3：对于这部分的理解主要还是对于generator.send()的理解。
'''
    