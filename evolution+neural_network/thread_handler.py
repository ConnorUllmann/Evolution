from threading import *

class ThreadHandler:

    def __init__(self):
        self.Reset()

    def AddThread(self, function, arguments=None, threadName=None):
        if arguments is None:
            thread = Thread(target=function, name=threadName)
        else:
            thread = Thread(target=function, args = arguments, name=threadName)
        self.threads.append(thread)
        return thread

    def RunThread(self, thread):
        if not thread.isAlive():
            thread.start()

    def RunThreads(self, threads):
        for thread in threads:
            self.RunThread(thread)

    def RunAllThreads(self):
        self.RunThreads(self.threads)

    def WaitForThreadsToFinish(self, threads):
        for thread in threads:
            thread.join()
            if thread in self.threads:
                self.threads.remove(thread)

    def WaitForAllThreadsToFinish(self):
        self.WaitForThreadsToFinish(self.threads)
        self.Reset()

    def Reset(self):
        self.threads = []
