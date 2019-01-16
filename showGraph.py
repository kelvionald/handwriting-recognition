import matplotlib.pyplot as plt
import os
import math
import json

from common import *

def showGraph2(user, key, graphNum, dots, lines, path):
    '''Выводи график времен перехода по попыткам'''
    print(user, ' key: ', key)
    keyArr = key.split(' ')
    transition = getChar(int(keyArr[0])) + ' - ' + getChar(int(keyArr[1]))
    plt.title('Переход: ' + transition)
    plt.scatter(1, 1000, color= 'white')
    plt.scatter(1, 0, color= 'white')
    
    for dot in dots:
        plt.scatter(dot[0], dot[1], color = dot[2], s = 6)
    for line in lines:
        plt.plot(line[0], line[1], marker = ',', color = line[3])
        
    commonPath = path + user + ' ' + str(graphNum) + ' ' + key
    try:
        plt.savefig(commonPath + ' ' + transition + '.png')
    except OSError:
        print('Err filename: ' + commonPath + ' ' + transition)
        plt.savefig(commonPath + '.png')
    except ValueError:
        print('Err filename: ' + commonPath + ' ' + transition)
        plt.savefig(commonPath + '.png')
    plt.clf()

def sortModel(lens):
    for i in range(0, len(lens)):
        for j in range(i + 1, len(lens)):
            if lens[i]['length'] < lens[j]['length']:
                lens[i], lens[j] = lens[j], lens[i]
    return lens

def saveAdditionalData(path, data):
    f = open(path, 'w')
    f.write(json.dumps(data, indent=2, sort_keys=True))
    f.close()

colorBadDot = 'red'

# Пакетная обработка с предобработкой
preparedPath = 'prepared/'
graphsPath = 'graphs/'
dirs = os.listdir(preparedPath)
commonStat = {}
for user in dirs:
    if user != '5643': continue # testing
    xpath = preparedPath + user + '/'
    files = os.listdir(xpath)
    dir = graphsPath + user + '/'
    if not os.path.exists(dir):
        os.makedirs(dir)
    files = list(map(lambda x: xpath + x, files))
    lensArr, dataArr, commonModel = prepareData(files)
    graphNum = 1
    model = sortModel(lensArr[0])
    i = 10
    addData = {}
    for el in model:
        key = el['key']
        if (isContainsSpaces(key)):
            print('continue ', key)
            continue
        # if '66 32' != key: continue # testing
        i -= 1
        # if i == 0: break # testing

        lines = []
        dots = []
        # Сборка точек
        tmp = GraphData.getDots(dataArr, key)
        [dots.append(x) for x in tmp]
        # Сборка средних линий
        middleDots, movingAverages, sigmaArr, tmp = GraphData.getMiddleLines(dataArr, key)
        [lines.append(x) for x in tmp]
        # Перекраска точек выше стандартного отклонения
        for j in range(0, len(dots)):
            attemptNum = dots[j][0]
            value = dots[j][1]
            if value > sigmaArr[attemptNum - 1]:
                dots[j][2] = colorBadDot
        # Общая средняя линия
        if len(middleDots) != 0:
            commonMiddle = GraphData.getCommonMiddleLine(middleDots)
            lines.append([[1, len(middleDots)], [commonMiddle, commonMiddle], 'o', '#fefe22'])

        # showGraph2(user, key, graphNum, dots, lines, dir)
        graphNum += 1
        addData[key] = {}
        addData[key]['dots'] = list(map(lambda x: str(x), dots))
        stat = {}
        print(len(dots))
        for dd in dots:
            if dd[2] == colorBadDot:
                continue
            key22 = dd[1]
            if not key22 in stat:
                stat[key22] = 0
            stat[key22] += 1
        stat2 = []
        for kk, vv in stat.items():
            stat2.append([kk, vv])
        stat2.sort(key=lambda x: int(x[1]), reverse=True)
        # print(stat2)
        addData[key]['stat'] = stat2#list(map(lambda x: str(x), stat2))
        if not user in commonStat:
            commonStat[user] = {}
        commonStat[user][key] = addData[key]['stat'][0][0]
        # break
    saveAdditionalData(graphsPath + user + '/dots.txt', addData)
    # break
saveAdditionalData(graphsPath + 'commonStat.txt', commonStat)
