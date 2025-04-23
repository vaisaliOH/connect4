import numpy as np
import pygame
import sys

# Game setup
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

pygame.init()
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("monospace", 75)

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Horizontal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all([board[r][c+i] == piece for i in range(4)]):
                return True
    # Vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all([board[r+i][c] == piece for i in range(4)]):
                return True
    # Diagonal /
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all([board[r+i][c+i] == piece for i in range(4)]):
                return True
    # Diagonal \
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all([board[r-i][c+i] == piece for i in range(4)]):
                return True
    return False

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, (r+1)*SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int((r+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):        
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int((r+0.5)*SQUARESIZE)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height - int((r+0.5)*SQUARESIZE)), RADIUS)
    pygame.display.update()

board = create_board()
game_over = False
turn = 0

draw_board(board)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            color = RED if turn == 0 else YELLOW
            pygame.draw.circle(screen, color, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            col = int(posx / SQUARESIZE)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                piece = 1 if turn == 0 else 2
                drop_piece(board, row, col, piece)

                if winning_move(board, piece):
                    label = font.render(f"Player {turn+1} wins!", 1, RED if piece == 1 else YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                draw_board(board)
                turn += 1
                turn %= 2

            if game_over:
                pygame.time.wait(3000)
