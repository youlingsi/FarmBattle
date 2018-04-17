import socket, queue, threading
import pygame
import classGameMap
import os

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

def runMoles(server, msgs_q, gm, width, height):
    pygame.init()
    screen=pygame.display.set_mode([width,height])
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    moleImage = pygame.image.load(os.path.join('Graphic', 'MoleUp.png'))
    moleImage = pygame.transform.scale(moleImage, (gm.tileSize,gm.tileSize))
    done = False
    clock = pygame.time.Clock()
    timer = 0


    while not done:
    
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(10)

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True
                pygame.quit()         
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if (pos[0] > 0 and pos[0] < gm.width
                    and pos[1] > 0 and pos[1] < gm.width):
                    timer = 0
                    server.send(("%d,%d\n"%pos).encode())

        timer += 1
        if timer % 12 == 0:
            server.send(("%d,%d\n"%(-gm.width,-gm.height)).encode())

        if not done:
            # Clear the screen and set the screen background
            screen.fill((0,255,0))

            if msgs_q.qsize() > 0:
                msg = msgs_q.get()
                msgs_q.task_done()
                if (msg.startswith('newconn') or
                    msg.startswith('existingconn') or
                    msg.startswith('myid')):
                    newID = msg.split()[1]
                    gm.moles[newID] = (-gm.width, -gm.height)
                else:
                    infoList = msg.split()
                    thatID = infoList[0]
                    x = int(infoList[1])
                    y = int(infoList[2])
                    gm.moles[thatID] = (x,y)

                for playerID in gm.moles:
                    x, y= gm.moles[playerID]
                    #pygame.draw.circle(screen, (255,0,0), [x,y], 20)
                    screen.blit(moleImage, [x,y])
                    textsurface = myfont.render(str(playerID), False, (0, 0, 0))
                    screen.blit(textsurface,(x,y))

    
                # Go ahead and update the screen with what we've drawn.
                # This MUST happen after all the other drawing commands.
                pygame.display.flip()
    
    # Be IDLE friendly
    pygame.quit()

def runFarmer(server, msgs_q, gm, width,height):
    pygame.init()
    screen=pygame.display.set_mode([width,height])
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    done = False
    clock = pygame.time.Clock()
    timer = 0

    while not done:
    
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(10)

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True
                pygame.quit()         
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if (pos[0] > 0 and pos[0] < gm.width
                    and pos[1] > 0 and pos[1] < gm.width):
                    for m in gm.moles:
                        if (pos[0] - m[0] <= gm.tileSize
                            and pos[1]-m[1] <= gm.tileSize):
                                server.send(("%d,%d\n"%(-gm.width, -gm.height)).encode())

#=========Need alteration=====================
        timer += 1
        if timer % 8 == 0:
            server.send(("%d,%d\n"%(-gm.width,-gm.height)).encode())

        if not done:
            # Clear the screen and set the screen background
            screen.fill((0,255,0))

            if msgs_q.qsize() > 0:
                msg = msgs_q.get()
                msgs_q.task_done()
                if (msg.startswith('newconn') or
                    msg.startswith('existingconn') or
                    msg.startswith('myid')):
                    newID = msg.split()[1]
                    gm.moles[newID] = (-gm.width, -gm.height)
                else:
                    infoList = msg.split()
                    thatID = infoList[0]
                    x = int(infoList[1])
                    y = int(infoList[2])
                    gm.moles[thatID] = (x,y)

                for playerID in gm.moles:
                    x, y= gm.moles[playerID]
                    pygame.draw.circle(screen, (255,0,0), [x,y], 20)
                    textsurface = myfont.render(str(playerID), False, (0, 0, 0))
                    screen.blit(textsurface,(x,y))

    
                # Go ahead and update the screen with what we've drawn.
                # This MUST happen after all the other drawing commands.
                pygame.display.flip()
    pygame.quit()
#=============Need alteration=================================




def play(width = 800, height = 600):

    HOST = ''
    PORT = 50003

    msgs_q = queue.Queue()

    server = socket.socket()
    server.connect((HOST, PORT))

    threading.Thread(target=handle_server_msgs, args=(server, msgs_q)).start()

    gm = classGameMap.gameMap(width,height)

    runMoles(server, msgs_q, gm, width,height)
    runFarmer(server, msgs_q, gm, width,height)

if __name__ == '__main__':
    play()
