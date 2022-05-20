#pip install prettytable

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

from prettytable import PrettyTable
from os import walk, path, chdir
from sys import argv
from multiprocessing import Pool

def getLineCount(filePath):
    f = open(filePath)
    lineCount = len(f.readlines())
    f.close()
    return lineCount

def main():
    sortBy = "FILES"
    for i in argv:
        if "-sort:" in i: sortBy = i[6:].upper()

    listOfFiles = []
    dirCount = 0

    chdir(argv[1])
    for root, dirs, files in walk("."):
        gotoTop = False
        for ignoreDir in ignoreDirs:
            if(ignoreDir in root):
                gotoTop = True
                break
        if gotoTop: continue
        dirCount += 1
        for file in files:
            shouldAppend = True
            for ignoreExt in ignoreExts:
                if(file.endswith(ignoreExt)):
                    shouldAppend = False
                    break
            if shouldAppend: listOfFiles.append(path.join(root, file))

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
    table.sortby = sortBy
    print(table,"\nTotal lines:", sum(lines), "\nFiles:", len(listOfFiles), "\t\tDirectories:", dirCount)

if(__name__ == "__main__"): main()
