def create_empty_board(shape):
    return {(x, y): False for x in range(shape[0]) for y in range(shape[1])}

def get_neighbours(x, y): 
    neighbours = [(x-1, y-1), (x+0, y-1), (x+1, y-1), (x-1, y+0), (x+1, y+0), (x-1, y+1), (x+0, y+1), (x+1, y+1)] 
                    
    nbr_nei = 0 
    for x, y in neighbours: 
        try: 
            if board[(x, y)]:
                nbr_nei += 1
        except KeyError: 
            pass

    return nbr_nei 

def print_board(shape): 
    # Yes, this is logical, trust me I am an engineer 
    for y in range(shape[1]): 
        for x in range(shape[0]): 
            print('0 ', end='') if board[(x, y)] else print('_ ', end='')
        print()
    print()

def create_planer(board):
    cells = [(0, 2), (1, 2), (2, 2), (1, 0), (2, 1)]
    for x, y in cells: 
        try:
            board[(x, y)] = True
        except KeyError:
            pass

def next_board(board):
    new_board = {}
    for (x, y), status in board.items():
        nbr_neighbours = get_neighbours(x, y)
        if status and nbr_neighbours in [2, 3] or (not status and nbr_neighbours == 3): 
            new_board[coor] = True
        else:
            new_board[coor] = False
    return new_board


if __name__ == '__main__':
    from time import sleep
    shape = (30, 30)
    board = create_empty_board(shape)
    create_planer(board)

    while True:
        print_board(shape)
        board = next_board(board)
        sleep(0.2)