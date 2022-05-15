import socket
import json
import time
# import dearpygui.dearpygui as dpg

# GUI nonsense
# dpg.create_context()
# dpg.create_viewport(title='Custom Title', width=600, height=300)
#
# with dpg.window(label="Example Window"):
#     dpg.add_text("Hello, world")
#     dpg.add_button(label="Save")
#     dpg.add_input_text(label="string", default_value="Quick brown fox")
#     dpg.add_slider_float(label="float", default_value=0.273, max_value=1)
#
# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()

s = socket.socket() # Create a socket object

port = 420 # Define the port on which you want to connect

#something something
HEADERSIZE = 1024
host = 'localhost'

s.connect((host, port)) # connect to the server

def printBoard(br, id):
    print(fr"""
    1   2   3   4   5   6   7   8   9
A | {br[0]} | {br[1]} | {br[2]} | {br[3]} | {br[4]} | {br[5]} | {br[6]} | {br[7]} | {br[8]} |
B | {br[9]} | {br[10]} | {br[11]} | {br[12]} | {br[13]} | {br[14]} | {br[15]} | {br[16]} | {br[17]} | {id} board
C | {br[18]} | {br[19]} | {br[20]} | {br[21]} | {br[22]} | {br[23]} | {br[24]} | {br[25]} | {br[26]} |
D | {br[27]} | {br[28]} | {br[29]} | {br[30]} | {br[31]} | {br[32]} | {br[33]} | {br[34]} | {br[35]} |
E | {br[36]} | {br[37]} | {br[38]} | {br[39]} | {br[40]} | {br[41]} | {br[42]} | {br[43]} | {br[44]} |   /  N  \
F | {br[45]} | {br[46]} | {br[47]} | {br[48]} | {br[49]} | {br[50]} | {br[51]} | {br[52]} | {br[53]} |  /   ^   \
G | {br[54]} | {br[55]} | {br[56]} | {br[57]} | {br[58]} | {br[59]} | {br[60]} | {br[61]} | {br[62]} | W <  ✚  > E
H | {br[63]} | {br[64]} | {br[65]} | {br[66]} | {br[67]} | {br[68]} | {br[69]} | {br[70]} | {br[71]} |  \   v   /
I | {br[72]} | {br[73]} | {br[74]} | {br[75]} | {br[76]} | {br[77]} | {br[78]} | {br[79]} | {br[80]} |   \  S  /""")

placedShips = False
gameboard = []
dumblock = False

def findPos(row, col):
    out = ((row - 1) * 9) + col - 1
    return out

def safeInput(prompt): # gets input from user and doesn't crash and only accept correct input
    while True:
        try:
            res = int(input(prompt))
            if (res > -1 and res < 10):
                break
        except ValueError:
            print("enter Number")

    return res

def safeInputrow(prompt): # gets input from user and doesn't crash and only accept correct input
    while True:
        try:
            res = input(prompt)
            try:
                out = ord(res) - 96
            except:
                print("only one char")
                out = 10
            if (out >= 1 and out <= 9):
                break
        except ValueError:
            print("lower case letter")
    return out

def safeInputchar(prompt): # like safeinput but with char
    while True:
            res = input(prompt)
            # print(f"res is {res}")
            if (ord(res) - 96 == 5 or ord(res) - 96 == 14):
                res = res.upper()
                return res
            print("enter N or E")

def getBoard(id, sd):
    time.sleep(.25)
    board = sd.recv(HEADERSIZE)
    print(board)
    try:
        board = json.loads(board)
    except:
        print("json failed to load")
    printBoard(board, id)

while True:

    # while dumblock == False: # makes sure that the client are syncs
    #     time.sleep(1)
    #     print("waiting for other player")
    #     try:
    #         out = s.recv(HEADERSIZE)
    #     except:
    #         print("failed")
    #     print(out)
    #     dumblock = json.loads(out)

    getBoard("your", s)

    if (placedShips == False):
        for a in range(2): # place ships
            print("placeship")
            row = safeInputrow("enter row")
            col = safeInput("enter colum")
            dir = safeInputchar("enter cardinal direction")

            outlist = [row, col, dir]

            s.send(bytes(json.dumps(outlist), encoding="utf-8"))
            time.sleep(.25)
            getBoard("your", s)
    else:
        time.sleep(.25)
        getBoard("other player", s) # shoot other player board

        guess1 = safeInputrow("enter row")
        guess2 = safeInput("enter colum")

        moves = [guess1, guess2]
        s.send(bytes(json.dumps(moves), encoding="utf-8"))

        time.sleep(.25)

    placedShips = True

    win = json.loads(s.recv(HEADERSIZE))

    if (win == "T"): # checks if you won the game
        print("you win")
        time.sleep(20)
        break
    elif(win == "F"):
        print("you lost")
        time.sleep(20)
        break

    # dumblock = False