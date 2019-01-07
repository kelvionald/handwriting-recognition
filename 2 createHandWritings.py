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
    model = []
    for el in commonModel:
        timeSeriesArr = []
        elements = []
        for d in dataArr:
            key = el['key']
            if key in d:
                timeSeriesArr.append(d[key])
                [elements.append(x) for x in d[key]]
        middle = sum(elements) / len(elements)
        leng = len(elements)
        for i in range(0, leng):
            el = elements[i]
            if middle + border >= el and el >= middle - border:
                elements[i] = 1
            else:
                elements[i] = 0
        percent = sum(elements) / leng
        if percent > limit:
            arr = key.split(' ')
            arr = list(map(int, arr))
            # print(key, getChar(arr[0]) + ' ' + getChar(arr[1]), percent)
            model.append([key, middle])
    return model

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

preparedPath = './prepared/'
userPath = './users/'
files = os.listdir(preparedPath)
dirs = list(filter(lambda x: not x.endswith('.csv'), files))
for d in dirs:
    files = os.listdir(preparedPath + d)
    userId = files[0].split('_')[0]
    files = list(map(lambda x: preparedPath + d + '/' + x, files))
    lensArr, dataArr, commonModel = prepareData(files)
    model = createModel(commonModel, dataArr)
    path = userPath + userId + '.csv'
    saveUser(path, model)