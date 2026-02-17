import pygame

pygame.init()
WIDTH, HEIGHT = 1680, 960
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("C.H.E.S.S")
font = pygame.font.SysFont('arial', 30)
font_small = pygame.font.SysFont('arial', 15)
clock = pygame.time.Clock()
fps = 120

# Game variables
white_pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook",
                "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]

black_pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook",
                "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]

white_locations = [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7),
                    (0,6), (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6)]

black_locations = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                    (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]

captured_white = []
captured_black = []

turn_step = 0
# 0 - white's turn no selected piece
# 1 - white's turn piece selected
# 2 - black's turn no selected piece
# 3 - black's turn piece selected

selection = 999
valid_moves = []

# Load in game piece images
black_queen = pygame.image.load('Assets/queen-b.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (40, 40))

white_queen = pygame.image.load('Assets/queen-w.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (40, 40))

black_king = pygame.image.load('Assets/king-b.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (40, 40))

white_king = pygame.image.load('Assets/king-w.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (40, 40))

black_rook = pygame.image.load('Assets/rook-b.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (40, 40))

white_rook = pygame.image.load('Assets/rook-w.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (40, 40))

black_bishop = pygame.image.load('Assets/bishop-b.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (40, 40))

white_bishop = pygame.image.load('Assets/bishop-w.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (40, 40))

black_knight = pygame.image.load('Assets/knight-b.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (40, 40))

white_knight = pygame.image.load('Assets/knight-w.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (40, 40))

black_pawn = pygame.image.load('Assets/pawn-b.png')
black_pawn = pygame.transform.scale(black_pawn, (60, 60))
black_pawn_small = pygame.transform.scale(black_pawn, (40, 40))

white_pawn = pygame.image.load('Assets/pawn-w.png')
white_pawn = pygame.transform.scale(white_pawn, (60, 60))
white_pawn_small = pygame.transform.scale(white_pawn, (40, 40))

white_images = [white_pawn, white_rook, white_knight, white_bishop, white_queen, white_king]
black_images = [black_pawn, black_rook, black_knight, black_bishop, black_queen, black_king]

white_images_small = [white_pawn_small, white_rook_small, white_knight_small, white_bishop_small, white_queen_small, white_king_small]
black_images_small = [black_pawn_small, black_rook_small, black_knight_small, black_bishop_small, black_queen_small, black_king_small]

pieces_list = ["pawn", "rook", "knight", "bishop", "queen", "king"]

# Check Variables


# Draw main board

def draw_board():
    colors = ["#769656", "#eeeed2"]
    square_size = 120
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (square_size * 3 + col * square_size, row * square_size, square_size, square_size))
    
    pygame.draw.rect(screen, "black", (square_size * 3, 0, square_size * 8, square_size * 8), 4)
    pygame.draw.rect(screen, "black", (0, 0, square_size * 3, square_size * 8), 4)
    pygame.draw.rect(screen, "black", (square_size * 11, 0, square_size * 3, square_size * 8), 4)
    
    # Show turn
    if turn_step == 0 or turn_step == 1:
        turn_text = font.render("White's Turn", True, "black")
    else:
        turn_text = font.render("Black's Turn", True, "black")

    screen.blit(turn_text, (20, 20))

    for i in range(9):
        pygame.draw.line(screen, "black", (square_size * 3, i * square_size), (square_size * 11, i * square_size), 2)
        pygame.draw.line(screen, "black", (square_size * 3 + i * square_size, 0), (square_size * 3 + i * square_size, square_size * 8), 2)

# Draw pieces on board

def draw_pieces():
    for i in range(len(white_pieces)):
        index = pieces_list.index(white_pieces[i])
        if white_pieces[i] == "pawn":
            screen.blit(white_images[index], (white_locations[i][0] * 120 + 3 * 120 + 27.5, white_locations[i][1] * 120 + 27.5))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 120 + 3 * 120 + 20, white_locations[i][1] * 120 + 20))
        
        # Highlight selected piece
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, "red", (white_locations[i][0] * 120 + 3 * 120, white_locations[i][1] * 120, 120, 120), 4)
            
    for i in range(len(black_pieces)):
        index = pieces_list.index(black_pieces[i])
        if black_pieces[i] == "pawn":
            screen.blit(black_images[index], (black_locations[i][0] * 120 + 3 * 120 + 27.5, black_locations[i][1] * 120 + 27.5))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 120 + 3 * 120 + 20, black_locations[i][1] * 120 + 20))
        
        # Highlight selected piece
        if turn_step >= 2:
                if selection == i:
                    pygame.draw.rect(screen, "red", (black_locations[i][0] * 120 + 3 * 120, black_locations[i][1] * 120, 120, 120), 4)

# Function to check all pieces valid options on board
def check_options(pieces, locations, color):
    moves_list = []
    all_moves_list = []
    for i in range(len(pieces)):
        if pieces[i] == "pawn":
            moves_list = pawn_moves(locations[i], color)
        # elif pieces[i] == "rook":
        #     moves_list = rook_moves(locations[i], color)
        # elif pieces[i] == "knight":
        #     moves_list = knight_moves(locations[i], color)
        # elif pieces[i] == "bishop":
        #     moves_list = bishop_moves(locations[i], color)
        # elif pieces[i] == "queen":
        #     moves_list = queen_moves(locations[i], color)
        # elif pieces[i] == "king":
        #     moves_list = king_moves(locations[i], color)
        all_moves_list.append(moves_list)
    return all_moves_list

# Check valid pawn moves

def pawn_moves(location, color):
    moves_list = []
    if color == 'white':
        if (location[0], location[1] - 1) not in white_locations and \
           (location[0], location[1] - 1) not in black_locations and location[1] > 0:
            moves_list.append((location[0], location[1] - 1))
        if (location[0], location[1] - 2) not in white_locations and \
           (location[0], location[1] - 2) not in black_locations and location[1] == 6:
            moves_list.append((location[0], location[1] - 2))
        if (location[0] - 1, location[1] - 1) in black_locations:
            moves_list.append((location[0] - 1, location[1] - 1))
        if (location[0] + 1, location[1] - 1) in black_locations:
            moves_list.append((location[0] + 1, location[1] - 1))

    if color == 'black':
        if (location[0], location[1] + 1) not in black_locations and \
           (location[0], location[1] + 1) not in white_locations and location[1] < 7:
            moves_list.append((location[0], location[1] + 1))
        if (location[0], location[1] + 2) not in black_locations and \
           (location[0], location[1] + 2) not in white_locations and location[1] == 1:
            moves_list.append((location[0], location[1] + 2))
        if (location[0] - 1, location[1] + 1) in white_locations:
            moves_list.append((location[0] - 1, location[1] + 1))
        if (location[0] + 1, location[1] + 1) in white_locations:
            moves_list.append((location[0] + 1, location[1] + 1))
        
    return moves_list

# check for valid moves for selected piece
def check_valid_moves():
    if selection in (100, 999):
        return []
    if turn_step < 2:
        option_list = check_options(white_pieces, white_locations, 'white')
    else:
        option_list = check_options(black_pieces, black_locations, 'black')

    return option_list[selection]

# draw valid moves on screen
def draw_valid(moves_list):
    for i in range(len(moves_list)):
        pygame.draw.circle(
            screen,
            "red",
            (moves_list[i][0] * 120 + 3 * 120 + 60, moves_list[i][1] * 120 + 60),
            10
        )

# Main game loop
is_running = True

while is_running:
    clock.tick(fps)
    screen.fill("white")

    draw_board()
    draw_pieces()
    
    if selection != (100):
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x= event.pos[0] // 120 - 3  # -3 for white space in sides
            y = event.pos[1] // 120
            click_coords = (x, y)
            print(click_coords)

            if turn_step <= 1:
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection not in (100, 999):
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_white.append(black_pieces[black_piece])
                        black_locations.pop(black_piece)
                        black_pieces.pop(black_piece)

                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []

            else:
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection not in (100, 999):
                    black_locations[selection] = click_coords
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_black.append(white_pieces[white_piece])
                        white_locations.pop(white_piece)
                        white_pieces.pop(white_piece)

                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
            
    
        
    pygame.display.flip()

pygame.quit()


