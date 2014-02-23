import xbmc

class EventPlayer(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        self.client = None
        self.path = "/player/status"

    def update(self, state):
        if self.client:
            self.client.publish(self.path, state, retain=True, qos=1)

    def onPlayBackStarted(self):
        self.update('playing')

    def onPlayBackStopped(self):
        self.update('stopped')

    def onPlayBackPaused(self):
        self.update('paused')

    def onPlayBackResumed(self):
        self.update('playing')
