import random
class gameMap(object):
    def __init__(self, width, height, tNum = 9, time = 120):
        self.width = width
        # exclude the size of the UI banner a the bottom
        # banner is 10% height of the screen andthe full width of the screen
        self.height = int(height * 0.85)
        # calculate the sise of the each tiles
        self.tileSize = int(min(self.width,self.height)/tNum)
        # calculate the origin point of the tiles
        self.origin = ((self.width%self.tileSize)//2,
                    (self.height%self.tileSize)//2)
        # the map is a rectangle grid map
        self.mpSize = (int(self.width//self.tileSize), int(self.height//self.tileSize))
        self.moles = {} # to move to Moles class
        # dict of the map
        # key is the tuple of the index
        # value is true or false
        # true = field tile; false = grass tile
        self.map = {}
        # randomly generate the map
        for x in range(self.mpSize[0]):
            for y in range(self.mpSize[1]):
                self.map[(x,y)] = random.randint(0,1)
        # score of the farmer(s)
        self.scoreF = 0
        # score of the moles
        self.scoreM = 0
        # contdown time
        self.time = time
        # UI properties
        # backgroung color
        self.BGcolor = (20,50,20)
        # color of the fonts
        self.fontColor = (160,160,150)
        # size of the fonts
        self.fontSize = int(self.tileSize * 0.8)
        # font name
        self.fontName = 'Comic Sans MS'

    # convert the position to be fiting in the closest tile
    def converPOS(self, pos):
        index = self.posToIndex(pos)
        return self.indexToPos(index)

    # covert the positon to the index of the cloeset tile
    def posToIndex(self, pos):
        x = (pos[0] - self.origin[0])//self.tileSize
        y = (pos[1] - self.origin[1])//self.tileSize
        return (x, y)

    # conver the index value to the position on the map
    def indexToPos(self, index):
        x = self.origin[0] + self.tileSize * index[0]
        y = self.origin[1] + self.tileSize * index[1]
        return (x,y)

    # check if the tile is a field tile that a mole can show
    def isValidTile(self, pos):
        index = self.posToIndex(pos)
        return self.map[index] == 1

    # convert the time to formated string
    # assume the longest time for a game is less than a hour
    def getTime(self):
        minutes = str(self.time//60)
        seconds = str(self.time%60)
        if len(minutes) < 2:
            minutes = "0" + minutes
        if len(seconds) < 2:
            seconds = "0" + seconds
        return "%s : %s" %(minutes, seconds)

    @staticmethod
    def getPosCentered(sideLen, surface, direction):
        if direction == "x":
            return (sideLen - surface.get_rect().width)//2
        elif direction == "y":
            return (sideLen - surface.get_rect().height)//2


