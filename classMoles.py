class Moles(object):
    def __init__(self, showtime = 2, num=2):
        # total number of clicks that are valid for spawning a mole
        self.clicks= 0
        # max number of the moles can be controled by the player
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
        # init the states dict based on number of moles
        for i in range(num):
            self.pos.append((-1,-1))
            self.states.append(0)

    def __repr__(self):
        strState = ""
        strPos = ""
        for i in range(len(self.states)):
            strState += str(self.states[i]) + "st"
            strPos += repr(self.pos[i]) + "po"
        msg = (strState[:-2] + "&" + strPos[:-2] + 
                "&" + str(self.show)+"&"+str(self.num))
        return msg

    # alter the states along with the time passed
    def countDown(self):
        #loop through and change state of every mole
        #the value going towards 0
        succesCount = 0
        for i in range(len(self.states)):
            # when the mole is out, -1
            if self.states[i] > 0:
                self.states[i] -= 1
                if self.states[i] == 0:
                    self.pos[i] = (-1,-1)
                    succesCount += 1
            # when the mole is dazzle +1
            elif self.states[i] < 0:
                self.states[i] += 1
                if self.states[i] == 0:
                    self.pos[i] = (-1,-1)
        return succesCount

                    



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
                self.pos[index] = gm.convertPOS(pos)
                self.states[index] = self.show
        else:
            # if no moles spawned, restore the click count
            self.clicks -= 1
        return None

    # check if a mole is hit
    def moleHit(self, farmerClick,gm):
        # conver the farmClick pos to a position matching the mole pos
        convertedPos = gm.convertPOS(farmerClick)
        # loop through all the moles
        for i in range(len(self.pos)):
            if self.pos[i] == convertedPos and self.states[i]>0:
                # revers the states to minus when the mole is dazzle
                self.states[i] = (-1)*self.states[i]
                return True
        return False
        

    @staticmethod
    def decodeMole(reprMsg):
        s = reprMsg.strip().split("&")
        strStates = s[0].strip().split("st")
        strPos = s[1].strip().split("po")
        states = []
        pos = []
        show = int(s[2])
        num = int(s[3])
        for i in range(len(strStates)):
            states.append(int(strStates[i]))
            tp = strPos[i].strip()[1:-1].split(",")
            pos.append((int(tp[0]), int(tp[1])))
        return (states,pos,show,num)



