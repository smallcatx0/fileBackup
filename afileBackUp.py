import os
import shutil
import random
import time
import json

config = {}


def getallpath(root):
    """获取目录所有路径"""
    path_collection = []
    # 创建所有文件路径的储存日志文件
    with open(config['mateFileTree'], 'w', encoding='utf-8') as fp:
        fp.write('')
    for dirpath, dirnames, filenames in os.walk(root):
        filePathTemp = ''
        for file in filenames:
            fullpath = os.path.join(dirpath, file)
            fullpath = os.path.abspath(fullpath)
            path_collection.append(fullpath)
            filePathTemp += fullpath + '\n'
        with open(config['allFileTree'], 'a', encoding="utf-8") as fp:
            fp.write(filePathTemp)
    return path_collection


def backupFile(fFrom, toDir):
    if not os.path.isdir(toDir):
        os.makedirs(toDir)
    fTo = toDir + '\\' + os.path.basename(fFrom)
    shutil.copyfile(fFrom, fTo)


def BackUp(rootPath, backupPath):
    path = getallpath(rootPath)
    tar = []
    with open(config['mateFileTree'], 'w', encoding='utf-8') as fp:
        fp.write('')
    for oneFile in path:
        exc = os.path.splitext(oneFile)[1]
        if exc in config['mateAss']:
            tar.append(oneFile)
            with open(config['mateFileTree'], 'a', encoding='utf-8') as fp:
                fp.write(oneFile + '\n')
    for oneFile in tar:
        backupFile(oneFile, backupPath)
    print('have backuped ')


def needBackup(allFileTree):
    ranNum = []
    fList = []
    if not os.path.isfile(allFileTree):
        return 1
    ranStr = str(random.random())
    ranNum.append(int(ranStr[2:4]))
    ranNum.append(int(ranStr[6:8]))
    ranNum.sort()
    with open(allFileTree, encoding='utf-8') as fp:
        for x in range(101):
            fList.append(fp.readline())
        if not os.path.isfile(fList[ranNum[0]][:-1]):
            return 1
        if not os.path.isfile(fList[ranNum[1]][:-1]):
            return 1
    return 0


def waitToBackup(onePath):
    if not os.path.exists(onePath):
        print('no USB (sleep 5s)')
        time.sleep(5)
        return 0
    if not needBackup(config['allFileTree']):
        print('USB content is no change (sleep 5s)')
        time.sleep(5)
        return 0
    else:
        try:
            BackUp(onePath, config['backupPath'])
        except:
            pass


if __name__ == '__main__':
    config = json.load(open('fb.ini', encoding='utf-8'))
    while(1):
        for onePath in config['rootPath']:
            waitToBackup(onePath)
