import dearpygui.dearpygui as dpg

dpg.create_context()


def button_callback(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")


dpg.create_viewport(title="battleships", width=850, height=850)
dpg.set_viewport_max_height(850)
dpg.set_viewport_max_width(850)

with dpg.font_registry():
    # first argument ids the path to the .ttf or .otf file
    default_font = dpg.add_font("pixeldroidBoticRegular.otf", 20)
    font_constat = dpg.add_font("pixeldroidBoticRegular.otf", 30)
    board = dpg.add_font("pixeldroidBoticRegular.otf", 18)

with dpg.window(pos=[0, 0], no_collapse=True, no_resize=True, no_close=True, no_move=True, no_title_bar=True,
                label="background", width=850, height=850):
    with dpg.group(horizontal=True):
        # connection status text
        constat = dpg.add_text(default_value="connection status: disconected", pos=[120, 20])
        # binds font
        dpg.bind_item_font(item=constat, font=font_constat)
        player_board = dpg.add_text(default_value="your board", pos=[320, 45], label="player_board")
        # binds font
        dpg.bind_item_font(item=player_board, font=default_font)

    with dpg.group(horizontal=True, pos=[-5, 70]):
        with dpg.plot(no_menus=False, no_title=True, no_box_select=True,
                      no_mouse_pos=True, width=840, height=500, equal_aspects=True):

            default_x = dpg.add_plot_axis(axis=0, no_gridlines=True, no_tick_marks=True, no_tick_labels=True,
                                          label="", lock_min=True)
            dpg.set_axis_limits(axis=default_x, ymin=0, ymax=9)
            default_y = dpg.add_plot_axis(axis=1, no_gridlines=True, no_tick_marks=True, no_tick_labels=True,
                                          label="", lock_min=True)
            dpg.set_axis_limits(axis=default_y, ymin=0, ymax=9)

            # burrow = dpg.draw_rectangle(pmin=[0, 0], pmax=[50, 50], color=[33, 33, 33], fill=[33, 33, 33])
            #snake = dpg.draw_polyline(points=[[1.1,5.5,10.,20., 30.]], thickness=1, color=[0, 255, 0])
            # for i in range(9):
            #     for j in range(9):
            #         dpg.draw_rectangle(pmin=[j+1, j+1], pmax=[i-1, i-1], thickness=0, color=[0, 255-j*i*3, 0],
            #                            fill=[0, 255-j*i*3, 0])
            dpg.draw_rectangle(pmin=[1,  2], pmax=[2, 3], thickness=0, color=[0, 255, 0],
                               fill=[0, 255, 0])

        # with dpg.table(header_row=True, row_background=True, borders_innerH=True, borders_innerV=True,
        #                borders_outerV=True, width=840):
        #     # creates columns
        #     dpg.add_table_column()
        #     dpg.add_table_column(label="11")
        #     dpg.add_table_column(label="22")
        #     dpg.add_table_column(label="33")
        #     dpg.add_table_column(label="44")
        #     dpg.add_table_column(label="55")
        #     dpg.add_table_column(label="66")
        #     dpg.add_table_column(label="77")
        #     dpg.add_table_column(label="88")
        #     dpg.add_table_column(label="99")
        #
        #     count = 0 # this counts the number of rows made
        #
        #     for i in range(0, 9):
        #         with dpg.table_row():
        #             for j in range(0, 9):
        #                 if j == 0:
        #                     a = dpg.add_text(f"{chr(i+97).upper()}")
        #                     dpg.bind_item_font(item=a, font=board)
        #                 count += 1
        #                 print(F"table {count}")
        #                 dpg.add_text(default_value=f"{j}", label=F"{count}")
        #                 dpg.bind_item_font(item=F"{count}", font=board)

    with dpg.group(horizontal=True, pos=[0, 370]):
        tableRow = dpg.add_text(default_value="row")
        dpg.bind_item_font(item=tableRow, font=default_font)
        input_row = dpg.add_input_text(width=100)

        tableCol = dpg.add_text(default_value="col")
        dpg.bind_item_font(item=tableCol, font=default_font)
        input_col = dpg.add_input_text(width=100)

        # button that send the moves to the server
        btn = dpg.add_button(label="subment move")
        dpg.set_item_callback(btn, button_callback)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()