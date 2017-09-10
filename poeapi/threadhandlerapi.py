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

            for filter in filters:
                api.addFilter(filter)

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
            ids[0] + "-999999999999-999999999999-999999999999-999999999999",
            "999999999999-" +ids[1] + "-999999999999-999999999999-999999999999",
            "999999999999-999999999999-" +ids[2] + "-999999999999-999999999999",
            "999999999999-999999999999-999999999999-" +ids[3] + "-999999999999",
            "999999999999-999999999999-999999999999-999999999999-" +ids[4]
        ]
