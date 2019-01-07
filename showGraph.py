import matplotlib.pyplot as plt
import os
import math

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

class GraphData:
    @staticmethod
    def getDots(dataArr, key):
        dots = []
        x = 1
        for d in dataArr:
            if key in d:
                timeSeries = d[key]
                for y in timeSeries:
                    dots.append([x, y, '#673ab7'])
                x += 1
        return dots
    @staticmethod
    def getMiddleLines(dataArr, key):
        middleDots = []
        movingAverages = []
        sigmaArr = []
        x = 1
        lastMean = 0
        lines = []
        for d in dataArr:
            if key in d:
                timeSeries = d[key]
                if len(timeSeries) == 0:
                    currMean = 0
                else:
                    currMean = int(sum(timeSeries) / len(timeSeries))

                if lastMean != 0:
                    lines.append([ [x - 1, x], [lastMean, currMean], 'o', '#588dff' ]) # testing

                    # indicator MA
                    middleDots.append(currMean)
                    movingAverage = sum(middleDots) / len(middleDots)
                    movingAverages.append(movingAverage)
                    # lines.append([ [x - 1, x], [movingAverages[len(movingAverages) - 2], movingAverage], 'o', 'black' ])

                    # standart deviation
                    s = 0
                    for m in middleDots:
                        s += (m - movingAverage) ** 2
                    s /= len(middleDots)
                    sigma = math.sqrt(s)
                    sigmaArr.append(sigma)
                    prevSigma = sigmaArr[len(sigmaArr) - 2]
                    lines.append([ [x - 1, x], [movingAverage + prevSigma, movingAverage + sigma], ',', 'grey' ])
                    # lines.append([ [x - 1, x], [movingAverage - prevSigma, movingAverage - sigma], ',', 'grey' ])

                lastMean = currMean
                x += 1
        return middleDots, movingAverages, sigmaArr, lines
    @staticmethod
    def getCommonMiddleLine(middleDots):
        return int(sum(middleDots) / len(middleDots))

# Пакетная обработка с предобработкой
preparedPath = 'prepared/'
graphsPath = 'graphs/'
dirs = os.listdir(preparedPath)
for user in dirs:
    if user != '5643':
        continue
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
    for el in model:
        key = el['key']
        if '66 32' != key: continue # testing
        i -= 1
        if i == 0: break # testing

        lines = []
        dots = []
        # Сборка точек
        tmp = GraphData.getDots(dataArr, key)
        [dots.append(x) for x in tmp]
        # Сборка средних линий
        middleDots, movingAverages, sigmaArr, tmp = GraphData.getMiddleLines(dataArr, key)
        [lines.append(x) for x in tmp]
        # Общая средняя линия
        if len(middleDots) != 0:
            commonMiddle = GraphData.getCommonMiddleLine(middleDots)
            lines.append([[1, len(middleDots)], [commonMiddle, commonMiddle], 'o', '#fefe22'])

        showGraph2(user, key, graphNum, dots, lines, dir)
        graphNum += 1

# Одиночная обработка
# user = '8'
# xpath = 'prepared/' + user + '/'
# files = os.listdir(xpath)
# # Создает графики попыток по всем переходам
# files = list(map(lambda x: xpath + x, files))
# lensArr, dataArr, commonModel = prepareData(files)
# graphNum = 1
# model = sortModel(lensArr[0])
# for el in model:
#     showGraph(user, graphNum, dataArr, el['key'])
#     graphNum += 1

# # Пакетная обработка
# preparedPath = 'prepared/'
# graphsPath = 'graphs/'
# dirs = os.listdir(preparedPath)
# for user in dirs:
#     xpath = preparedPath + user + '/'
#     files = os.listdir(xpath)
#     dir = graphsPath + user + '/'
#     if not os.path.exists(dir):
#         os.makedirs(dir)
#     files = list(map(lambda x: xpath + x, files))
#     lensArr, dataArr, commonModel = prepareData(files)
#     graphNum = 1
#     model = sortModel(lensArr[0])
#     for el in model:
#         # if '74 0' == el['key']:
#         showGraph(user, graphNum, dataArr, el['key'], dir)
#         graphNum += 1