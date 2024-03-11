from openpyxl import Workbook
import main
from itertools import product
from tabulate import tabulate
import numpy as np
import argparse

wb = Workbook()
ws = wb.active

data = [["Scale", "WinStride", "People"]]
scales = np.arange(1.01, 1.5, 0.05)
wStrides = [4, 8, 12, 16, 24, 32]

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to video file/stream")
args = vars(ap.parse_args())

fileName = args["video"]
fileNameSplit = args["video"].split(".")[0]

for args in product(scales, wStrides):
    people = main.img_detection(fileName, *args)
    data.append([args[0], args[1], people])
table = tabulate(data)
print(table)
for row in data:
    ws.append(row)

wb.save(fileName+".xlsx")