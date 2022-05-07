import socket
import pickle
import json

# Create a socket object
s = socket.socket()
  
# Define the port on which you want to connect
port = 4200

#something something
HEADERSIZE = 1024
  
# connect to the server on local computer
s.connect(('localhost', port))

gameboard = []

def printBoard(br):
    print(fr"""
    1   2   3   4   5   6   7   8   9
1 | {br[0]} | {br[1]} | {br[2]} | {br[3]} | {br[4]} | {br[5]} | {br[6]} | {br[7]} | {br[8]} |
2 | {br[9]} | {br[10]} | {br[11]} | {br[12]} | {br[13]} | {br[14]} | {br[15]} | {br[16]} | {br[17]} |
3 | {br[18]} | {br[19]} | {br[20]} | {br[21]} | {br[22]} | {br[23]} | {br[24]} | {br[25]} | {br[26]} |
4 | {br[27]} | {br[28]} | {br[29]} | {br[30]} | {br[31]} | {br[32]} | {br[33]} | {br[34]} | {br[35]} |
5 | {br[36]} | {br[37]} | {br[38]} | {br[39]} | {br[40]} | {br[41]} | {br[42]} | {br[43]} | {br[44]} |   /  N  \
6 | {br[45]} | {br[46]} | {br[47]} | {br[48]} | {br[49]} | {br[50]} | {br[51]} | {br[52]} | {br[53]} |  /   ^   \
7 | {br[54]} | {br[55]} | {br[56]} | {br[57]} | {br[58]} | {br[59]} | {br[60]} | {br[61]} | {br[62]} | W <  ✚  > E
8 | {br[63]} | {br[64]} | {br[65]} | {br[66]} | {br[67]} | {br[68]} | {br[69]} | {br[70]} | {br[71]} |  \   v   /
9 | {br[72]} | {br[73]} | {br[74]} | {br[75]} | {br[76]} | {br[77]} | {br[78]} | {br[79]} | {br[80]} |   \  S  /""")

placedShips = False

def safeinput(prompt):
    while True:
        try:
            res = int(input(prompt))
            if (res > -1 and res < 81):
                break
        except ValueError:
            print("enter Number")

    return res

while True:
    msg = s.recv(HEADERSIZE)
    printBoard(json.loads(msg))
    print(msg)

    if (placedShips == False):
        for i in range(2):
            print("placeship")
            pos = input("enter row")
            pos = json.dumps(pos)
            s.send(bytes(pos, encoding="utf-8"))
            pos = input("enter colum")
            pos = json.dumps(pos)
            s.send(bytes(pos, encoding="utf-8"))
            msg = s.recv(HEADERSIZE)
            printBoard(json.loads(msg))
        placedShips = True

    msg = s.recv(HEADERSIZE)
    printBoard(json.loads(msg))

    guess = safeinput("enter row")
    guess = json.dumps(guess)

    s.send(bytes(guess,encoding="utf-8"))

    guess = safeinput("enter colum")
    guess = json.dumps(guess)

    s.send(bytes(guess, encoding="utf-8"))

    msg = s.recv(HEADERSIZE)
    printBoard(json.loads(msg))