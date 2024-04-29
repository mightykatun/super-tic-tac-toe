import asyncio
import numpy as np
import pygame as pg
import pygame.freetype
import random as rd
import sys, os

pygame.init()
pygame.display.set_caption("Super Tic Tac Toe")
screen_state = pygame.display.Info()
screen_height = 3 * screen_state.current_h // 4
screen_width = 3 * screen_height // 2
screen = pygame.display.set_mode((screen_width, screen_height))

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#====== USER VAR ======
square_amount = 3
grid_line_width = 2
pad = 10

text_color = "black"
grid_color = "black"
frame_color = "darkgray"
bg_color = "gray"
highlight_color= "red"

#====== VAR COMP ======
font_path = resource_path("pixelmix_micro.ttf")

frame_size = screen_height - 4 * pad
frame_origin = pad * 2

grid_size = frame_size - 2 * (pad + grid_line_width)
grid_cell_size = (grid_size - (square_amount - 1) * grid_line_width) // square_amount
grid_origin = frame_origin + pad + grid_line_width

sub_grid_size = (grid_size - 2 * square_amount * pad - (square_amount - 1) * grid_line_width) // square_amount
sub_grid_cell_size = (sub_grid_size - (square_amount - 1) * (grid_line_width - 1)) // square_amount
sub_grid_origin = [grid_origin + pad + (sub_grid_size + 2 * pad + grid_line_width) * i for i in range(square_amount)]

radius = 2 * pad
text_size = sub_grid_cell_size * 2 // 3
board_font = pygame.freetype.Font(font_path, text_size)

x_origin_toplay_frame = frame_origin + pad + frame_size
toplay_frame_size = screen_width - x_origin_toplay_frame - 2 * pad
toplay_frame_height = frame_size // 4
toplay_text_size = toplay_frame_size // 5
toplay_font = pygame.freetype.Font(font_path, toplay_text_size)
toplay_cor = (x_origin_toplay_frame + toplay_text_size // 5,
              frame_origin + 5 * (toplay_frame_height - toplay_text_size) // 8)

win_text_size = grid_cell_size
win_font = pygame.freetype.Font(font_path, win_text_size)

game_matrix = np.zeros([square_amount]*4, dtype=int)
win_matrix = np.zeros([square_amount]*2, dtype=int)
collider = []

#====== FUNCTION ======
def draw_frame():
    pygame.draw.rect(screen, frame_color, (frame_origin, frame_origin, frame_size, frame_size), border_radius=radius, width=grid_line_width)
    pygame.draw.rect(screen, frame_color, (x_origin_toplay_frame, frame_origin, toplay_frame_size, toplay_frame_height), border_radius=radius, width=grid_line_width)

def draw_grid():
    global collider
    for i in range(1, square_amount):
        y_cor =  grid_origin + i * grid_cell_size
        pygame.draw.line(screen, grid_color, (grid_origin, y_cor), (grid_origin + grid_size, y_cor), width=grid_line_width)
        x_cor =  grid_origin + i * grid_cell_size
        pygame.draw.line(screen, grid_color, (x_cor, grid_origin), (x_cor, grid_origin + grid_size), width=grid_line_width)
    for a, i in enumerate(sub_grid_origin):
        for b, j in enumerate(sub_grid_origin):
            for k in range(1, square_amount):
                y_cor = j + k * sub_grid_cell_size
                pygame.draw.line(screen, grid_color, (i, y_cor), (i + sub_grid_size, y_cor), width=grid_line_width - 1)
                x_cor = i + k * sub_grid_cell_size
                pygame.draw.line(screen, grid_color, (x_cor, j), (x_cor, j + sub_grid_size), width=grid_line_width - 1)
            for c in range(square_amount):
                for d in range(square_amount):
                    content = game_matrix[a][b][c][d]
                    if content == 0 or content == 3:
                        content = ""
                    if content == 1:
                        content = "O"
                    if content == 2:
                        content = "X"
                    x_cor = i + (c + 1) * sub_grid_cell_size
                    y_cor = j + (d + 1) * sub_grid_cell_size
                    board_font.render_to(screen, (x_cor - text_size, y_cor - text_size), str(content), text_color)
                    button = pygame.Rect(x_cor - sub_grid_cell_size, y_cor - sub_grid_cell_size, sub_grid_cell_size, sub_grid_cell_size) 
                    collider.append([button, a, b, c, d])

def clickable(button, next_grid):
    square_clicked_val = game_matrix[button[1]][button[2]][button[3]][button[4]]
    if square_clicked_val == 0:
        if next_grid == None or next_grid[0] == button[1] and next_grid[1] == button[2]:
            return True

def highlight_next(next_grid):
    if next_grid != None:
        origin = [next_grid[0] * (grid_cell_size + grid_line_width) + grid_origin + pad // 2,
                  next_grid[1] * (grid_cell_size + grid_line_width) + grid_origin + pad // 2]
        size = grid_cell_size - pad
        pygame.draw.rect(screen, highlight_color, (origin[0], origin[1], size, size), border_radius=radius // 2, width=grid_line_width - 1)

def display_player(player_turn):
    if player_turn == 1:
        toplay_font.render_to(screen, toplay_cor, "TO PLAY: O", text_color)
    if player_turn == 2:
        toplay_font.render_to(screen, toplay_cor, "TO PLAY: X", text_color)

def win_overlay(win_player, button):
    if button != None:
        win_matrix[button[1]][button[2]] = win_player
        for i in range(square_amount):
            for j in range(square_amount):
                if win_matrix[i][j] != 0:
                    x_cor = grid_origin + i * (grid_cell_size + grid_line_width)
                    y_cor = grid_origin + j * (grid_cell_size + grid_line_width)
                    content = "X"
                    div = 5
                    if win_matrix[i][j] == 1:
                        content = "O"
                        div = 4
                    win_font.render_to(screen, (x_cor + win_text_size // div, y_cor + win_text_size // 6), content, text_color)
    
def next_grid_loc(button, win_player):
    next_grid = [button[3], button[4]]
    sum = 0
    for i in game_matrix[button[3]][button[4]]:
        for j in i:
            if j != 0:
                sum += 1
    if sum == square_amount**2:
        next_grid = None
    if win_player != 0:
        next_grid = None
        for i in range(square_amount):
            for j in range(square_amount):
                temp = game_matrix[button[1]][button[2]][i][j]
                if temp == 0:
                    game_matrix[button[1]][button[2]][i][j] = 3

    return next_grid

def is_win(button):
    win_player = 0
    sub_grid = game_matrix[button[1]][button[2]]
    player_played = sub_grid[button[3]][button[4]]
    for i in sub_grid:
        if(i == [player_played] * square_amount).all():
            win_player = player_played
    for i in sub_grid.transpose().copy():
        if (i == [player_played] * square_amount).all():
            win_player = player_played
    if (sub_grid.diagonal().copy() == [player_played] * square_amount).all():
        win_player = player_played
    if (np.fliplr(sub_grid).diagonal() == [player_played] * square_amount).all():
        win_player = player_played
    return win_player

def final_win(turns_played, is_playing):
    if is_playing == True:
        if turns_played == square_amount**4 or (win_matrix != 0).all():
            is_playing = False
        for i in range(1, 3):
            for j in win_matrix:
                if(j == [i] * square_amount).all():
                    is_playing = False
            for j in win_matrix.transpose().copy():
                if (j == [i] * square_amount).all():
                    is_playing = False
            if (win_matrix.diagonal().copy() == [i] * square_amount).all():
                is_playing = False
            if (np.fliplr(win_matrix).diagonal() == [i] * square_amount).all():
                is_playing = False
        return is_playing
        
async def main():
    button_exit = False
    is_playing = True
    next_grid = None
    last_pressed = None
    win_player = None
    player_turn = rd.randint(1, 2)
    turns_played = 0
    while is_playing:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_playing = False
                button_exit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in collider:
                    if button[0].collidepoint(pos):
                        if clickable(button, next_grid):
                            game_matrix[button[1]][button[2]][button[3]][button[4]] = player_turn
                            if player_turn == 1:
                                player_turn = 2
                            else:
                                player_turn = 1
                            turns_played += 1
                            win_player = is_win(button)
                            next_grid = next_grid_loc(button, win_player)
                            last_pressed = button
        
        screen.fill(bg_color)
        is_playing = final_win(turns_played, is_playing)
        highlight_next(next_grid)
        display_player(player_turn)             
        draw_frame()
        draw_grid()
        win_overlay(win_player, last_pressed)

        pg.display.update()
        await asyncio.sleep(0)

    if button_exit == False:
        is_playing = True     
        while is_playing:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    is_playing = False
            pygame.draw.rect(screen, bg_color, (x_origin_toplay_frame, frame_origin, toplay_frame_size, toplay_frame_height))
            pygame.draw.rect(screen, frame_color, (x_origin_toplay_frame, frame_origin, toplay_frame_size, toplay_frame_height), border_radius=radius, width=grid_line_width)
            if player_turn == 1:
                toplay_font.render_to(screen, toplay_cor, "X WINS !!", text_color)
            if player_turn == 2:
                toplay_font.render_to(screen, toplay_cor, "O WINS !!", text_color)
            pg.display.update()
            await asyncio.sleep(0)

    pg.quit()

asyncio.run(main())