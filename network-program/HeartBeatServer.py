'''
Created on Feb 26, 2016

@author: xuyi
'''
import socket,threading,time,logging
import logging.config

logging.config.fileConfig("../logging.conf")
logger = logging.getLogger("root")

lock = threading.Lock()

hb_expiredTime=20
hb_host="127.0.0.1"
hb_port=9999
hb_maxListenThread=5
hb_watchPeriodTime=8

nodeInfo = {}
nodeAlive = set([])

def handleClient():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((hb_host,hb_port))
    s.listen(hb_maxListenThread)
    print('Waiting for connection...')
    
    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=parseSocket, args=(sock, addr))
        t.start()
    pass

def parseSocket(sock,addr):
    message = ""
    try:  
        while True:
            data = sock.recv(1024)
            if not data:
                break
            message += data.decode('utf-8')
        values = message.split(',')
        logger.debug("HeartBeatServer: get message from client ")
        if(values is None or len(values) < 2):
            logger.warn("HeartBeatServer: get error format of message: %s" % (message))
            return
        ip = values[0]
        timestamp = float(values[1])
        if(ip is None or not ip or ip == ""):
            ip = addr[0]
            logger.debug("HeartBeatServer: get ip from socket self %s" % (ip))
        logger.debug("HeartBeatServer: get message from client %s: %s" % (ip,message))
        lock.acquire()
        try:
            if(not (ip in nodeInfo)):
                nodeInfo[ip] = timestamp
            elif(nodeInfo[ip] < timestamp):
                nodeInfo[ip] = timestamp
        finally:
            lock.release()   
    except Exception as e:
        logger.error("HeartBeatServer: error occurs when parsing message",e)
    finally:
        sock.close()
    pass

def watchClient():
    while True:
        aliveNodes = set([])
        flag = False
        currentTimestamp = time.time()
        lock.acquire()
        try:
            if(not nodeInfo):
                logger.debug("HeartBeatServer: no node info saved in server")
            else:
                for node in nodeInfo:
                    if(currentTimestamp - nodeInfo[node] < hb_expiredTime):
                        aliveNodes.add(node)
                        flag = True
                        if(not (node in nodeAlive)):
                            nodeAlive.add(node)
                            logger.debug("HeartBeatServer: receive new node %s alive" % node)
                    else:
                        if(node in nodeAlive):
                            nodeAlive.remove(node)
                            flag = True
            if(flag):
                logger.debug("HeartBeatServer: alive node list %s",aliveNodes)
        finally:
            lock.release()   
        time.sleep(hb_watchPeriodTime)
    pass

if __name__ == '__main__':
    clientHandlerThread = threading.Thread(target=handleClient)
    clinetWatcherThread = threading.Thread(target=watchClient)
    clientHandlerThread.start()
    clinetWatcherThread.start()
    clientHandlerThread.join()
    clinetWatcherThread.join()    

    pass