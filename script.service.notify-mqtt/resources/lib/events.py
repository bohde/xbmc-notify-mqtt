import xbmc
import json

class EventPlayer(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        self.client = None
        self.path = "/player/status"
        self.paused = False

    def update(self, state, **kwargs):
        d = dict(kwargs)
        d['state'] = state
        if self.client:
            self.client.publish(self.path, json.dumps(d), retain=True, qos=1)

    def type(self):
        if self.isPlayingAudio():
            return 'audio'
        if self.isPlayingVideo():
            return 'video'
        return 'unknown'

    def status(self):
        if self.isPlaying():
            self.playing()
        else:
            self.update('stopped')

    def playing(self):
        status = 'playing' if not self.paused else 'paused'
        self.update(status, type=self.type(),
                    current=int(self.getTime()),
                    total=int(self.getTotalTime()))

    def onPlayBackStarted(self):
        self.paused = False
        self.playing()

    def onPlayBackStopped(self):
        self.paused = False
        self.update('stopped')

    def onPlayBackPaused(self):
        self.paused = True
        self.playing()

    def onPlayBackResumed(self):
        self.paused = False
        self.playing()
