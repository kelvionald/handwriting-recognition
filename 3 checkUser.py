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

            def func1(x):
                key = x[0]
                middle = x[1]
                if key in data:
                    value = sum(data[key]) / len(data[key])
                    return (1 if cmp(value, middle) else 0)
                return -1

            checklist = list(map(func1, hw['modelMiddle']))
            checklist = list(filter(lambda x: x >= 0, checklist))
            if len(checklist) == 0:
                rating = 0
            else:
                rating = sum(checklist) / len(checklist)
            h = f.split('_')[0]
            if not name in statistic:
                statistic[name] = []
            statistic[name].append([h, round(rating, 2)])

minStat = {}
size = 0
for keys, values in statistic.items():
    print(keys)
    for x in values:
        if not keys in minStat:
            minStat[keys] = {'equals': [], 'notequals': []}
        err = ''
        if keys == x[0]:
            if x[1] >= accessLimit:
                minStat[keys]['equals'].append(1)
            else:
                minStat[keys]['equals'].append(0)
                err = '<--- equals'
        else:
            if x[1] >= accessLimit:
                minStat[keys]['notequals'].append(1)
                err = '<--- not equals'
            else:
                minStat[keys]['notequals'].append(0)
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
    minStat[i] = {
        'i': i,
        'equals': equals,
        'notequals': notequals,
        'eqPercent': round(equalsPercent, 2),
        'neqPercent': round(notequalsPercent, 2)
    }
print()
table = PrettyTable()
table.field_names = ["Номер подчерка", "Удачные", "Ошибки", "Удач.%", "Ошибки%", "Кол-во признаков"]
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
    'accessLimit': accessLimit
})