from config import *

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