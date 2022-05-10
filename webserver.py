import socket
import json
import time
from threading import Lock
from _thread import *
import copy

lock = Lock()  # stop shit

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # object socket
host = 'localhost'
port = 420
HEADERSIZE = 2048
ThreadCount = 0

# bind the socket to the port
sock.bind((host, port))
print("socket bound to %s" % port)

sock.listen(5)  # starts listening for tcp. the number is the queue

rowSize = 9  # global var
numOfShips = 2



map = []  # legend X = hit * = miss . = unknowen :  O = ship
for _ in range(rowSize ** 2):
    map.append('.')

def findPos(row, col): # find pos on list from row and colum input
    out = ((row - 1) * rowSize) + col - 1
    print(f"pos from findpos is {out}")
    return out

class Player:
    board = []
    placedShips = False

    def __init__(self, board):
        self.board = board

class Game:  # game logic
    listOfPlayers = []
    win = [False, "", ""]

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
            # print("got to place ship")
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

def sendBoard(player, con):  # send board to client program
    con.send(bytes(json.dumps(player.board), encoding="utf-8"))

def sendOtherBoard(player, con):  # send board to client program and hides ships
    sendboard = copy.deepcopy(player.board)
    for i in range(len(sendboard)):
        if (sendboard[i] == "O"):
            sendboard[i] = "."
    con.send(bytes(json.dumps(sendboard), encoding="utf-8"))

# function that threads uses
def handleClient(con, game, player):
    while True:
        lock.acquire(blocking=True, timeout=- 1)
        difPlay = game.otherPlayer(player) # gets other player object

        con.send(bytes(json.dumps(True), encoding="utf-8"))

        # print(f" player id = {player}")
        time.sleep(.25)
        con.send(bytes(json.dumps(player.board), encoding="utf-8"))
        print(player.board)
        # player places ships
        if (player.placedShips == False):
            print(player.placedShips)
            for a in range(2):
                inlist = con.recv(HEADERSIZE)

                game.placeShip(inlist[0], inlist[1], player, inlist[3])
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

        time.sleep(1)

        # checks if won after first turn
        if (player.placedShips == True):
            game.checkWin(player, difPlay)
            if (game.win[0] == True): # sends messges to player if they won
                print("end game")
                if (game.win[1] == player):
                    con.send(bytes(json.dumps("T"), encoding="utf-8"))
                    lock.release()
                    break
                elif(game.win[2] == player):
                    con.send(bytes(json.dumps("F"), encoding="utf-8"))
                    lock.release()
                    break
            else:
                con.send(bytes(json.dumps("S"), encoding="utf-8")) # this is so the client doesn't break
        else:
            con.send(bytes(json.dumps("S"), encoding="utf-8")) # this is so the client doesn't break

        player.placedShips = True



        while ThreadCount == 1:
            time.sleep(1)
        lock.release()
        time.sleep(1)

while True: # main loop
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
        elif(ThreadCount > 2):
            break
        else:
            start_new_thread(handleClient, (Client, g1, listOfPlayer[1]))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))