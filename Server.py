import socket, queue, threading
import classGameMap
import classMoles
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

# takes messages from message queue, sends to everyone except the sender
def server_thread(clientele, msg_q, gm):
    while True:
        # gets & formats a message
        ready_msg = msg_q.get() + '\n'
        msg_q.task_done()
        # gets the ID of sender from the message
        sender_ID = ready_msg.split("+")[0]
        update_ID = sender_ID
        #msgContent = ready_msg[ready_msg.index(' '):].strip().split(",")
        msgReceive = ready_msg.split("+")[1]
        if msgReceive.strip().startswith("update"):
            gm.time -= 1/len(clientele)
            if int(gm.time) == 0:
                gm.gameState = 1
                print("game End")
            success = gm.moles[sender_ID].countDown()
            gm.scoreM += success
            msgContent = gm.moles[sender_ID].__repr__()
            msgOut = "%s+%s\n"%(sender_ID, msgContent)
        else:
            strPos = msgReceive.split()
            pos = (int(strPos[0]), int(strPos[1]))
            role = int(strPos[2])
            if role == 1:
                gm.moles[sender_ID].spawnMoles(pos,gm)
                msgContent = gm.moles[sender_ID].__repr__()
            elif role == 0:
                for cID in gm.moles:
                    if gm.moles[cID].moleHit(pos,gm):
                        msgContent = gm.moles[cID].__repr__()
                        update_ID = cID
                        gm.scoreF += 1
                        break
                    else:
                        msgContent = gm.moles[sender_ID].__repr__()
            msgOut = "%s+%s\n"%(update_ID, msgContent)
        for client_ID in clientele:
            # sends to all
            clientele[client_ID].send(msgOut.encode())
            clientele[client_ID].send(("?%d,%d,%d,%d\n"%
                        (gm.gameState,gm.time,gm.scoreF,gm.scoreM)).encode())
        


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
    #mole = classMoles.Moles()

    
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #players = dict()
    threading.Thread(target=server_thread,
                     args=(clientele, msg_q, gm)).start()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    while True:

        (new_client_conn, address) = server.accept()
        # assigns unique ID
        new_client_ID = str(num_conns)
        num_conns += 1
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # generates random initial states
        #moleShow = random.randint(1,2)
        moleShow = 5
        moleNum = 2
        gm.moles[new_client_ID] = classMoles.Moles(moleShow,moleNum)
        reprMole = gm.moles[new_client_ID].__repr__()
        # constructs the initialization message to be sent to all
        newConnInit = '%s+%s\n ' % (new_client_ID, reprMole)
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
            initOld = '%s+%s\n' % (client_ID, gm.moles[client_ID].__repr__())
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
        # send init game state
        new_client_conn.send(("?%d,%d,%d,%d\n"%
                        (gm.gameState,gm.time,gm.scoreF,gm.scoreM)).encode())
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        threading.Thread(target=handle_client,
                         args=(new_client_conn, msg_q, new_client_ID,
                               clientele)).start()
    #reset server

if __name__ == '__main__':
    play()