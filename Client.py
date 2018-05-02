import socket, queue, threading
import pygame
import classGameMap
import classMoles
import os
import random
import classOpenScene

# decode the info receved from the server and put it into a message queue
# From:

###################################
#       Socket Server Demo        #
#         by Rohan Varma          #
#      adapted by Kyle Chin       #
# further adapted by Matthew Kong #
###################################
def handle_server_msgs(server, msgs_q, bufsize=16):
    server.setblocking(True)
    msg_stream = ''
    while True:
        msg_stream += server.recv(bufsize).decode()
        while '\n' in msg_stream:
            newline_index = msg_stream.index('\n')
            ready_msg = msg_stream[:newline_index]
            msg_stream = msg_stream[newline_index + 1 :]
            msgs_q.put(ready_msg)

# converte the string represnt of a tuple with two int to real tuple
def tupleFromMSG(s):
    s = s.strip()[1:].split(",")
    return (int(s[0]), int(s[1]))

# load the mapInfo sent from the server into the client game map
def loadMap(strMap, gm):
    s = strMap[2:-2].split("], [")
    lstFalse = s[0][:-1].split("), ")
    lstTrue = s[1][:-1].split("),")
    count = 0
    countT = 0
    countF = 0
    for tF in lstFalse:
        count +=1
        countF += 1
        gm.map[tupleFromMSG(tF)] = 0
    for tT in lstTrue:
        count += 1
        countT += 1
        gm.map[tupleFromMSG(tT)] = 1

def updateGame(strState, gm):
    s = strState.strip()[1:].split(",")
    gm.gameState = int(s[0])
    gm.time = int(s[1])
    gm.scoreF = int(s[2])
    gm.scoreM = int(s[3])
    if gm.gameState == 1:
        print("end")
    elif gm.gameState == -1:
        print("Opening")
    else:
        print("gameON")

# draw the base map
def drawMap(screen,field, grass, gm):
    # Clear the screen and set the screen background
    screen.fill(gm.BGcolor)
    for tile in gm.map:
        if gm.map[tile] == 1:
            screen.blit(field, gm.indexToPos(tile))
        else:
            screen.blit(grass, gm.indexToPos(tile))

# draw the UI Element Including the scores, the time left 
def drawUI(width, height, screen, gm, myfont):
    sFarmer = myfont.render("Farmer", False, gm.fontColor)
    sMole = myfont.render("Moles", False, gm.fontColor)
    sTime = myfont.render("Time Left", False, gm.fontColor) 
    farmerScore = myfont.render(str(gm.scoreF), False, gm.fontColor)
    moleScore = myfont.render(str(gm.scoreM), False, gm.fontColor)
    time = myfont.render(gm.getTime(), False, gm.fontColor)               
    sFarmPos = (gm.origin[0] + gm.getPosCentered(width/3, sFarmer, "x"), 
            gm.height+gm.getPosCentered(height*0.15/2, sFarmer, "y"))
    sMolePos = (gm.origin[0] + width/ 3*2 + gm.getPosCentered(width/3, sMole, "x"), 
            gm.height+gm.getPosCentered(height*0.15/2, sMole, "y"))
    sTimePos = (gm.origin[0] + width/ 3 + gm.getPosCentered(width/3, sTime, "x"), 
            gm.height+gm.getPosCentered(height*0.15/2, sTime, "y"))
    farmPos = (gm.origin[0] + gm.getPosCentered(width/3, farmerScore, "x"), 
            gm.height+height*0.15/2+gm.getPosCentered(height*0.15/2, farmerScore, "y"))
    molePos = (gm.origin[0] + width/ 3*2 + gm.getPosCentered(width/3, moleScore, "x"), 
            gm.height+height*0.15/2+gm.getPosCentered(height*0.15/2, moleScore, "y"))
    timePos = (gm.origin[0] + width/ 3 + gm.getPosCentered(width/3, time, "x"), 
            gm.height+height*0.15/2+gm.getPosCentered(height*0.15/2, time, "y"))
    screen.blit(sFarmer,sFarmPos)
    screen.blit(sMole,sMolePos)
    screen.blit(sTime,sTimePos)
    screen.blit(farmerScore,farmPos)
    screen.blit(moleScore,molePos)
    screen.blit(time,timePos)

# Draw the Opening scene:
def drawOpen(screen,farmer, mole, myfont, gm):
    screen.fill(gm.BGcolor)

##AI of the moles. spawn a mole 
def moleAI(gm,server):
    toSpawn = random.randint(0,1)
    if toSpawn:
        x = random.randint(gm.origin[0],gm.width-gm.origin[0])
        y = random.randint(gm.origin[1],gm.height-gm.origin[1])
        pos = gm.convertPOS((x,y))
        server.send(("%d %d %d %s\n"%(pos[0], pos[1],1,"AI")).encode())

def farmerAI(gm, server):
    toCapture = random.randint(0,10)
    if toCapture == 5:
        keyList = list(gm.moles.keys())
        i = random.randint(0,len(keyList)-1)
        try:
            mPos = gm.moles[keyList[i]][1]
            pos = mPos[random.randint(0,len(mPos)-1)]
            print(pos)
            server.send(("%d %d %d %s\n"%(pos[0], pos[1],0,"AI")).encode())
        except:
            pass


# run the game        
def run(server, msgs_q, gm, width, height):
    pygame.init()
    # create game screen
    screen=pygame.display.set_mode([width,height])
    # load images
    moleImage = pygame.image.load(os.path.join('Graphic', 'MoleUp.png'))
    moleImage = pygame.transform.scale(moleImage, (gm.tileSize,gm.tileSize))
    # Load ground tiles
    grass = pygame.image.load(os.path.join('Graphic', 'Grass.png'))
    grass = pygame.transform.scale(grass, (gm.tileSize,gm.tileSize))
    field = pygame.image.load(os.path.join('Graphic', 'Field.png'))
    field = pygame.transform.scale(field, (gm.tileSize,gm.tileSize))
    # load sprite sheet
    moleSheet = pygame.image.load(os.path.join('Graphic', 'MoleUp.png'))
    #moleAni = ClassMolePopAni.MolePop(moleSheet,(64,64))
    farmerSheet = pygame.image.load(os.path.join('Graphic', 'MoleUp.png'))
    # define Fonts
    myfont = pygame.font.SysFont(gm.fontName, gm.fontSize)
    titleFont = pygame.font.SysFont(gm.titleFont, gm.titleSize)
    


    done = False
    clock = pygame.time.Clock()
    timer = 0


    while not done:
    
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(30)

        timer += 1
        if timer % 30 == 0:
            server.send("update\n".encode())

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True
                pygame.quit()
            else:
                if gm.gameState == 0:       
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = gm.convertPOS(pygame.mouse.get_pos())
                        if (pos[0] > 0 and pos[0] < gm.width
                            and pos[1] > 0 and pos[1] < gm.width):
                            server.send(("%d %d %d %s\n"%(pos[0], pos[1],gm.playerRole,"Pl")).encode())

        if not done:
            if msgs_q.qsize() > 0:
                msg = msgs_q.get()
                msgs_q.task_done()
                if (msg.startswith('newconn') or
                    msg.startswith('existingconn') or
                    msg.startswith('myid')):
                    newID = msg.split()[1]
                    gm.moles[newID] = ""
                elif (msg.strip().startswith("?")):
                    updateGame(msg.strip(), gm)
                elif (msg.strip().startswith("!")):
                    loadMap(msg.strip()[1:], gm)
                else:
                    infoList = msg.split("+")
                    thatID = int(infoList[0])
                    gm.moles[thatID]=classMoles.Moles.decodeMole(infoList[1])

                if gm.gameState == 0:
                    # AI generate moles and farmers
                    if timer % 10 == 0 and gm.mAIOn:
                        moleAI(gm,server)
                    if timer % 15 == 0 and gm.fAIOn:
                        farmerAI(gm,server)
                    drawMap(screen,field,grass,gm)
                    drawUI(width,height,screen,gm,myfont)
                    
                    # draw all moles
                    for cID in gm.moles:
                        try:
                            mState = gm.moles[cID][0]
                            mPos = gm.moles[cID][1]
                            for i in range(len(mState)):
                                pos = mPos[i]
                                if mState[i] > 0:
                                    screen.blit(moleImage, pos)
                                    textsurface = myfont.render(str(cID)+"I", False, (0, 0, 0))
                                    screen.blit(textsurface,pos)
                                elif mState[i] < 0:
                                    #moleAni.moleSinkAni(screen,pos)
                                    screen.blit(moleImage, pos)
                                    textsurface = myfont.render(str(cID)+"D", False, (0, 0, 0))
                                    screen.blit(textsurface,pos)
                        except:
                            continue
    
                # Go ahead and update the screen with what we've drawn.
                # This MUST happen after all the other drawing commands.
                pygame.display.flip()
    
    # Be IDLE friendly
    pygame.quit()


def play(width = 800, height = 600):

    HOST = ''
    PORT = 50003

    msgs_q = queue.Queue()

    server = socket.socket()
    server.connect((HOST, PORT))

    threading.Thread(target=handle_server_msgs, args=(server, msgs_q)).start()

    gm = classGameMap.gameMap(width,height)
    op = classOpenScene.OpenScene(width,height)
    #mole = classMoles.Moles()


    #role = int(input("0=Farmer; 1 = moles"))
    #mAI = True
    #fAI = True

    run(server, msgs_q, gm, width,height)

if __name__ == '__main__':
    play()
