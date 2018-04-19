import classGameMap
import pygame
import os

def drawMap(screen,field, grass, gm):
    for tile in gm.map:
        if gm.map[tile] == 1:
            screen.blit(field, gm.indexToPos(tile))
        else:
            screen.blit(grass, gm.indexToPos(tile))

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


def testClassMap(width = 800, height = 600):
    gm = classGameMap.gameMap(width, height,8)
    gm.mapGenerater()
    print(gm.mapRepre())
    pygame.init()
    screen=pygame.display.set_mode([width,height])
    grass = pygame.image.load(os.path.join('Graphic', 'Grass.png'))
    grass = pygame.transform.scale(grass, (gm.tileSize,gm.tileSize))
    field = pygame.image.load(os.path.join('Graphic', 'Field.png'))
    field = pygame.transform.scale(field, (gm.tileSize,gm.tileSize))
    myfont = pygame.font.SysFont(gm.fontName, gm.fontSize)
    done = False
    while not done:
        screen.fill(gm.BGcolor)
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True
        # draw the generated map
        drawMap(screen, field, grass, gm)

        # draw UI elelments
        drawUI(width, height, screen, gm, myfont)

        pygame.display.flip()
    pygame.quit()  

testClassMap(600,600)
            