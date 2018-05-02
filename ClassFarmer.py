class Farmer(object):
    def __init__(self, playerID, pos):
        self.player = playerID
        self.pos = pos
        self.AllDirection = [(-1,0),(0,-1),(1,0),(0,1)]
        self.route = []

    def moveFarmer(self,timer):
        length = len(self.route)
        if length != 0:
            index = timer % length
            self.pos = self.route[index]
            if index == length -1:
                self.route.clear

    


