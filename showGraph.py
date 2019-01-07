import matplotlib.pyplot as plt
import os

from common import *

def showGraph(user, graphNum, dataArr, key, newDir = '', isShow = False):
    '''Выводи график времен перехода по попыткам'''
    print(user, ' key: ', key)
    keyArr = key.split(' ')
    transition = getChar(int(keyArr[0])) + ' - ' + getChar(int(keyArr[1]))
    plt.title('Переход: ' + transition)
    lastMean = 0
    x = 1
    
    middleValue = 0
    values = []
    count = 0
    plt.scatter(x, 1000, color= 'white')
    plt.scatter(x, 0, color= 'white')
    for d in dataArr:
        if key in d:
            timeSeries = d[key]
            if len(timeSeries) == 0:
                currMean = 0
            else:
                currMean = int(sum(timeSeries) / len(timeSeries))
            if lastMean != 0:
                plt.plot([x - 1, x], [lastMean, currMean], marker = 'o', color= '#588dff')
            lastMean = currMean
            
            for y in timeSeries:
                plt.scatter(x, y, color= '#673ab7')
                values.append(y)

            middleValue += currMean
            count += 1
        x += 1
    
    if count != 0:
        middleValue /= count
        plt.plot([1, x-1], [middleValue, middleValue], marker = 'o', color= 'y')
    
    commonPath = newDir + user + ' ' + str(graphNum) + ' ' + key
    if isShow:
        plt.show()
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

# Пакетная обработка с предобработкой
preparedPath = 'prepared/'
graphsPath = 'graphs/'
dirs = os.listdir(preparedPath)
for user in dirs:
    xpath = preparedPath + user + '/'
    files = os.listdir(xpath)
    dir = graphsPath + user + '/'
    if not os.path.exists(dir):
        os.makedirs(dir)
    files = list(map(lambda x: xpath + x, files))
    lensArr, dataArr, commonModel = prepareData(files)
    graphNum = 1
    model = sortModel(lensArr[0])
    for el in model:
        # if '74 0' == el['key']:
        showGraph(user, graphNum, dataArr, el['key'], dir)
        graphNum += 1