import numpy as np

board_shape=(6,7)
board = np.zeros(board_shape).astype('int32')

print(board)

value = 0


for r in range(6):
    row_array = [int(i) for i in list(board[r,:])]
    for c in range(7-3):
        window = row_array[c:c+4]