"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 28, 2022
"""

def is_empty(board):
    # This function returns True iff there are no stones on the board board
    # Procedure: Run through every square (board[i][j]) and confirm that it is an empty space
    for row in board:
        for element in row:
            if element != " ":
                return False
    return True



def is_bounded(board, y_end, x_end, length, d_y, d_x):
    # This function analyses the sequence of length length that ends at location (y end, x_end). The function returns "OPEN" if the sequence is open, "SEMIOPEN" if the sequence if semi-open, and "CLOSED" if the sequence is closed.
    # Assume that the sequence is complete (i.e., you are not just given a subsequence) and valid, and contains stones of only one colour.
    # Make sure to also check when the square surrounding the sequence is on the board
    #check when the length is 1

    #Following code attempts to find out if the sequence is bound by the dimensions of the board, then whether or not the space is empty
    if  d_x == -1 and (x_end + d_x) < 0:
        end_bound = True
    elif (y_end + d_y) >=  len(board) or (x_end + d_x) >=  len(board[0]):
        end_bound = True
    elif board[y_end + d_y][x_end + d_x] == " ":
        end_bound = False
    else:
        end_bound = True
    if  d_x == -1 and (x_end - d_x * length) >=  len(board[0]):
        start_bound = True
    elif (y_end - d_y * length) < 0 or (x_end - d_x * length) < 0:
        start_bound = True
    elif board[y_end - (d_y * length)][x_end - (d_x * length)] == " ":
        start_bound = False
    else:
        start_bound = True

    if start_bound == True and end_bound == True:
        return "CLOSED"
    elif start_bound == True and end_bound == False:
        return "SEMIOPEN"
    elif start_bound == False and end_bound == True:
        return "SEMIOPEN"
    elif start_bound == False and end_bound == False:
        return "OPEN"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
# This function analyses the row (let’s call it R) of squares that starts at the location (y start,x start)
# and goes in the direction (d y,d x). Note that this use of the word row is different from “a row in
# a table”. Here the word row means a sequence of squares, which are adjacent either horizontally,
# or vertically, or diagonally. The function returns a tuple whose first element is the number of open
# sequences of colour col of length length in the row R, and whose second element is the number of
# semi-open sequences of colour col of length length in the row R.
# Assume that (y start,x start) is located on the edge of the board. Only complete sequences count.
# For example, column 1 in Fig. 1 is considered to contain one open row of length 3, and no other rows.
# Assume length is an integer greater or equal to 2
    open_seq_count, semi_open_seq_count = 0, 0
    y = y_start
    x = x_start
    while y <= (len(board)-length*d_y) and x <= (len(board[0])-length*d_x):
        if d_x == -1 and x < (length - 1):
            break
        for i in range(length):
            if board[y+i*d_y][x+i*d_x] != col:
                y += d_y
                x += d_x
                break
            elif i == length - 1:
                if is_bounded(board, y+i*d_y, x+i*d_x, length, d_y, d_x) == "OPEN":
                    open_seq_count += 1
                elif is_bounded(board, y+i*d_y, x+i*d_x, length, d_y, d_x) == "SEMIOPEN":
                    if y == y_start and x== x_start:
                        semi_open_seq_count += 1
                    elif y == (len(board)-length*d_y) or x == (len(board[0])-length*d_x):
                        semi_open_seq_count += 1
                    elif board[y + length*d_y][x+length*d_x] != col and board[y + length*d_y][x+length*d_x] != ' ':
                        semi_open_seq_count += 1
                    elif board[y - d_y][x - d_x] != col and board[y - d_y][x - d_x] != ' ':
                        semi_open_seq_count += 1
                y = y + length*d_y
                x = x + length*d_x
    return open_seq_count, semi_open_seq_count

def detect_rows(board, col, length):
# This function analyses the board board. The function returns a tuple, whose first element is the
# number of open sequences of colour col of length lengthon the entire board, and whose second
# element is the number of semi-open sequences of colour col of length length on the entire board.
# Only complete sequences count. For example, Fig. 1 is considered to contain one open row of length
# 3, and no other rows.
# Assume length is an integer greater or equal to 2.
    open_seq_count, semi_open_seq_count = 0, 0
    # Check the horizontal rows for sequences
    for i in range(len(board)):
        open_seq, semi_open_seq = detect_row(board, col, i, 0, length, 0, 1)
        open_seq_count += open_seq
        semi_open_seq_count += semi_open_seq
    # Check the vertical rows for sequences
    for j in range(len(board[0])):
        open_seq, semi_open_seq = detect_row(board, col, 0, j, length, 1, 0)
        open_seq_count += open_seq
        semi_open_seq_count += semi_open_seq
    # Check the upper left to lower right diagonal for sequence
    # len(board)-1 because bottom left corner cannot start a sequence of length greater than 1
    for k in range(len(board)-1):
        open_seq, semi_open_seq = detect_row(board, col, k, 0, length, 1, 1)
        open_seq_count += open_seq
        semi_open_seq_count += semi_open_seq
    for l in range(1, len(board[0])-1):
        open_seq, semi_open_seq = detect_row(board, col, 0, l, length, 1, 1)
        open_seq_count += open_seq
        semi_open_seq_count += semi_open_seq
    # Check the upper right to lower left diagonal for sequence
    # tbh, len(board[0]) is unnecessary becauses it is the same as len(board) due to the board being square
    for m in range(1, len(board)-1):
        open_seq, semi_open_seq = detect_row(board, col, m, len(board[0])-1, length, 1, -1)
        open_seq_count += open_seq
        semi_open_seq_count += semi_open_seq
    #this loop runs from top right corner to the top left corner
    for n in range(len(board[0])-1, 0, -1):
        open_seq, semi_open_seq = detect_row(board, col, 0, n, length, 1, -1)
        open_seq_count += open_seq
        semi_open_seq_count += semi_open_seq

    return open_seq_count, semi_open_seq_count

def search_max(board):
# This function uses the function score() (provided) to find the optimal move for black. It finds the
# location (y,x), such that (y,x) is empty and putting a black stone on (y,x) maximizes the score of
# the board as calculated by score(). The function returns a tuple (y, x) such that putting a black
# stone in coordinates (y, x) maximizes the potential score (if there are several such tuples, you can
# return any one of them). After the function returns, the contents of board must remain the same
    top_score = -1000000000000000
    for y in range(len(board)):
        for x in range(len(board[0])):
            test_board = []
            for sublist in board:       #This creates a shallow copy so that board remains unchanged
                test_board.append(sublist[:])
            if board[y][x] == " ":      # This ensures that the square is empty
                test_board[y][x] = "b"
                if score(test_board) >= top_score:
                    top_score = score(test_board)
                    move_y = y
                    move_x = x
    return move_y, move_x


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def is_win(board):
    counter = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            #horizontal so account for changes in (0,1)
            if j<(len(board)-4):
                if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == board[i][j+4]:
                    a = board[i][j]
                    if a == "w":
                        return "White won"
                    elif a == "b":
                        return "Black won"
            # vertical so account for changes in (1,0)
            if i<(len(board)-4):
                if board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] == board[i+4][j]:
                    a = board[i][j]
                    if a == "w":
                        return "White won"
                    elif a == "b":
                        return "Black won"
            #accounts for right lower diagonal
            if i<(len(board)-4):
                if j<(len(board)-4):
                    if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == board[i+4][j+4]:
                        a = board[i][j]
                        if a == "w":
                            return "White won"
                        elif a == "b":
                            return "Black won"
            #accounts for right upper diagnonal
            if i<(len(board)-4):
                if j>3:
                    if board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] == board[i+4][j-4]:
                        a = board[i][j]
                        if a == "w":
                            return "White won"
                        elif a == "b":
                            return "Black won"
            #account for full board
            if board[i][j] != " ":
                counter += 1
                if counter == len(board)*len(board):
                    return "Draw"
    return "Continue Playing"


def print_board(board):
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)




def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))

def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x



def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    #Test 1
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")
    #Test 2
    board = make_empty_board(8)
    x = 5; y = 5; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 7
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'SEMIOPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")
    #Test 3
    board = make_empty_board(8)
    x = 5; y = 5; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    x = 3; y = 4; d_x = 1; d_y = 0; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)

    y_end = 7
    x_end = 5
    d_x = 0
    d_y = 1

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'CLOSED':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def test_is_win():
    #Test 1
    board = make_empty_board(8)
    x = 0; y = 0; d_x = 1; d_y = 0; length = 5
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    x = 5; y = 0; d_x = 1; d_y = 0; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)


    if is_win(board) == 'White won':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


if __name__ == '__main__':
    # play_gomoku(8)
    # easy_testset_for_main_functions()
    # some_tests()
    test_is_win()
