class gameMap(object):
    def __init__(self, width, height, tNum = 9):
        self.width = width
        self.height = height
        self.tileSize = int(min(width,height)/tNum)
        self.origin = ((width - self.tileSize * tNum)/2,
                    (height - self.tileSize * tNum)/2)
        self.moles = {}

    def converPOS(self, pos):
        x = pos[0] - self.origin[0]
        y = pos[1] - self.origin[1]
        x = int((x - x % self.tileSize) + self.origin[0])
        y = int((x - y % self.tileSize) + self.origin[1])
        return (x,y)

    #def hitMole(self, pos):
