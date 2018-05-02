import pygame

class spriteAni(pygame.sprite.Sprite):
    def __init__(self, sheet, frameSize, gridSize):
        self.sheet = sheet
        self.size = frameSize
        self.gridSize = gridSize
        self.sprites = []
        self.loadAllFrames()
        self.rate = 2

    def loadAllFrames(self):
        x = self.sheet.get_rect().width//self.size[0]
        y = self.sheet.get_rect().height//self.size[1]
        for i in range(x):
            group = []
            for j in range(y):
                sp = self.sheet.subsurface(self.size[0]*i, self.size[1]*j, self.size[0], self.size[1])
                sp = pygame.transform.scale(sp, (self.gridSize,self.gridSize))
                group.append(sp)
            self.sprites.append(group)




        