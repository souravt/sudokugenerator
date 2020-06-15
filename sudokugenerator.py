import numpy as np
import random
import pandas as pd

import pdfkit

basepath = "C://Users/sourav/Desktop/sudoku/"
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'


def generateGrid(width, height):
    gridArray = np.full([width, height], 0)

    for i in range(0, width - 1, 1):
        #  Get a random number
        match = False

        idx = 0
        while not match:
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

            if 0 in gridArray[i, :]:
                match = False
                gridArray[i, :] = np.zeros((9,), dtype=int)
            else:
                match = True
            idx = idx + 1
            if idx > 100:
                return

    for j in range(0, height, 1):
        temp = gridArray[0:height - 1, j]
        val = [k for k in range(1, width + 1, 1)]
        val = np.setdiff1d(val, temp)
        gridArray[height - 1][j] = val[0]

    # print(gridArray)

    return gridArray


def generatePagePDF(html, fileName):
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    output_file = basepath + str(fileName) + ".pdf"
    options = {'page-size': 'A5', 'dpi': 400}
    pdfkit.from_string(html, output_file, configuration=config, options=options)
    return output_file


def array_to_html(arr):
    html = "<html><head> <style> table{width:90%;margin-left: auto;margin-right: auto;} table,tr,td { border-collapse: collapse;}td { width :50px;height :50px;padding: 10px;font-size:32px; text-align:center;border-bottom:solid ;border-right:solid ;}td:first-child {border-left:2px solid;}td:nth-child(3n) {border-right:2px solid;}tr:first-child {border-top:2px solid;}tr:nth-child(3n){border-bottom:2px solid;} </style></head> <body>TO_REPLACE_BODY</body> </html>"

    tableHTML = "<table>"
    for x in arr:
        tableHTML += "<tr>"
        for y in x:
            if y == 0:
                tableHTML += "<td></td>"
            else:
                tableHTML += "<td>" + str(y) + "</td>"
        tableHTML += "</tr>"
    tableHTML += "</table>"
    html = html.replace('TO_REPLACE_BODY', tableHTML)
    return html


class SudokuGenerator:
    if __name__ == "__main__":
        sudokus = list()
        while len(sudokus) < 2:
            arrayGrid = generateGrid(9, 9)
            if arrayGrid is not None:
                sudokus.append(arrayGrid)

        puzzleCount = 0
        for suSol in sudokus:
            suProb = suSol.copy()
            maskDigits = random.randint(45, 70)
            idxArr = np.c_[np.random.randint(0, 9, maskDigits), np.random.randint(0, 9, maskDigits)]

            for idx in idxArr:
                suProb[idx[0]][idx[1]] = 0
            print(suSol)
            print(suProb)

            df = pd.DataFrame(suProb)
            puzzle_html = array_to_html(suProb)

            generatePagePDF(puzzle_html, 'Sudoku_' + str(puzzleCount))

            df = pd.DataFrame(suSol)
            df = df.replace('0', ' ')
            sol_html = array_to_html(df.values)

            generatePagePDF(sol_html, 'Sudoku_Solution_' + str(puzzleCount))

            puzzleCount = puzzleCount + 1
