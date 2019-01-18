from keras.models import load_model
import numpy as np
import os
from common import *
import json

def loadCommonModel(path):
    f = open(path)
    # data = f.readline()
    jdata = ''
    for line in f:
        jdata += line
    hw = json.loads(jdata)
    f.close()
    return hw

def getData(path):
    '''Возвращает данные переходов из файла'''
    f = open(path)
    f.readline()
    data = {}
    for line in f:
        arr = line.split(',')
        dtime = arr[3].replace('\n', '')
        dtime = int(dtime)
        if dtime > obrubka:
            continue
        key = arr[1] + ' ' + arr[2]
        if not key in data:
            data[key] = []
        data[key].append(dtime)
    f.close()
    return data

def prepareData(files):
    lensArr = []
    dataArr = {}

    for file in files:
        data = getData(file)
        dataArr[file] = data
    return lensArr, dataArr

import math

def getSigmaArr(source):
    sigmaArr = []
    for i in range(0, len(source)):
        if i < 2:
            window = source[0:i + 1]
        else:
            window = source[i-2:i+1]
        middle = sum(window)/len(window)
        summa = sum(map(lambda x: (x - middle) ** 2, window))
        middleSqr = summa / len(window)
        sigma = math.sqrt(middleSqr)
        sigmaArr.append(sigma)
        # print(window, middle, sigma)
    return sigmaArr


def prepareAttempt(attempt, commonModel):
    arr = {}
    arr2 = {}
    for m in commonModel:
        # print(m)
        arr[m] = attempt[m]
        # attempt[m] = list(filter(lambda x: x < 501, attempt[m]))
        # print(attempt[m])
        mid = sum(attempt[m])/len(attempt[m])
        arr[m] = mid / obrubka
    return [list(arr.values())]

def checkAttempt(nn, attempt):
    inputs = []
    training_data = np.array(attempt, "float32")
    result = nn.predict(training_data)
    return result

commonModel = loadCommonModel('models/common.json')

models = {}
dirs = os.listdir('models')
for d in dirs:
    if d == 'common.json':
        continue
    path = 'models/' + d
    models[d] = load_model(path)

kkk = list(models.keys())
def fff(x):
    return x.split('.')[0]
assocModels = list(map(fff, kkk))
print(assocModels)

assocModels = {}
for mm in models:
    assocModels[mm] = mm.split('.')[0]

counts = 0
errors = 0

preparedPath = './prepared/'
files = os.listdir(preparedPath)
dirs = list(filter(lambda x: not x.endswith('.csv'), files))
for da in dirs:
    # if d != '5643': continue # testing
    files = os.listdir(preparedPath + da)
    userId = files[0].split('_')[0]
    files = list(map(lambda x: preparedPath + da + '/' + x, files))
    lensArr, dataArr = prepareData(files)
    found = 0
    s = 0
    for d in dataArr:
        kk = d
        nameUserAttempt = da
        d = dataArr[d]
        keys = list(d.keys())
        obj = {}
        notFound = False
        for i in commonModel:
            if not i in keys:
                notFound = True
                break
        if not notFound:
            found += 1
            # check
            attempt = prepareAttempt(d, commonModel)
            results = []
            for dd in models:
                nn = models[dd]
                result = checkAttempt(nn, attempt)
                results.append(list(map(list, result)))
                ln = round(result[0][0], 3)
                if assocModels[dd] == nameUserAttempt and ln < access:
                    print('error == ', assocModels[dd], nameUserAttempt, ln)
                    errors += 1
                elif assocModels[dd] != nameUserAttempt and ln >= access:
                    print('error != ', assocModels[dd], nameUserAttempt, ln)
                    errors += 1
                counts += 1

            # print( kk)#list(models.keys())
            # print(results)
        s += 1
        # print(keys)
        # break
        # print(d)
        # break
    # print(s, found)
    # break
print('total', 'errors', errors, 'counts', counts)
print('success percent', (counts - errors) / counts)

print({
    'obrubka': obrubka,
    'access':access
})