import dearpygui.dearpygui as dpg
dpg.create_context()

import socket
import json
import time
import threading


def button_callback(sender, app_data, user_data):
    dpg.set_item_user_data(sender, [dpg.get_value(input_col), dpg.get_value(input_row)])
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")


s = socket.socket()  # Create a socket object

port = 420  # Define the port on which you want to connect

# something something
HEADERSIZE = 1024
host = '192.168.72.129'

placedShips = False

s.connect((host, port))  # connect to the server

row = 0
col = 0
dir = ""
listOfblock = []

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

def findPos(r, c):
    out = ((r - 1) * 9) + c - 1
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

def getBoard(prompt, sock):
    time.sleep(.25)
    board = sock.recv(HEADERSIZE)
    # print(board)
    try:
        board = json.loads(board)
    except:
        print("json failed to load")
    print("change GUI")
    # dpg.set_value(item=player_board, value=prompt)
    print(F"len of board = {len(board)}")
    # for i in range(len(board)):
    #     # print(listOfblock[i])
    #     if (board[i] == "O"):
    #         dpg.configure_item(item=listOfblock[i], color=[000, 000, 000], fill=[000, 255, 000])
    #     elif (board[i] == "X"):
    #         dpg.configure_item(item=listOfblock[i], color=[000, 000, 000], fill=[255, 100, 100])
    #     else:
    #         dpg.configure_item(item=listOfblock[i], color=[000, 000, 255], fill=[000, 000, 255])
    printBoard(board, id)

def network():
    print("got to network")
    global  placedShips, row, col, dir, btn, \
            constat, player_board, \
            input_col, input_row, \
            tableRow, tableCol
    while True:
        getBoard("your", s)

        if (placedShips == False):
            for a in range(2):  # place ships
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
            getBoard("other player", s)

            guess1 = safeInputrow("enter row")
            guess2 = safeInput("enter colum")

            moves = [guess1, guess2]
            s.send(bytes(json.dumps(moves), encoding="utf-8"))

            time.sleep(.25)
        placedShips = True

        win = json.loads(s.recv(HEADERSIZE))

        if (win == "T"):
            print("you win")
            time.sleep(20)
            break
        elif (win == "F"):
            print("you lost")
            time.sleep(20)
            break


# def main_window_setup():
#     global row, col, btn, listOfblock, \
#            dir, constat, \
#            player_board, \
#            input_col, input_row, \
#            tableRow, tableCol \
#
#
#     dpg.create_viewport(title="battleships", width=850, height=850)
#     dpg.set_viewport_max_height(850)
#     dpg.set_viewport_max_width(850)
#
#     with dpg.font_registry():
#         # first argument ids the path to the .ttf or .otf file
#         default_font = dpg.add_font("pixeldroidBoticRegular.otf", 20)
#         font_constat = dpg.add_font("pixeldroidBoticRegular.otf", 30)
#         board = dpg.add_font("pixeldroidBoticRegular.otf", 18)
#
#     with dpg.window(pos=[0, 0], no_collapse=True, no_resize=True, no_close=True, no_move=True, no_title_bar=True,
#                     label="background", width=850, height=850):
#         with dpg.group(horizontal=True):
#             # connection status text
#             constat = dpg.add_text(default_value="connection status: disconected", pos=[120, 20])
#             # binds font
#             dpg.bind_item_font(item=constat, font=font_constat)
#             player_board = dpg.add_text(default_value="your board", pos=[320, 45], label="player_board")
#             # binds font
#             dpg.bind_item_font(item=player_board, font=default_font)
#
#         with dpg.group(horizontal=True, pos=[-5, 70]):
#             with dpg.plot(no_menus=False, no_title=True, no_box_select=True,
#                           no_mouse_pos=True, width=400, height=400, equal_aspects=True):
#
#                 default_x = dpg.add_plot_axis(axis=0, no_gridlines=True, no_tick_marks=True, no_tick_labels=True,
#                                               label="", lock_min=True)
#                 dpg.set_axis_limits(axis=default_x, ymin=0, ymax=9)
#
#                 default_y = dpg.add_plot_axis(axis=1, no_gridlines=True, no_tick_marks=True, no_tick_labels=True,
#                                               label="", lock_min=True)
#                 dpg.set_axis_limits(axis=default_y, ymin=0, ymax=9)
#
#                 for i in range(9):
#                     for j in range(9):
#                          listOfblock.append(dpg.draw_rectangle(pmin=[j, i], pmax=[j + 1, i + 1], thickness=0,
#                                                    color=[0, 255-i*10, 0-i*10], fill=[0, 255-i*40, 0+j*40]))
#                 # listOfblock.reverse()
#
#         with dpg.group(horizontal=True, pos=[0, 370]):
#             tableRow = dpg.add_text(default_value="row")
#             dpg.bind_item_font(item=tableRow, font=default_font)
#             input_row = dpg.add_input_text(width=100)
#
#             tableCol = dpg.add_text(default_value="col")
#             dpg.bind_item_font(item=tableCol, font=default_font)
#             input_col = dpg.add_input_text(width=100)
#
#             # button that send the moves to the server
#             btn = dpg.add_button(label="subment move")
#             dpg.set_item_callback(btn, button_callback)
#
#     dpg.setup_dearpygui()
#     dpg.show_viewport()
#     dpg.start_dearpygui()
#     dpg.destroy_context()


def start():
    n = threading.Thread(target=network, args=())
    # w = threading.Thread(target=main_window_setup, args=(),)
    n.start()
    # w.start()


start()
