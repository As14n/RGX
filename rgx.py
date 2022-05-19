ignoreDirs = [
    ".git",
    ".vs",
    ".vscode",
    "bin",
]
ignoreExts = [
    "gitignore",
    "md",
    "txt",
]

from os import walk, path
from sys import argv
from multiprocessing import Pool
from prettytable import PrettyTable      #pip install prettytable

def getLineCount(filePath):
    f = open(filePath)
    lineCount = len(f.readlines())
    f.close()
    return lineCount

def main():
    listOfFiles = []

    for root, dirs, files in walk(argv[1]):
        for file in files:
            shouldAppend = True
            for ignoreExt in ignoreExts:
                if(file.endswith(ignoreExt)):
                    shouldAppend = False
                    break
                if(shouldAppend == False): continue
                for ignoreDir in ignoreDirs:
                    if(ignoreDir in root):
                        shouldAppend = False
                        break
            if(shouldAppend): listOfFiles.append(path.join(root, file))

    pool = Pool(processes=4)
    lines = pool.map(getLineCount, listOfFiles)
    pool.close()
    pool.join()

    table = PrettyTable(["FILES","LINES"])
    length = len(listOfFiles)
    x = 0
    while x != length:
        table.add_row([listOfFiles[x], lines[x]])
        x += 1
    table.align = "l"
    print(table)

if(__name__ == "__main__"): main()
