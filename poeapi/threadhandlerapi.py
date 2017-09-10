import threading
import config
from poeapi.poeapi import PoEAPI
import logging
import time

logger = logging.getLogger(__name__)

class ThreadHandlerAPI:
    threads = []
    classes = []
    WAITTIME = 1 

    def __init__(self, changeID, filters):
        
        changeIDs = self.getChangeIDs(changeID)

        for i in range(0, 5):
            api = PoEAPI(i, changeIDs[i])

            api.filters = filters

            self.classes.append(api)


    def initThreads(self):
        for apiClass in self.classes:
            self.threads.append(threading.Thread(target=apiClass.run))
    
    def runThreads(self):
        i = 0
        for thread in self.threads:
            logger.info('Starting Thread: ' + str(i))
            time.sleep(0.75)
            thread.start()
            i+=1
        

    def stopThreads():
        i=0
        for thread in self.threads:
            logger.info('Stopping Thread: ' + str(i))
            self.classes[i].run = False
            i += 1

    def getChangeIDs(self, changeID):
        ids = changeID.split('-')

        return [
            str(int(ids[0]) + 5000) + "-999999999999-999999999999-999999999999-999999999999",
            "999999999999-" + str(int(ids[1]) + 5000) + "-999999999999-999999999999-999999999999",
            "999999999999-999999999999-" + str(int(ids[2]) + 5000) + "-999999999999-999999999999",
            "999999999999-999999999999-999999999999-" + str(int(ids[3]) + 5000) + "-999999999999",
            "999999999999-999999999999-999999999999-999999999999-" + str(int(ids[4]) + 5000)
        ]

