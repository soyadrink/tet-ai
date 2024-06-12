from threading import Timer

class Autolock:
    def __init__(self, time):
        self.finished = False
        self.time = time
        self.timer = Timer(self.time, self.finish)
        self.mcount = 0
        self.rcount = 0

    def finish(self):
        self.finished = True

    def reset_timer(self):
        self.finished = False
        self.timer.cancel()
        self.timer = Timer(self.time, self.finish)
        self.timer.start()

    def check_timer(self):
        if self.finished:
            return True
        return False
    
    def increment(self, inc, touching):
        if inc == 0:
            self.mcount += 1
        elif inc == 1:
            if touching:
                self.rcount += 1
            else:
                self.rcount += 0.5
        if touching:
            if self.mcount + self.rcount >= 15:
                return True
            return False
        else:
            if self.rcount >= 15:
                return True
            return False
    
    def reset_counter(self):
        self.mcount = 0
        self.rcount = 0