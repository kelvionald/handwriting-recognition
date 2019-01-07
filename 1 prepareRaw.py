import os

rawData = './data/'
preparedPath = './prepared/'

def prepareRaw(path, newPath):
    '''Преобразует времена нажатия во времена переходов'''
    rawFile = open(path)
    delimeter = ';'#chr(32)
    started = False
    valuesUp = []
    valuesDown = []
    i = 15
    data = []
    for line in rawFile:
        values = line.split(delimeter)
        values[3] = values[3].replace('\n', '')
        if values[3] == '"KEY_UP"':
            started = True
            valuesUp = values
        elif started and values[3] == '"KEY_DOWN"':
            valuesDown = values
            dt = int(valuesDown[1]) - int(valuesUp[1])
            newRow = [
                valuesUp[0],
                valuesUp[2],
                valuesDown[2],
                str(dt)
            ]
            data.append(newRow)
    rawFile.close()
    
    preparedFile = open(newPath, 'w')
    preparedFile.write('"userId","key1","key2","dtime"' + '\n')
    for line in data:
        preparedFile.write(','.join(line) + '\n')
    preparedFile.close()
'''
files = os.listdir('./prepared/')

for file in files:
    prepareRaw(file)
'''

files = os.listdir('data')
dirs = list(filter(lambda x: not x.endswith('.csv'), files))

for d in dirs:
    files = os.listdir(rawData + d)
    for f in files:
        print('preparing file: ' + f)
        if not os.path.exists(preparedPath + d):
            os.mkdir(preparedPath + d)
        prepareRaw(rawData + d + '/' + f, preparedPath + d + '/' + f)