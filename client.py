import socket
import json
import time

# Create a socket object
s = socket.socket()
  
# Define the port on which you want to connect
port = 4200

#something something
HEADERSIZE = 1024
  
# connect to the server on local computer
s.connect(('localhost', port))

gameboard = []

def printBoard(br, id):
    print(fr"""
    1   2   3   4   5   6   7   8   9
1 | {br[0]} | {br[1]} | {br[2]} | {br[3]} | {br[4]} | {br[5]} | {br[6]} | {br[7]} | {br[8]} |
2 | {br[9]} | {br[10]} | {br[11]} | {br[12]} | {br[13]} | {br[14]} | {br[15]} | {br[16]} | {br[17]} | {id} board
3 | {br[18]} | {br[19]} | {br[20]} | {br[21]} | {br[22]} | {br[23]} | {br[24]} | {br[25]} | {br[26]} |
4 | {br[27]} | {br[28]} | {br[29]} | {br[30]} | {br[31]} | {br[32]} | {br[33]} | {br[34]} | {br[35]} |
5 | {br[36]} | {br[37]} | {br[38]} | {br[39]} | {br[40]} | {br[41]} | {br[42]} | {br[43]} | {br[44]} |   /  N  \
6 | {br[45]} | {br[46]} | {br[47]} | {br[48]} | {br[49]} | {br[50]} | {br[51]} | {br[52]} | {br[53]} |  /   ^   \
7 | {br[54]} | {br[55]} | {br[56]} | {br[57]} | {br[58]} | {br[59]} | {br[60]} | {br[61]} | {br[62]} | W <  ✚  > E
8 | {br[63]} | {br[64]} | {br[65]} | {br[66]} | {br[67]} | {br[68]} | {br[69]} | {br[70]} | {br[71]} |  \   v   /
9 | {br[72]} | {br[73]} | {br[74]} | {br[75]} | {br[76]} | {br[77]} | {br[78]} | {br[79]} | {br[80]} |   \  S  /""")

placedShips = False

def findPos(row, col):
    out = ((row - 1) * 9) + col - 1
    return out

def safeInput(prompt):
    while True:
        try:
            res = int(input(prompt))
            if (res > -1 and res < 10):
                break
        except ValueError:
            print("enter Number")

    return res

def safeInputchar(prompt):
    while True:
            res = input(prompt)
            # print(f"res is {res}")
            if (ord(res) - 96 == 5 or ord(res) - 96 == 14):
                res = res.upper()
                return res
            print("enter N or E")
# def safePlaceShip(board):
#     while True:
#
#         print("placeship")
#         row = safeInput("enter row")
#         printBoard(board)
#         col = safeInput("enter colum")
#         printBoard(board)
#         dir = safeInputchar("enter cardinal direction")
#         dir = dir.upper()
#         printBoard(board)
#
#         row = json.dumps(row)
#         col = json.dumps(col)
#         dir = json.dumps(dir)
#
#         print(dir)
#         if (board[findPos(int(row), int(col))] != 'O'):
#             board[findPos(int(row), int(col))] = 'O'
#             if (dir == "N"):
#                 board[findPos(int(row) - 1, int(col))] = 'O'
#                 s.send(bytes(row, encoding="utf-8"))
#                 s.send(bytes(col, encoding="utf-8"))
#                 s.send(bytes(dir, encoding="utf-8"))
#                 break
#             elif (dir == "E"):
#                 board[findPos(int(row), int(col) + 1)] = 'O'
#                 s.send(bytes(row, encoding="utf-8"))
#                 s.send(bytes(col, encoding="utf-8"))
#                 s.send(bytes(dir, encoding="utf-8"))
#                 break

def getBoard(id, sd):
    board = sd.recv(HEADERSIZE)
    print(board)
    board = json.loads(board)

    printBoard(board, id)

dumblock = False

while True:

    while dumblock == False:
        dumblock = json.loads(s.recv(HEADERSIZE))

    getBoard("your", s)

    if (placedShips == False):
        for a in range(2):
            print("placeship")
            row = safeInput("enter row")
            col = safeInput("enter colum")
            dir = safeInputchar("enter cardinal direction")

            time.sleep(.01)
            s.send(bytes(json.dumps(row), encoding="utf-8"))

            time.sleep(.01)
            s.send(bytes(json.dumps(col), encoding="utf-8"))

            time.sleep(.01)
            s.send(bytes(json.dumps(dir), encoding="utf-8"))

            getBoard("your", s)
    else:
        getBoard("other player", s)

        guess = safeInput("enter row")
        s.send(bytes(json.dumps(guess), encoding="utf-8"))

        guess = safeInput("enter colum")
        s.send(bytes(json.dumps(guess), encoding="utf-8"))

        getBoard("other player", s)

    placedShips = True

    win = json.loads(s.recv(HEADERSIZE))

    if (win == "T"):
        print("you win")
        break
    elif(win == "F"):
        print("you lost")
        break

    dumblock = False