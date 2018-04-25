import pygame

class MolePop(pygame.sprite.Sprite):
    def __init__(self, sheet, frameSize):
        self.sheet = sheet
        self.size = frameSize
        self.sprites = []
        self.loadAllFrames()
        self.rate = 2

    def loadAllFrames(self):
        x = self.sheet.get_rect().width//self.size[0]
        y = self.sheet.get_rect().height//self.size[1]
        for i in range(x):
            for j in range(y):
                sp = self.sheet.subsurface(self.size[0]*i, 0, self.size[0], self.size[1])
                self.sprites.append(sp)




        