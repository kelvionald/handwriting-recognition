from config import *
import math

def middleCalc(arr):
    return sum(arr) / len(arr)

def getData(path):
    '''Возвращает данные переходов из файла'''
    f = open(path)
    f.readline()
    data = {}
    for line in f:
        arr = line.split(',')
        dtime = arr[3].replace('\n', '')
        dtime = int(dtime)
        if dtime > 1000:
            continue
        key = arr[1] + ' ' + arr[2]
        if not key in data:
            data[key] = []
        data[key].append(dtime)
    f.close()
    return data

def getChar(code):
    '''Код символа в символ'''
    ch = chr(code)
    if ch == ' ':
        return 'Пробел'
    return ch

def getLens(data):
    '''Возвращает сортированное количесво переходов'''
    lens = []
    for key in data.keys():
        lens.append({
            'key': key,
            'length': len(data[key])
        })
    return lens

def addModel(model, lens):
    for el in lens:
        key = el['key']
        index = -1
        for j, m in enumerate(model):
            if m['key'] == key:
                index = j
                break
        if index == -1:
            model.append(el)
        else:
            model[index]['length'] += el['length']
    return model

def prepareData(files):
    lensArr = []
    dataArr = []
    commonModel = []

    for file in files:
        data = getData(file)
        dataArr.append(data)
        lens = getLens(data)
        lensArr.append(lens)
        commonModel = addModel(commonModel, lens)
    return lensArr, dataArr, commonModel

    

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
                movingMiddleDots = middleDots[-StdPeriod:]
                for m in movingMiddleDots:
                    s += (m - movingAverage) ** 2
                s /= len(movingMiddleDots)
                sigma = math.sqrt(s)
                curSigma = movingAverage + sigma * StdMultiplier
                sigmaArr.append(curSigma)
                prevSigma = sigmaArr[len(sigmaArr) - 2]
                lines.append([ [x - 1, x], [prevSigma, curSigma], ',', 'grey' ])
                # lines.append([ [x - 1, x], [movingAverage - prevSigma, movingAverage - sigma], ',', 'grey' ])

                lastMean = currMean
                x += 1
        return middleDots, movingAverages, sigmaArr, lines
    @staticmethod
    def getCommonMiddleLine(middleDots):
        return int(sum(middleDots) / len(middleDots))

def cmp(el, middle):
    return middle + border >= el and el >= middle - border

def getSigmaArr(source):
    sigmaArr = []
    for i in range(0, len(source)):
        if i < StdPeriod:
            window = source[0:i + 1]
        else:
            window = source[i-2:i+1]
        middle = middleCalc(window)
        summa = sum(map(lambda x: (x - middle) ** 2, window))
        middleSqr = summa / len(window)
        sigma = math.sqrt(middleSqr)
        sigmaArr.append(sigma)
        # print(window, middle, sigma)
    return sigmaArr

# import matplotlib.pyplot as plt
# b = [1, 1, 1, 6, 2, 1, 8, 2, 2, 2, 2, 3]
# c = list(range(0, len(b)))
# a = getSigmaArr(b)

def isContainsSpaces(key):
    arr = key.split(' ')
    arr = list(map(int, arr))
    return chr(arr[0]) == ' ' or chr(arr[1]) == ' '