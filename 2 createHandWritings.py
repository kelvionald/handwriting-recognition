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

    # middleDotsArr = {}
    # movingAveragesArr = {}
    # sigmaArrArr = {}
    # for el in commonModel:
    #     for d in dataArr:
    #         key = el['key']
    #         if (isContainsSpaces(key)):
    #             print('continue ', key)
    #             continue
    #         if key in d:
    #             middleDots, movingAverages, sigmaArr, lines = GraphData.getMiddleLines(dataArr, key)
    #             middleDotsArr[key] = middleDots
    #             movingAveragesArr[key] = movingAverages
    #             sigmaArrArr[key] = sigmaArr
    for el in commonModel:
        key = el['key']
        if (isContainsSpaces(key)):
            print('continue ', key)
            continue
        timeSeries = []
        elements = []
        for d in dataArr:
            if key in d:
                [elements.append(x) for x in d[key]]
                timeSeries.append(d[key])
                
        arr = key.split(' ')
        arr = list(map(int, arr))
        # if key == '66 32':
        # currSigma = sigmaArrArr[key]
        newDots = []
        for i in range(0, len(timeSeries)):
            sigmaArr = getSigmaArr(timeSeries[i])
            for j in range(0, len(sigmaArr)):
                ts = timeSeries[i][j]
                middle = middleCalc(timeSeries[i])
                if ts <= sigmaArr[j] * StdMultiplier + middle and ts >= middle - sigmaArr[j] * StdMultiplier:
                    newDots.append(ts)
        middle = middleCalc(newDots)
        elementsPrep = list(map(lambda x: 1 if cmp(x, middle) else 0, newDots))
        percent = middleCalc(elementsPrep)
        # print(percent, StdLimit)
        if percent > StdLimit:
            modelStd.append([key, middle])
    return modelMiddles, modelStd

def saveUser(path, user):
    f = open(path, 'w')
    f.write('"key","middle"' + '\n')
    for line in user:
        line = list(map(lambda x: '"' + str(x) + '"', line))
        f.write(','.join(line) + '\n')
    f.close()

import json

def saveUser2(path, modelMiddle, modelStd, key):
    data = {
        'key': key,
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
    saveUser2(path, model, modelStd, d)
    print('complete: ', d)