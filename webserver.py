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
    print(f"pos from findpos is {out}")
    return out

class Player:
    board = []
    placedShips = False

    def __init__(self, board):
        self.board = board



# game logic
class Game:
    listOfPlayers = []
    win = [False, "a", "a"]

    def __init__(self, listOfPlayers):
        self.listOfPlayers = listOfPlayers

    def checkWin(self, player, difplayer):
        if (difplayer.board.count("O") < 1):
            self.win[0] = True
            self.win[1] = player
            self.win[2] = difplayer

    def otherPlayer(self, player):
        for i in range(len(self.listOfPlayers)):
            if(self.listOfPlayers[i] != player):
                return self.listOfPlayers[i]

    def placeShip(self, row, col, player, dir):
        if (player.board[findPos(row, col)] != 'O'):
            player.board[findPos(row, col)] = 'O'
            print("got to place ship")
            if (dir == "N"):
                player.board[findPos(row - 1, col)] = 'O'
            elif (dir == "E"):
                player.board[findPos(row, col + 1)] = 'O'
        else:
            print("aready ship taken error")

    def shoot(self, row, col, player):
        if (player.board[findPos(row, col)] == 'O'):
            player.board[findPos(row, col)] = 'X'
        elif (player.board[findPos(row, col)] == '.'):
            player.board[findPos(row, col)] = '*'

# send board to client program
def sendBoard(player, con):
    con.send(bytes(json.dumps(player.board), encoding="utf-8"))

def sendOtherBoard(player, con):
    sendboard = copy.deepcopy(player.board)
    for i in range(len(sendboard)):
        if (sendboard[i] == "O"):
            sendboard[i] = "."
    con.send(bytes(json.dumps(sendboard), encoding="utf-8"))

# function that threads uses
def handleClient(con, game, player):
    while True:
        lock.acquire(blocking=True, timeout=- 1)
        # gets other player object
        difPlay = game.otherPlayer(player)

        con.send(bytes(json.dumps(True), encoding="utf-8"))

        # print(f" player id = {player}")

        con.send(bytes(json.dumps(player.board), encoding="utf-8"))
        print(player.board)
        # player places ships
        if (player.placedShips == False):
            print(player.placedShips)
            for a in range(2):
                # print("start")
                p1 = con.recv(HEADERSIZE)
                # print("got row")
                p2 = con.recv(HEADERSIZE)
                # print("got col")
                direct = con.recv(HEADERSIZE)
                # print("got dir")

                game.placeShip(json.loads(p1), json.loads(p2), player, json.loads(direct))
                con.send(bytes(json.dumps(player.board), encoding="utf-8"))
                # print("one loop")
        else:
            sendOtherBoard(difPlay, con)

            m1 = json.loads(con.recv(HEADERSIZE))
            m2 = json.loads(con.recv(HEADERSIZE))

            g1.shoot(int(m1), int(m2), difPlay)

            sendOtherBoard(difPlay, con)
        # print(difPlay)
        # print(player)

        # checks if won after first turn
        if (player.placedShips == True):
            game.checkWin(player, difPlay)
            # sends messges to player if they won
            if (game.win[0] == True):
                print("end game")
                if (game.win[1] == player):
                    con.send(bytes(json.dumps(True), encoding="utf-8"))
                    lock.release()
                    break
                elif(game.win[2] == player):
                    con.send(bytes(json.dumps(False), encoding="utf-8"))
                    lock.release()
                    break
        #     else:
        #
        #         # this is so the client doesn't break
        #         con.send(bytes(json.dumps(), encoding="utf-8"))
        # else:
        #     # this is so the client doesn't break
        #     con.send(bytes(json.dumps(), encoding="utf-8"))

        player.placedShips = True



        while ThreadCount == 1:
            time.sleep(1)
        lock.release()
        time.sleep(1)

# main loop
while True:
    # creates game and players
    listOfPlayer = []
    listOfPlayer.append(Player(copy.deepcopy(map)))
    listOfPlayer.append(Player(copy.deepcopy(map)))
    print(listOfPlayer)
    g1 = Game(listOfPlayer)
    # loop to accept connections
    while True:
        Client, address = sock.accept()

        print ('Got connection from', address)
        # puts connection on differnt threads with a differnt player args
        if (ThreadCount == 0):
            start_new_thread(handleClient, (Client, g1, listOfPlayer[0]))
        else:
            start_new_thread(handleClient, (Client, g1, listOfPlayer[1]))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))