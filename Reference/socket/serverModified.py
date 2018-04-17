###################################
#       Socket Server Demo        #
#         by Rohan Varma          #
#      adapted by Kyle Chin       #
# further adapted by Matthew Kong #
###################################

import socket, queue, threading
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
            msg_q.put(('%s %s' % (client_ID, ready_msg)))

# takes messages from message queue, sends to everyone except the sender
def server_thread(clientele, msg_q, players):
    while True:
        # gets & formats a message
        ready_msg = msg_q.get() + '\n'
        msg_q.task_done()
        # gets the ID of sender from the message
        sender_ID = ready_msg.split()[0]
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        msgContent = ready_msg[ready_msg.index(' '):].strip()
        if msgContent == 'Up':
            players[sender_ID][1] -= 5
        elif msgContent == 'Down':
            players[sender_ID][1] += 5
        elif msgContent == 'Left':
            players[sender_ID][0] -= 5
        elif msgContent == 'Right':
            players[sender_ID][0] += 5
        elif msgContent == 'r':
            players[sender_ID][2] = 'red'
        elif msgContent == 'g':
            players[sender_ID][2] = 'green'
        elif msgContent == 'b':
            players[sender_ID][2] = 'blue'
        msgOut = '%s %d %d %s\n' % (sender_ID, players[sender_ID][0],
                                               players[sender_ID][1],
                                               players[sender_ID][2])
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        for client_ID in clientele:
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            # sends to all
            clientele[client_ID].send(msgOut.encode())
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def main():
    HOST = '' # put server IP here for multiple computers; '' for local demos
    PORT = 50003
    num_conns = 0

    clientele = dict()
    msg_q = queue.Queue()

    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen()
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # {str ID: [int cx, int cy, str color]}
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
        newCX = random.randrange(0, 800)
        newCY = random.randrange(0, 600)
        newC = '#%02x%02x%02x' % (random.randrange(0, 256),
                                  random.randrange(0, 256),
                                  random.randrange(0, 256))
        players[new_client_ID] = [newCX, newCY, newC]
        # constructs the initialization message to be sent to all
        newConnInit = '%s %d %d %s\n' % (new_client_ID, newCX, newCY, newC)
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
            initOld = '%s %d %d %s\n' % (client_ID, players[client_ID][0],
                                                    players[client_ID][1],
                                                    players[client_ID][2])
            new_client_conn.send(initOld.encode())
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        clientele[new_client_ID] = new_client_conn
        # informs the new connection of its unique ID
        ID_msg = 'myid %s\n' % new_client_ID
        new_client_conn.send(ID_msg.encode())
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # sends init message
        new_client_conn.send(newConnInit.encode())
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        threading.Thread(target=handle_client,
                         args=(new_client_conn, msg_q, new_client_ID,
                               clientele)).start()

if __name__ == '__main__':
    main()
