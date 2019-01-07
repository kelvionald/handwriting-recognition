from config import *
import math

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