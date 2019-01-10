import os
import math
from common import *

def getModel(path):
    '''Возвращае модель из файла'''
    f = open(path)
    f.readline()
    model = []
    for line in f:
        arr = line.split(',')
        arr = [x.replace('"', '') for x in arr]
        arr[1] = arr[1].replace('\n', '')
        model.append(arr[0] + ' ' + arr[1])
    f.close()
    return model

def createModel(commonModel, dataArr):
    modelMiddles = []
    modelStd = []

    middleDotsArr = {}
    movingAveragesArr = {}
    sigmaArrArr = {}
    for el in commonModel:
        for d in dataArr:
            key = el['key']
            if key in d:
                middleDots, movingAverages, sigmaArr, lines = GraphData.getMiddleLines(dataArr, key)
                middleDotsArr[key] = middleDots
                movingAveragesArr[key] = movingAverages
                sigmaArrArr[key] = sigmaArr
    for el in commonModel:
        timeSeries = []
        elements = []
        for d in dataArr:
            key = el['key']
            if key in d:
                [elements.append(x) for x in d[key]]
                timeSeries.append(d[key])
                # print(d[key])

        middle = middleCalc(elements)
        def cmp(el):
            return middle + border >= el and el >= middle - border
        elementsPrep = list(map(lambda x: 1 if cmp(x) else 0, elements))

        percent = middleCalc(elementsPrep)
        if percent > limit:
            arr = key.split(' ')
            arr = list(map(int, arr))
            modelMiddles.append([key, middle])
        else:
            arr = key.split(' ')
            arr = list(map(int, arr))
            # if key == '66 32':
            currSigma = sigmaArrArr[key]
            newDots = []
            for i in range(0, len(timeSeries)):
                for ts in timeSeries[i]:
                    if ts < currSigma[i]:
                        newDots.append(ts)
            middle = middleCalc(newDots)
            elementsPrep = list(map(lambda x: 1 if cmp(x) else 0, newDots))
            percent = middleCalc(elementsPrep)
            # print(percent, StdLimit)
            if percent > StdLimit:
                modelStd.append([key, middle])
    return modelMiddles, modelStd

'''
# Создает графики попыток по общей модели
lensArr, dataArr, commonModel = prepareData(files)
graphNum = 1
model = getModel('k2k_model_56.csv')
for key in model:
    showGraph(graphNum, dataArr, key)
    graphNum += 1
'''

'''
files = os.listdir('./prepared/')
lensArr, dataArr, commonModel = prepareData(files)
border = 40
limit = 0.9
model = createModel(commonModel, dataArr)

# checking
data = getData('./3573_28-12-2018_14-27-28.csv')
checklist = []
for m in model:
    key = m[0]
    middle = m[1]
    if key in data:
        value = sum(data[key]) / len(data[key])
        if middle + border > value and value > middle - border:
            checklist.append(1)
        else:
            checklist.append(0)
print(sum(checklist) / len(checklist))
'''

def saveUser(path, user):
    f = open(path, 'w')
    f.write('"key","middle"' + '\n')
    for line in user:
        line = list(map(lambda x: '"' + str(x) + '"', line))
        f.write(','.join(line) + '\n')
    f.close()

import json

def saveUser2(path, modelMiddle, modelStd):
    data = {
        'modelMiddle': modelMiddle,
        'modelStd': modelStd
    }
    f = open(path, 'w')
    f.write(json.dumps(data))
    f.close()

preparedPath = './prepared/'
userPath = './users/'
files = os.listdir(preparedPath)
dirs = list(filter(lambda x: not x.endswith('.csv'), files))
for d in dirs:
    # if d != '5643': continue # testing
    files = os.listdir(preparedPath + d)
    userId = files[0].split('_')[0]
    files = list(map(lambda x: preparedPath + d + '/' + x, files))
    lensArr, dataArr, commonModel = prepareData(files)
    model, modelStd = createModel(commonModel, dataArr)
    path = userPath + userId + '.csv'
    saveUser2(path, model, modelStd)
    print('complete: ', d)