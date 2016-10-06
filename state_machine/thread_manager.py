import threading

class ThreadManager:

    def Clear(self):
        self.threads = []

    def Add(self, function, arguments=None, threadName=None):
        if threadName is None:
            threadName = "thread #{0}".format(self.threadsCreated)
        
        if arguments is None:
            thread = threading.Thread(name=threadName, target=function)
        else:
            thread = threading.Thread(name=threadName, target=function, args=arguments)
        self.threads.append(thread)
        
        self.threadsCreated += 1
        return thread

    def Run(self, threads):
        for thread in threads:
            if not thread.isAlive():
                thread.start()
            
    def RunAll(self):
        self.Run(self.threads)

    def Wait(self, threads):
        for thread in threads:
            thread.join()
            if thread in self.threads:
                self.threads.remove(thread)

    def WaitAll(self):
        for thread in self.threads:
            thread.join()
        self.Clear()

    def __init__(self):
        self.Clear()
        self.threadsCreated = 0
