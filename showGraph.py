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

# Пакетная обработка с предобработкой
preparedPath = 'prepared/'
graphsPath = 'graphs/'
dirs = os.listdir(preparedPath)
for user in dirs:
    # if user != '5643': continue # testing
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
                dots[j][2] = 'red'
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