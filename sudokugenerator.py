import numpy as np
import random


def generateGrid(width, height):
    gridArray = np.full([width, height], 0)


    for i in range(0, width-1, 1):
        #  Get a random number
        match = False

        idx = 0
        while not match :
            seed = [k for k in range(1, width + 1, 1)]
            random.shuffle(seed)

            for j in range(0, height, 1):

                gRow = (i // 3) * 3
                gCol = (j // 3) * 3

                for val in seed:
                    if val not in gridArray[i, :] and val not in gridArray[:, j] and val not in gridArray[gRow:gRow + 2,
                                                                                                gCol:gCol + 2]:
                        gridArray[i][j] = val
                        # print('row', i, 'col', j, 'val', val)
                        break

            if 0 in gridArray[i, :] :
                match = False
                gridArray[i, :] = np.zeros((9,), dtype=int)
            else :
                match = True
            idx = idx + 1
            if idx >100 :
                return


    for j in range(0, height, 1):
        temp = gridArray[0:height-1,j]
        val = [k for k in range(1, width + 1, 1)]
        val = np.setdiff1d(val, temp)
        gridArray[height-1][j] = val[0]

    print(gridArray)

    return gridArray


class SudokuGenerator:
    if __name__ == "__main__":
        sudokus = list()
        while len(sudokus) < 25 :
            arrayGrid = generateGrid(9, 9)
            if arrayGrid is not None :
                sudokus.append(arrayGrid)
