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

from sys import argv
from multiprocessing import Pool

def getLineCount(filePath):
    f = open(filePath)
    lineCount = len(f.readlines())
    f.close()
    return lineCount

def getLineCountAndTags(filePath):
    f = open(filePath)
    lines = f.readlines()
    todoCount = 0
    fixmeCount = 0
    todoLines = []
    fixmeLines = []
    lineNum = 1
    for line in lines:
        if "TODO" in line:
            todoCount += 1
            todoLines.append(lineNum)
        if "FIXME" in line:
            fixmeCount += 1
            fixmeLines.append(lineNum)
        lineNum += 1
    f.close()
    return [filePath, todoCount, todoLines, fixmeCount, fixmeLines]

def showTagsFunc(listOfFiles):
    pool = Pool(processes=4)
    data = pool.map(getLineCountAndTags, listOfFiles)
    pool.close()
    pool.join()
    x = 0
    print("[TODO]")
    for i in data:
        while i[1] > 0:
            print(i[0]+":",i[2][x])
            x += 1
            i[1] -= 1
    x = 0
    print("[FIXME]")
    for i in data:
        while i[3] > 0:
            print(i[0]+":",i[4][x])
            x += 1
            i[3] -= 1

def RenderMDFile(filePath):
    #budget rendering
    try: f = open(filePath)
    except FileNotFoundError: print("Invalid file path:", filePath)
    else:
        for line in f:
            line = line.lstrip("#")
            line = line.lstrip("`")
            print(line,end="")
        f.close()

def main():
    if argv[1].endswith("md") or argv[1].endswith("MD"):
        RenderMDFile(argv[1])
        return
    
    sortBy = "FILES"
    showTags = False
    for i in argv[2:]:
        if "-sort:" in i: sortBy = i[6:].upper()
        elif "-tags" in i: showTags = True

    listOfFiles = []
    dirCount = 0

    from os import walk, path, chdir

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

    if(showTags):
        showTagsFunc(listOfFiles)
        return

    from prettytable import PrettyTable

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
