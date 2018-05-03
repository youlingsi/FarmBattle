class Farmer(object):
    def __init__(self):
        self.pos = (-100,-100)
        self.target = (-100,-100)
        #self.moveSteps = (0,0)
        #self.AllDirection = [(-1,0),(0,-1),(1,0),(0,1)]
        self.route = []
        self.moving = False        

    def getRoute(self, gm):
        if (not self.moving) and self.target[0]> 0:
            diff = (self.target[0] - self.pos[0],
                    self.target[1] - self.pos[1])
            if diff[0]!=0:
                dirX = diff[0]//abs(diff[0])
            else:
                dirX = 0
            if diff[1] != 0:
                dirY = diff[1]//abs(diff[1])
            else:
                dirY = 0
            steps = abs(diff[0]//gm.tileSize) + abs(diff[1]//gm.tileSize)
            currentX = self.pos[0]
            currentY = self.pos[1]
            routeX = []
            routeY = []
            for i in range(abs(diff[0]//gm.tileSize)):
                currentX += dirX * gm.tileSize
                routeX.append((currentX,currentY))
            for j in range(abs(diff[1]//gm.tileSize)):
                currentY += dirY * gm.tileSize
                routeX.append((currentX,currentY)) 
            self.route = routeX + routeY
            self.route.reverse()           
            self.moving = True

    def moveFarmer(self):
        if self.route == []:
            self.moving = False
            self.target = (-100,-100)
        if self.moving:
            self.pos = self.route[-1]
            self.route.pop()
            if len(self.route) == 0:
                self.target = (-100,-100)
                self.moving = False

    def encodeFarmer(self):
        strRoute = ""
        for rPos in self.route:
            strRoute += "%dp%dr"%(rPos[0],rPos[1])
        msg = "farmer=%dp%d=%dp%d=%s=%d"%(self.pos[0], self.pos[1],
                                            self.target[0], self.target[1],
                                            strRoute,int(self.moving))
        return msg

    @staticmethod
    def decodeFarmer(msg):
        msgList = msg.strip().split("=")[1:]
        strPos = msgList[0].split("p")
        pos = (int(strPos[0]), int(strPos[1]))
        strTarget = msgList[1].strip().split("p")
        target = (int(strTarget[0]), int(strTarget[1]))
        strRoute = msgList[2].strip().split("r")
        route = []
        for r in strRoute:
            if r != "":
                p = r.strip().split("p")
                ro = (int(p[0]), int(p[1]))
                route.append(ro)
        moving = int(msgList[3])
        return(pos, target,route,moving)

            




        


    


