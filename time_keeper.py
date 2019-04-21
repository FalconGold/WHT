import time

class count:

    def __init__(self):
        self.now=0
        self.end=0
        self.total=0

    def start(self):
        self.now = time.time()
    
    def finish(self):
        self.end = time.time()
        self.total = self.end - self.now
        
        return dict({"day": int(self.total/86400), "hour": int(self.total/3600), "mins": int(self.total/60), "secs": int(self.total)%60})
        
        
