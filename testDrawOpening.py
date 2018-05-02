import classOpenScene
import classGameMap
import pygame
import os

height = 600
width = 800

opSce = classOpenScene.OpenScene(width, height)
pygame.init()
screen=pygame.display.set_mode([width,height])


moleImage = pygame.image.load(os.path.join('Graphic', 'MoleUp.png'))
moleImage = pygame.transform.scale(moleImage, (64,64))
gamestate = -1

# Check if the player clicked on the UI elements
def clickCheck(surf, surPos, pos):
    rec = surf.get_rect()
    rec = rec.move(surPos)
    print("Collide", rec.collidepoint(pos))
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
    elif opSce.selectionStage >= 1:
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


def testMain(screen,opSce,mole, farmer, gamestate):
    gameOn =True
    constructOpening(screen,opSce,mole,farmer)
    while gameOn:
        #drawOpening(screen,op,gamestate,moleImage,moleImage)
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                gamestate = 1
                gameOn = False
            else:
                """
                if gm.gameState == 0:       
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = gm.convertPOS(pygame.mouse.get_pos())
                        if (pos[0] > 0 and pos[0] < gm.width
                            and pos[1] > 0 and pos[1] < gm.width):
                            server.send(("%d %d %d %s\n"%(pos[0], pos[1],gm.playerRole,"Pl")).encode())
                """
                if gamestate == -1:
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            if opSce.selectionStage == 0:
                                opSce.playerRole = (opSce.playerRole + 1)%2
                            elif opSce.selectionStage == 1:
                                opSce.fAIon = not opSce.fAIon
                            elif opSce.selectionStage == 2:
                                opSce.mAIon = not opSce.mAIon
                        if event.key == pygame.K_RETURN:
                            if opSce.selectionStage == 2:
                                gamestate += 1
                                opSce.selectionStage = 0
                            else:
                                opSce.selectionStage += 1
                        elif event.key == pygame.K_ESCAPE and opSce.selectionStage > 0:
                            opSce.selectionStage -= 1
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        print("Stage", opSce.selectionStage)
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
                                gamestate +=1
                            elif clickCheck(opSce.allElement["sMAIOff"],opSce.allElement["sMAIOffPos"],mousePos):
                                opSce.mAIon = False
                                gamestate +=1
                        elif opSce.selectionStage == 1:
                            if clickCheck(opSce.allElement["sFAIOn"],opSce.allElement["sFAIOnPos"],mousePos):
                                opSce.fAIon = True
                                opSce.selectionStage +=1
                            elif clickCheck(opSce.allElement["sFAIOff"],opSce.allElement["sFAIOffPos"],mousePos):
                                opSce.fAIon = False
                                opSce.selectionStage +=1
                                                           
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                        if opSce.selectionStage > 0:
                            opSce.selectionStage -=1
                            


        if gamestate == -1:
            drawOpening(screen,opSce)
        pygame.display.flip()
    pygame.quit()
    
testMain(screen,opSce,moleImage,moleImage,gamestate)


    





