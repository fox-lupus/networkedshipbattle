import socket
import json
import time
from threading import Lock
from _thread import *
import copy

# stop shit
lock = Lock()

# object socket
sock = socket.socket()
host = '127.0.0.1'
port = 4200
HEADERSIZE = 1024
ThreadCount = 0

# bind the socket to the port
i = True
while(i == True):
    time.sleep(1)
    try:
        sock.bind((host, port))
        print("socket binded to %s" % port)
        i = False
    except socket.error as e:
        print(str(e))

# starts listening for tcp. the number is the queue
sock.listen(5)

# gobal var
rowSize = 9
numOfShips = 2


# legend X = hit * = miss . = unknowen :  O = ship
map = []
for _ in range(rowSize ** 2):
    map.append('.')
# find pos on list from row and colum input
def findPos(row, col):
    out = ((row - 1) * rowSize) + col - 1
    print(out)
    return out

class Player:
    numOfPlayer = 0
    id = 0
    board = []
    placedShips = False


    def __init__(self, board):
        self.board = board
        self.numOfPlayer += 1
        self.id = self.numOfPlayer


# game logic
class Game:
    listOfPlayers = []

    def __init__(self, listOfPlayers):
        self.listOfPlayers = listOfPlayers

    def otherPlayer(self, player):
        for i in range(len(self.listOfPlayers)):
            if(self.listOfPlayers[i] == player):
                return self.listOfPlayers[i]

    def placeShip(self, row, col, player):
        if (player.board[findPos(row, col)] != 'O'):
            player.board[findPos(row, col)] = 'O'
        else:
            print("aready ship taken error")

    def shoot(self, row, col, player):
        if (player.board[findPos(row, col)] == 'O'):
            player.board[findPos(row, col)] = 'X'
        elif (player.board[findPos(row, col)] == '.'):
            player.board[findPos(row, col)] = '*'

print(map)

# send board to client program
def sendBoard(player, con):
    sendboard = json.dumps(player.board)
    con.send(bytes(sendboard, encoding="utf-8"))

# function that threads uses
def handleClient(con, game, player):
    while True:
        lock.acquire(blocking=True, timeout=- 1)
        difPlay = game.otherPlayer(player)

        sendBoard(difPlay, con)

        # player places ships
        if (player.placedShips == False):
            for _ in range(numOfShips):
                p1 = json.loads(con.recv(HEADERSIZE))
                p2 = json.loads(con.recv(HEADERSIZE))
                game.placeShip(int(p1), int(p2), player)
                sendBoard(difPlay, con)
            player.placedShips = True

        sendBoard(difPlay, con)

        m1 = json.loads(con.recv(HEADERSIZE))
        m2 = json.loads(con.recv(HEADERSIZE))

        g1.shoot(int(m1), int(m2), difPlay)

        sendBoard(difPlay, con)

        lock.release()
        time.sleep(1)

# main loop
while True:
    # creates game and players
    listOfPlayer = []
    for i in range(2):
        listOfPlayer.append(Player(copy.deepcopy(map)))
    g1 = Game(listOfPlayer)
    # loop to accept connections
    while True:
        Client, address = sock.accept()
        ThreadCount += 1
        print ('Got connection from', address)
        # puts connection on differnt threads with a differnt player args
        if (ThreadCount == 1):
            start_new_thread(handleClient, (Client, g1, listOfPlayer[0]))
        else:
            start_new_thread(handleClient, (Client, g1, listOfPlayer[1]))

        print('Thread Number: ' + str(ThreadCount))