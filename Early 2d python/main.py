import pygame
import sys
import os

# initialise pygame
pygame.init()

# window size
WIDTH, HEIGHT = 800, 850
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Real-Time Chess")

# woard settings
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)

# colours
TEXT_COLOR = (255, 255, 255)
BOX_COLOR = (50, 50, 50)

# Font
FONT = pygame.font.SysFont("Arial", 32)

# load piece images
piece_images = {}
for piece in "prnbqkPRNBQK":
    path = os.path.join("pieces", f"{'w' if piece.isupper() else 'b'}{piece.upper()}.png")
    if os.path.exists(path):
        piece_images[piece] = pygame.transform.scale(pygame.image.load(path), (SQUARE_SIZE, SQUARE_SIZE))
    else:
        print(f"Warning: Missing image for {piece}")
        piece_images[piece] = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))  

# piece class
class Piece:
    def __init__(self, piece, row, col):
        self.piece = piece
        self.row = row
        self.col = col
        self.is_white = piece.isupper()

    def draw(self, window):
        if self.piece in piece_images:
            window.blit(piece_images[self.piece], (self.col * SQUARE_SIZE, self.row * SQUARE_SIZE))

# init pieces
pieces = {(row, col): Piece(piece, row, col) for piece, row, col in [
    # White
    ("R", 0, 0), ("N", 0, 1), ("B", 0, 2), ("Q", 0, 3), ("K", 0, 4), ("B", 0, 5), ("N", 0, 6), ("R", 0, 7),
    ("P", 1, 0), ("P", 1, 1), ("P", 1, 2), ("P", 1, 3), ("P", 1, 4), ("P", 1, 5), ("P", 1, 6), ("P", 1, 7),
    # Black
    ("r", 7, 0), ("n", 7, 1), ("b", 7, 2), ("q", 7, 3), ("k", 7, 4), ("b", 7, 5), ("n", 7, 6), ("r", 7, 7),
    ("p", 6, 0), ("p", 6, 1), ("p", 6, 2), ("p", 6, 3), ("p", 6, 4), ("p", 6, 5), ("p", 6, 6), ("p", 6, 7),
]}

turn = "white"  # White starts
 # drawing
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(WINDOW, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    for piece in pieces.values():
        piece.draw(WINDOW)

def draw_turn_box():
    pygame.draw.rect(WINDOW, BOX_COLOR, (0, HEIGHT - 50, WIDTH, 50))
    text_surface = FONT.render(f"{turn.capitalize()}'s Turn", True, TEXT_COLOR)
    WINDOW.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT - 40))

def draw_window():
    draw_board()
    draw_pieces()
    draw_turn_box()
    pygame.display.update()

# logi
def is_valid_move(from_pos, to_pos):
    if from_pos not in pieces:
        return False

    piece = pieces[from_pos]
    
    # turn validation
    if (turn == "white" and not piece.is_white) or (turn == "black" and piece.is_white):
        return False

    # tapture validation
    if to_pos in pieces and pieces[to_pos].is_white == piece.is_white:
        return False
    
    return True  

def move_piece(from_pos, to_pos):
    global turn
    if from_pos in pieces and is_valid_move(from_pos, to_pos):
        if to_pos in pieces and pieces[to_pos].piece.upper() == "K":
            check_winner()

        piece = pieces.pop(from_pos)
        piece.row, piece.col = to_pos  # uppdate position
        pieces[to_pos] = piece  # place in new location

        turn = "black" if turn == "white" else "white"  # switch turn

def check_winner():
    kings = [p.piece for p in pieces.values() if p.piece.upper() == "K"]
    if len(kings) < 2:
        winner = "White" if "K" in kings else "Black"
        print(f"{winner} wins!")
        pygame.quit()   
        sys.exit()

# --- Main Loop ---
def main():
    clock = pygame.time.Clock()
    selected_piece = None

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // SQUARE_SIZE, y // SQUARE_SIZE

                if row >= BOARD_SIZE:  # ignore clicks outside board
                    continue

                if selected_piece:
                    if selected_piece != (row, col):  # aivoid moving to the same square
                        move_piece(selected_piece, (row, col))
                    selected_piece = None
                else:
                    if (row, col) in pieces:
                        selected_piece = (row, col)
        
        draw_window()

if __name__ == "__main__":
    main()
