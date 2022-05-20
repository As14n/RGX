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

def getLineCount(filePath):
    f = open(filePath)
    lineCount = len(f.readlines())
    f.close()
    return lineCount

def RenderMDFile(filePath):
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

    from prettytable import PrettyTable
    from os import walk, path, chdir
    from multiprocessing import Pool
    
    sortBy = "FILES"
    for i in argv[2:]:
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
