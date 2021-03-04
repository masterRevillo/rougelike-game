import pygame.mixer

class SoundManager:

    def __init__(self):
        self.cacheSfx()

        self.sfx_bus = []

    def playBgm(self, file: str):
        pygame.mixer.music.load(file)
        pygame.mixer.music.set_volume(.25)
        pygame.mixer.music.play(-1, 0, 0)

    def pauseBgm(self):
        pygame.mixer.music.pause()

    def unpauseBgm(self):
        pygame.mixer.music.unpause()

    def queueSfx(self, sfx_name: str):
        if len(self.sfx) == 0:
            self.cacheSfx()
        self.sfx_bus.append(self.sfx[sfx_name])

    def playSfxQueue(self):
        if len(self.sfx_bus) > 0:
            for s in self.sfx_bus:
                s.play()
                self.sfx_bus.remove(s)

    def cacheSfx(self):
        pygame.mixer.init()
        self.sfx = {
            "scoot": pygame.mixer.Sound("assets/audio/scoot.wav"),
            "pling": pygame.mixer.Sound("assets/audio/pling.wav"),
            "chew": pygame.mixer.Sound("assets/audio/chew.wav"),
            "moan": pygame.mixer.Sound("assets/audio/moan.wav"),
            "pick": pygame.mixer.Sound("assets/audio/pick.wav"),
        }

    def clearSfxCache(self):
        self.sfx = {}


