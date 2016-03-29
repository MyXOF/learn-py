'''
Created on Feb 26, 2016

@author: xuyi
'''
import socket,threading,time,datetime,logging
import logging.config

hb_periodTime=5
hb_serverIP="127.0.0.1"
hb_port=9999

hb_clientIP = "192.168.1.1"

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("root")

def sendHeartBeat():
    logging.info("HeartBeatClient: heart beat client thread start")
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((hb_serverIP, hb_port))
            s.send(next(generateMessage()))
            time.sleep(hb_periodTime)
        except Exception as e:
            logging.error("HeartBeatClient: error occurs when client send packge to server",e)
        finally:
            pass
    pass

def generateMessage():
    IP = hb_clientIP
    while True:
        timestamp = time.time()
        message = IP + "," + str(timestamp)
        logger.debug("HeartBeatClient: generate message : %s" % (message))
        yield message.encode('utf-8')
    pass

if __name__ == '__main__':
    logger.debug("HeartBeatClient: ip is %s, port is %d, periodTime is %d" % (hb_serverIP,hb_port,hb_periodTime))
    client = threading.Thread(target=sendHeartBeat())
    client.start()
    client.join()
