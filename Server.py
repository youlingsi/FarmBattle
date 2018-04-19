import socket, queue, threading
import classGameMap



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
            msg_put = ('%s %s' % (client_ID, ready_msg))
            msg_q.put(msg_put)

# takes messages from message queue, sends to everyone except the sender
def server_thread(clientele, msg_q, players):
    while True:
        # gets & formats a message
        ready_msg = msg_q.get() + '\n'
        msg_q.task_done()
        # gets the ID of sender from the message
        sender_ID = ready_msg.split()[0]
        msgContent = ready_msg[ready_msg.index(' '):].strip().split(",")
        sender_ID = ready_msg.split()[0]
        msgOut = '%s %d %d \n' % (sender_ID, int(msgContent[0]),
                                             int(msgContent[1]),)
        for client_ID in clientele:
            # sends to all
            clientele[client_ID].send(msgOut.encode())
        


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

    #initiate the map
    gm = classGameMap.gameMap(width, height)
    gm.mapGenerater()
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # {str ID: [float x, float y]}
    players = dict()
    threading.Thread(target=server_thread,
                     args=(clientele, msg_q, players)).start()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    while True:
        (new_client_conn, address) = server.accept()
        # assigns unique ID
        new_client_ID = str(num_conns)
        num_conns += 1
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # generates random initial states
        newCX = -width
        newCY = -height
        players[new_client_ID] = [newCX, newCY]
        # constructs the initialization message to be sent to all
        newConnInit = '%s %d %d \n ' % (new_client_ID, newCX, newCY)
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
            clientele[client_ID].send(newConnInit.encode())
            initOld = '%s %d %d\n' % (client_ID, players[client_ID][0],
                                                    players[client_ID][1])
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

if __name__ == '__main__':
    play()