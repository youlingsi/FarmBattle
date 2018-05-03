import socket, queue, threading
import classGameMap
import classMoles
import ClassFarmer
import random



# receives messages from clients, puts into message queue
def handle_client(client_conn, msg_q, client_ID, clientele, bufsize=16):
    client_conn.setblocking(True)
    msg_stream = ''
    while True:
        # receives some bytes, decodes, adds onto message stream
        msg_stream += client_conn.recv(bufsize).decode()
        # while there are complete messages
        while '\n' in msg_stream:
            # gets one complete message
            newline_index = msg_stream.index('\n')
            ready_msg = msg_stream[:newline_index]
            # removes this complete message from stream
            msg_stream = msg_stream[newline_index + 1 :]
            # puts this complete message into queue
            msg_put = ('%s+%s\n' % (client_ID, ready_msg))
            msg_q.put(msg_put)



###################################
###### Game AIs ###################
##AI of the moles. spawn a mole 
def moleAI(gm):
    toSpawn = random.randint(0,1)
    if toSpawn:
        x = random.randint(gm.origin[0],gm.width-gm.origin[0])
        y = random.randint(gm.origin[1],gm.height-gm.origin[1])
        pos = gm.convertPOS((x,y))
        return pos
    else:
        return None

## AI of the Farmer
def farmerAI(gm):
    toCapture = random.randint(0,10)
    if toCapture <= 5:
        keyList = list(gm.moles.keys())
        i = random.randint(0,len(keyList)-1)
        try:
            mPos = gm.moles[keyList[i]][1]
            pos = mPos[random.randint(0,len(mPos)-1)]
            return pos
        except:
            pass
    else:
        x = random.randint(gm.origin[0],gm.width-gm.origin[0])
        y = random.randint(gm.origin[1],gm.height-gm.origin[1])
        pos = gm.convertPOS((x,y))
        return pos  

# check if AI is on:
def aiCheck(players, gm):
    playerSum=0
    mAIonSum = 0
    fAIonSum = 0
    for p in players:
        playerSum+=players[p][0]
        mAIonSum += players[p][1]
        fAIonSum += players[p][2]
    if playerSum == 0:
        gm.mAIOn = True
    elif playerSum == len(players):
        gm.fAIOn = True
    else:
        if mAIonSum != 0:
            gm.mAIOn = True
        else:
            gm.mAIOn = False
        if fAIonSum != 0:
            gm.fAIOn = True
        else:
            gm.fAIOn = False  
        
# takes messages from message queue, sends to everyone except the sender
def server_thread(clientele, msg_q, gm, players):
    while True:
        # gets & formats a message
        ready_msg = msg_q.get() + '\n'
        msg_q.task_done()
        # gets the ID of sender from the message
        sender_ID = ready_msg.split("+")[0]
        update_ID = sender_ID
        #msgContent = ready_msg[ready_msg.index(' '):].strip().split(",")
        msgReceive = ready_msg.split("+")[1]
        # manipulate the message
        msgOut = ""
        msgStateUpdate = ""
        msgContent = ""
        msgFarmer = ""
        msgColision = ""
        msgmAI = ""
        msgfAI = ""
        msgAICollision = ""
        if gm.gameState == -1:
            if msgReceive.strip().startswith("ready"):
                msg = msgReceive.strip().split(",")
                players[sender_ID] = [int(msg[1]), int(msg[2]),int(msg[3])]
            elif msgReceive.strip().startswith("update"):
                if len(players) > 0:
                    gm.loading -= 1/6/len(clientele)
                    print(gm.loading)
                    if gm.loading <= 0:
                        aiCheck(players,gm)
                        gm.gameState = 0
        elif gm.gameState == 0:
            if msgReceive.strip().startswith("update"):
                gm.time -= 1/3/len(clientele)
                print(gm.time)
                if int(gm.time) == 0:
                    gm.gameState = 1
                success = gm.moles[sender_ID].countDown()
                gm.scoreM += success
                msgContent = gm.moles[sender_ID].__repr__()
                gm.farmers[sender_ID].moveFarmer()
                msgFarmer = gm.farmers[sender_ID].encodeFarmer()
                msgOut = "%s+%s+%s\n"%(sender_ID, msgContent,msgFarmer)                                     
                # check collision
                for cID in gm.moles:
                    if gm.moles[cID].moleHit(gm.farmers[sender_ID].pos,gm):
                        msg = gm.moles[cID].__repr__()
                        update_ID = cID
                        gm.scoreF += 1
                        msgColision="%s+%s+%s\n"%(update_ID,msg,"")
                        break
                ## do AI
                if gm.mAIOn:
                    print("moleSpawn")
                    mPos = moleAI(gm)
                    if mPos!= None:
                        gm.moles["AI"].spawnMoles(mPos,gm)
                    success = gm.moles["AI"].countDown()
                    gm.scoreM += success
                    msgmAI = gm.moles["AI"].__repr__()
                if gm.fAIOn:
                    # send farmer to the position
                    fAIpos= farmerAI(gm)
                    print("farmer", fAIpos)
                    if fAIpos != None:
                        if gm.farmers["AI"].pos == (-100, -100):
                            gm.farmers["AI"].pos = gm.convertPOS(fAIpos)
                        else:
                            if gm.farmers["AI"].target == (-100, -100):
                                gm.farmers["AI"].target = gm.convertPOS(fAIpos)
                                gm.farmers["AI"].getRoute(gm)
                    gm.farmers["AI"].moveFarmer()
                    for cID in gm.moles:
                        if gm.moles[cID].moleHit(gm.farmers["AI"].pos,gm):
                            msg = gm.moles[cID].__repr__()
                            update_ID = cID
                            gm.scoreF += 1
                            msgAICollision ="%s+%s+%s\n"%(update_ID,msg,"")
                            break
                    msgfAI = gm.farmers["AI"].encodeFarmer()

            else:
                strPos = msgReceive.split()
                pos = (int(strPos[0]), int(strPos[1]))
                role = int(strPos[2])
                if role == 1:
                    gm.moles[sender_ID].spawnMoles(pos,gm)
                    msgContent = gm.moles[sender_ID].__repr__()
                elif role == 0:
                    # send farmer to the position
                    if gm.farmers[sender_ID].pos == (-100, -100):
                        gm.farmers[sender_ID].pos = gm.convertPOS(pos)
                        msgFarmer = gm.farmers[sender_ID].encodeFarmer()
                    else:
                        if gm.farmers[sender_ID].target == (-100, -100):
                            gm.farmers[sender_ID].target = gm.convertPOS(pos)
                            gm.farmers[sender_ID].getRoute(gm)
                        gm.farmers[sender_ID].moveFarmer()
                        msgFarmer = gm.farmers[sender_ID].encodeFarmer()

                        print("Farmer", msgFarmer)   
                    msgOut = "%s+%s+%s\n"%(sender_ID, msgContent,msgFarmer)
        # send out the messages
        for client_ID in clientele:
            # sends to all
            msgStateUpdate = "?%d,%d,%d,%d\n"%(gm.gameState,gm.time,gm.scoreF,gm.scoreM)
            msgAI = "%s+%s+%s\n"%("AI", msgmAI,msgfAI)
            clientele[client_ID].send(msgOut.encode())
            clientele[client_ID].send(msgStateUpdate.encode())
            clientele[client_ID].send(msgColision.encode())
            clientele[client_ID].send(msgAI.encode())
            clientele[client_ID].send(msgAICollision.encode())


   


def play(width = 800, height = 600):
## from modified socket template
    # set up baseic server info
    HOST = '' # put server IP here for multiple computers; '' for local demos
    PORT = 50003
    num_conns = 0 # number of connection

    clientele = dict()
    msg_q = queue.Queue() #que of message received

    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen()
    timer = 0

    #initiate the map
    gm = classGameMap.gameMap(width, height)
    gm.mapGenerater()
    players = {}
    gm.farmers["AI"] = ClassFarmer.Farmer()
    gm.moles["AI"] = classMoles.Moles(30, 4)

    
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    threading.Thread(target=server_thread,
                     args=(clientele, msg_q, gm, players)).start()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    while True:
        (new_client_conn, address) = server.accept()
        # assigns unique ID
        new_client_ID = str(num_conns)
        num_conns += 1
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # generates random initial states
        #moleShow = random.randint(1,2)
        moleShow = 30
        moleNum = 3
        gm.moles[new_client_ID] = classMoles.Moles(moleShow,moleNum)
        reprMole = gm.moles[new_client_ID].__repr__()
        gm.farmers[new_client_ID] = ClassFarmer.Farmer()
        reprFarmer = gm.farmers[new_client_ID].encodeFarmer()
        # constructs the initialization message to be sent to all
        newConnInit = '%s+%s+%s\n ' % (new_client_ID, reprMole,reprFarmer)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # constructs the message to be sent to all existing connections
        new_conn_msg = 'newconn %s\n' % new_client_ID
        for client_ID in clientele:
            clientele[client_ID].send(new_conn_msg.encode())
            # constructs the message to be sent to the new connection
            existing_conn_msg = 'existingconn %s\n' % client_ID
            new_client_conn.send(existing_conn_msg.encode())
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            # sends init message
            #clientele[client_ID].send(newConnInit.encode())
            initOld = '%s+%s+%s\n' % (client_ID, gm.moles[client_ID].__repr__(),
                                        gm.farmers[client_ID].encodeFarmer())
            new_client_conn.send(initOld.encode())
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        clientele[new_client_ID] = new_client_conn
        # informs the new connection of its unique ID
        ID_msg = 'myid %s\n' % new_client_ID
        new_client_conn.send(ID_msg.encode())
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # sends init message
        new_client_conn.send(newConnInit.encode())
        # sends init map
        new_client_conn.send(("!%s\n" % gm.mapRepre()).encode())
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        threading.Thread(target=handle_client,
                         args=(new_client_conn, msg_q, new_client_ID,
                               clientele)).start()
    #reset server

if __name__ == '__main__':
    play()