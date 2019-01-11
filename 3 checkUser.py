import os
from prettytable import PrettyTable
from common import *
import json

def readHandwriting(path):
    '''Возвращае подчерк из файла'''
    f = open(path)
    data = f.readline()
    hw = json.loads(data)
    f.close()
    return hw

statistic = {}

handWritingPath = 'users/'
files = os.listdir(handWritingPath)
files = list(map(lambda x: handWritingPath + x, files))
handwritigArr = list(map(readHandwriting, files))

preparedPath = 'prepared/'
files = os.listdir(preparedPath)
dirs = list(filter(lambda x: not x.endswith('.csv'), files))
for d in dirs:
    files = os.listdir(preparedPath + d)
    for f in files:
        data = getData(preparedPath + d + '/' + f)
        for hw in handwritigArr:
            checklist = []
            name = hw['key']
            for hwrow in hw['modelStd']:
                key = hwrow[0]
                middle = hwrow[1]
                if key in data:
                    sigmaArr = getSigmaArr(data[key])
                    currMiddle = middleCalc(data[key])
                    # data[key]
                    # print(sigmaArr)
                    newDots = []
                    for jj in range(0, len(sigmaArr)):
                        if data[key][jj] <= sigmaArr[jj] * 2 + currMiddle:
                            newDots.append(data[key][jj])
                    value = sum(newDots) / len(newDots)
                    checklist.append(1 if cmp(value, middle) else 0)
            if len(checklist) == 0:
                rating = 0
            else:
                rating = sum(checklist) / len(checklist)
            h = f.split('_')[0]
            if not name in statistic:
                statistic[name] = []
            statistic[name].append([h, round(rating, 2)])

minStat = {}
for keys, values in statistic.items():
    print(keys)
    for x in values:
        if not keys in minStat:
            minStat[keys] = {'equals': [], 'notequals': []}
        err = ''
        if keys == x[0]:
            if x[1] >= accessLimit:
                val = 1
            else:
                val = 0
                err = '<--- equals'
            minStat[keys]['equals'].append(val)
        else:
            if x[1] >= accessLimit:
                val = 1
                err = '<--- not equals'
            else:
                val = 0
            minStat[keys]['notequals'].append(val)
        if len(err) != 0:
            print(x, err)
print()
for keys, values in statistic.items():
    print('Количество сравнений по одельному подчерку: ', len(values))
    break

commonSuccess = 0
commonExpectSuccess = 0

commonError = 0
commonExpectError = 0

for i, v in minStat.items():
    sumEq = sum(v['equals'])
    lenEq = len(v['equals'])
    equalsPercent = sumEq / lenEq
    equals = str(sumEq) + '/' + str(lenEq)
    sumNEq = sum(v['notequals'])
    lenNEq = len(v['notequals'])
    notequals = str(sumNEq) + '/' + str(lenNEq)
    notequalsPercent = sumNEq / lenNEq
    commonSuccess += sumEq
    commonExpectSuccess += lenEq
    commonError += sumNEq
    commonExpectError += lenNEq
    for hw in handwritigArr:
        if i == hw['key']:
            lenHW = len(hw['modelMiddle'])
            break
    minStat[i] = {
        'Номер подчерка': i,
        'Удачные': equals,
        'Ошибки': notequals,
        'Удач.%': round(equalsPercent, 2),
        'Ошибки%': round(notequalsPercent, 2),
        'Кол-во признаков': lenHW
    }
print()
table = PrettyTable()
table.field_names = minStat[i].keys()
for i, v in minStat.items():
    table.add_row(v.values())
print(table)
print()
print('Итог успешные %:', round(commonSuccess / commonExpectSuccess, 4))
print('Итог ошибки %:', round(commonError / commonExpectError, 4))
print()
print({
    'border': border,
    'limit': limit,
    'accessLimit': accessLimit,
    'StdMultiplier': StdMultiplier,
    'StdPeriod': StdPeriod,
    'StdLimit': StdLimit
})