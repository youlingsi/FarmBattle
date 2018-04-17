class Moles(object):
    def __init__(self, showtime, num):
        # total number of clicks that are valid for spawning a mole
        self.clicks= 0
        # max number of the moles can controlec by the player
        self.num = num
        # time before the moles disappear
        self.show = showtime
        #list of the position of each mole
        self.pos = []
        #list of the lifes for each mole
        # 0-idle
        # >0- showing on the map
        # <0- dazzle
        self.states = [] 

    # alter the states along with the time passed
    def countDown(self):
        #loop through and change state of every mole
        #the value going towards 0
        for i in self.states:
            # when the mole is out, -1
            if i > 0:
                i -= 1
            # when the mole is dazzle +1
            elif i < 0:
                i += 1

    # click on the map and spawn a mole at the tile
    def spawnMoles(self, pos, gm):
        # add the number of click when the mole click occurs
        self.clicks += 1
        # calculate the index of the moles the click associated to
        index = self.clicks % self.num
        # check if the mole is at idle state
        if self.states[index] == 0:
            # check if the position is on a field
            if gm.isValidTile(pos):
                # spawn the mole at the position
                # change the states
                self.pos[index] = pos
                self.states[index] = self.show
        else:
            # if no moles spawned, restore the click count
            self.clicks -= 1

    # check if a mole is hit
    def moleHit(self, farmerClick,gm):
        # conver the farmClick pos to a position matching the mole pos
        covertedPos = gm.covertedPos(farmerClick)
        # loop through all the moles
        for i in range(len(self.pos)):
            if self.pos[i] == covertedPos:
                # revers the states to minus when the mole is dazzle
                self.states = (-1)*self.states
                break


