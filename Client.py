import socket, queue, threading
import pygame
import classGameMap
import classMoles
import os
import random
import classOpenScene

###################################################
########### Socket Helper Functions  ##############
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

####################################################
######### Opening Scene Helper Functions ###########

# Check if the mouse clicked on the surface object
def clickCheck(surf, surPos, pos):
    rec = surf.get_rect()
    rec = rec.move(surPos)
    return rec.collidepoint(pos)

# Calculate the positions and construct the opening Scene
def constructOpening(screen, opSce,mole, farmer):
    # generate fonts
    opSce.allElement["fTitle"] = pygame.font.SysFont(opSce.titleFont, opSce.titleSize)
    opSce.allElement["fSelection"] = pygame.font.SysFont(opSce.fontName, opSce.fontSize)
    # define all texts and frames
    opSce.allElement["sTitle"] = opSce.allElement["fTitle"].render(opSce.gameTitle, False, opSce.titleColor)
    opSce.allElement["sOpt1"] = opSce.allElement["fSelection"].render(opSce.opt1, False, opSce.fontColor)
    opSce.allElement["sOpt2"] = opSce.allElement["fSelection"].render(opSce.opt2, False, opSce.fontColor)
    opSce.allElement["sMAIOn"] = opSce.allElement["fSelection"].render(opSce.sMAIOn, False, opSce.fontColor)
    opSce.allElement["sMAIOff"] = opSce.allElement["fSelection"].render(opSce.sMAIOff, False, opSce.fontColor)
    opSce.allElement["sFAIOn"] = opSce.allElement["fSelection"].render(opSce.sFAIOn, False, opSce.fontColor)
    opSce.allElement["sFAIOff"] = opSce.allElement["fSelection"].render(opSce.sFAIOff, False, opSce.fontColor)
    opSce.allElement["mole"] = mole
    opSce.allElement["farmer"] = farmer
    opSce.allElement["sLoading"] = opSce.allElement["fSelection"].render(opSce.loading, False, opSce.fontColor)
    # define all positions
    opSce.allElement["sTitlePos"] = (classGameMap.gameMap.getPosCentered(opSce.width,opSce.allElement["sTitle"],"x"), 
                opSce.height//4)
    opSce.allElement["sOpt1Pos"]=(classGameMap.gameMap.getPosCentered(opSce.width,opSce.allElement["sOpt1"],"x"), 
                opSce.height//2)
    opSce.allElement["molePos"] = (classGameMap.gameMap.getPosCentered(opSce.width//2,mole,"x"), 
                opSce.height//3*2)
    opSce.allElement["farmerPos"] = (opSce.width//2+classGameMap.gameMap.getPosCentered(opSce.width//2,farmer,"x"), 
                opSce.height//3*2)
    opSce.allElement["sOpt2Pos"]=(classGameMap.gameMap.getPosCentered(opSce.width,opSce.allElement["sOpt2"],"x"), 
                opSce.height//2)
    opSce.allElement["sMAIOnPos"]=(classGameMap.gameMap.getPosCentered(opSce.width//2,opSce.allElement["sMAIOn"],"x"), 
                opSce.height//4*3)
    opSce.allElement["sMAIOffPos"]=(opSce.width // 2 + 
                classGameMap.gameMap.getPosCentered(opSce.width//2,opSce.allElement["sMAIOff"],"x"), 
                opSce.height//4*3)
    opSce.allElement["sFAIOnPos"]=(classGameMap.gameMap.getPosCentered(opSce.width//2,opSce.allElement["sFAIOn"],"x"), 
                opSce.height/5*3)
    opSce.allElement["sFAIOffPos"]=(opSce.width // 2 + 
                classGameMap.gameMap.getPosCentered(opSce.width//2,opSce.allElement["sFAIOff"],"x"), 
                opSce.height//5*3)
    opSce.allElement["sLoadingPos"] = (classGameMap.gameMap.getPosCentered(opSce.width,opSce.allElement["sLoading"],"x"), 
                opSce.height//2)

# Draw the opening Scene
def drawOpening(screen, opSce):
    screen.fill(opSce.BGcolor)
    RED = (255,0,0)
    assert(opSce.allElement!={})
    screen.blit(opSce.allElement["sTitle"],opSce.allElement["sTitlePos"])
    if opSce.selectionStage == 0:
        screen.blit(opSce.allElement["sOpt1"],opSce.allElement["sOpt1Pos"])
        screen.blit(opSce.allElement["farmer"],opSce.allElement["farmerPos"])
        screen.blit(opSce.allElement["mole"],opSce.allElement["molePos"])
        if opSce.playerRole == 0:
            rec = opSce.allElement["farmer"].get_rect()
            rec = rec.move(opSce.allElement["farmerPos"])
            pygame.draw.rect(screen, RED, rec, 2)
        else:
            rec = opSce.allElement["mole"].get_rect()
            rec = rec.move(opSce.allElement["molePos"])
            pygame.draw.rect(screen, RED, rec, 2)
    elif opSce.selectionStage >= 1 and opSce.selectionStage < 3:
        screen.blit(opSce.allElement["sOpt2"],opSce.allElement["sOpt1Pos"])
        screen.blit(opSce.allElement["sMAIOn"],opSce.allElement["sMAIOnPos"])
        screen.blit(opSce.allElement["sMAIOff"],opSce.allElement["sMAIOffPos"])
        screen.blit(opSce.allElement["sFAIOn"],opSce.allElement["sFAIOnPos"])
        screen.blit(opSce.allElement["sFAIOff"],opSce.allElement["sFAIOffPos"])
        if opSce.mAIon:
            rec = opSce.allElement["sMAIOn"].get_rect()
            rec = rec.move(opSce.allElement["sMAIOnPos"])
            pygame.draw.rect(screen, RED, rec, 2)
        else:
            rec = opSce.allElement["sMAIOff"].get_rect()
            rec = rec.move(opSce.allElement["sMAIOffPos"])
            pygame.draw.rect(screen, RED, rec, 2)
        if opSce.fAIon:
            rec = opSce.allElement["sFAIOn"].get_rect()
            rec = rec.move(opSce.allElement["sFAIOnPos"])
            pygame.draw.rect(screen, RED, rec, 2)
        else:
            rec = opSce.allElement["sFAIOff"].get_rect()
            rec = rec.move(opSce.allElement["sFAIOffPos"])
            pygame.draw.rect(screen, RED, rec, 2)
    else:
        screen.blit(opSce.allElement["sLoading"], opSce.allElement["sLoadingPos"])

###################################################
########### Game Scene Helper Functions ###########

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

# update the statues of moles
def updateGame(strState, gm):
    s = strState.strip()[1:].split(",")
    gm.gameState = int(s[0])
    gm.time = int(s[1])
    gm.scoreF = int(s[2])
    gm.scoreM = int(s[3])

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

<<<<<<< HEAD
# Draw the Opening scene:
def drawOpen(screen,farmer, mole, myfont, gm):
    screen.fill(gm.BGcolor)

=======

###################################
######## Ending Scene #############

def drawEnding(width, height, screen, gm, myfont):
    pos = (width/2, height/2)
    winMsg = ""
    if gm.scoreF > gm.scoreM:
        winMsg = "Farmer Team Wins!"
    elif gm.scoreF < gm.scoreM:
        winMsg = "Mole Team Wins!"
    else:
        winMsg = "It's a tie!"
    win = myfont.render(winMsg, False, gm.fontColor)
    screen.blit(win,pos)


###################################
###### Game AIs ###################
>>>>>>> 5039ed1261ecaad475738703d0384ace26f87944
##AI of the moles. spawn a mole 
def moleAI(gm,server):
    toSpawn = random.randint(0,1)
    if toSpawn:
        x = random.randint(gm.origin[0],gm.width-gm.origin[0])
        y = random.randint(gm.origin[1],gm.height-gm.origin[1])
        pos = gm.convertPOS((x,y))
        server.send(("%d %d %d %s\n"%(pos[0], pos[1],1,"AI")).encode())

## AI of the Farmer
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

################################################################
###############  Main Game Play ################################
# run the game        
<<<<<<< HEAD
def run(server, msgs_q, gm, width, height):
=======
def run(server, msgs_q, opSce, gm, width, height):
>>>>>>> 5039ed1261ecaad475738703d0384ace26f87944
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
<<<<<<< HEAD
    titleFont = pygame.font.SysFont(gm.titleFont, gm.titleSize)
    


=======
    constructOpening(screen,opSce,moleImage,moleImage)
    
>>>>>>> 5039ed1261ecaad475738703d0384ace26f87944
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
        # Handle the imput and events
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
<<<<<<< HEAD
=======
                elif gm.gamestate == -1:
                    # keyboard suport for selecting the roles and AIs
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            if opSce.selectionStage == 0:
                                opSce.playerRole = (opSce.playerRole + 1)%2
                            elif opSce.selectionStage == 1:
                                opSce.fAIon = not opSce.fAIon
                            elif opSce.selectionStage == 2:
                                opSce.mAIon = not opSce.mAIon
                        if event.key == pygame.K_RETURN:
                            if opSce.selectionStage < 3:
                                opSce.selectionStage += 1
                        elif (event.key == pygame.K_ESCAPE 
                                and opSce.selectionStage > 0
                                and opSce.selectionStage < 3):
                            opSce.selectionStage -= 1
                    # mouse click support for selecting roles and the AIs
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        mousePos = pygame.mouse.get_pos()
                        if opSce.selectionStage == 0:
                            if clickCheck(opSce.allElement["mole"], opSce.allElement["molePos"],mousePos):
                                opSce.playerRole = 1
                                opSce.selectionStage +=1                                
                            elif clickCheck(opSce.allElement["farmer"],opSce.allElement["farmerPos"],mousePos):
                                opSce.playerRole = 0
                                opSce.selectionStage +=1
                        elif opSce.selectionStage == 2:
                            if clickCheck(opSce.allElement["sMAIOn"],opSce.allElement["sMAIOnPos"],mousePos):
                                opSce.mAIon = True
                                opSce.selectionStage += 1
                            elif clickCheck(opSce.allElement["sMAIOff"],opSce.allElement["sMAIOffPos"],mousePos):
                                opSce.mAIon = False
                                opSce.selectionStage += 1
                        elif opSce.selectionStage == 1:
                            if clickCheck(opSce.allElement["sFAIOn"],opSce.allElement["sFAIOnPos"],mousePos):
                                opSce.fAIon = True
                                opSce.selectionStage +=1
                            elif clickCheck(opSce.allElement["sFAIOff"],opSce.allElement["sFAIOffPos"],mousePos):
                                opSce.fAIon = False
                                opSce.selectionStage +=1
                                opSce.selectionTogm(gm)
                                server.send("ready\n".encode())

                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                        if opSce.selectionStage > 0 and opSce.selectionStage < 3:
                            opSce.selectionStage -=1

>>>>>>> 5039ed1261ecaad475738703d0384ace26f87944

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
                elif gm.gameState == -1:
                    drawOpening(screen,opSce)
                elif gm.gameState == 1:
                    drawEnding(width,height,screen,gm,myfont)
    
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
<<<<<<< HEAD
    op = classOpenScene.OpenScene(width,height)
=======
    opSce = classOpenScene.OpenScene(width,height)
    gm.gameState = -1
>>>>>>> 5039ed1261ecaad475738703d0384ace26f87944
    #mole = classMoles.Moles()


    #role = int(input("0=Farmer; 1 = moles"))
    #mAI = True
    #fAI = True

<<<<<<< HEAD
    run(server, msgs_q, gm, width,height)
=======
    run(server, msgs_q, opSce, gm, width,height)
>>>>>>> 5039ed1261ecaad475738703d0384ace26f87944

if __name__ == '__main__':
    play()
