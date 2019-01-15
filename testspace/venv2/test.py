import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense
import time
import json
import os

current_milli_time = lambda: int(round(time.time() * 1000))

def createCommonModelFromFile(path):
    a = os.path.abspath(path)
    print(a)
    f = open(path)
    jdata = ''
    for line in f:
        jdata += line
    f.close()
    data = json.loads(jdata)
    return data

jd = createCommonModelFromFile('graphs/commonStat.txt')
dictionary = {}
for u in jd:
    for k, v in jd[u].items():
        if not k in dictionary:
            dictionary[k] = 0
        dictionary[k] += 1

arr = []
for k in dictionary:
    if dictionary[k] == 8: 
        arr.append(k)

arr = arr[0:5]

userInputs = {}
for uid in jd:
    userInputs[uid] = {}
    for aa in arr:
        userInputs[uid][aa] = jd[uid][aa]
    print(uid, userInputs[uid])

def normalize2(userInputs):
    for k, v in userInputs.items():
        userInputs[k] = v/1000
    return userInputs

def prepareForInputs(data):
    arrInputs = []
    for d in data:
        values = list(data[d].values())
        arrInputs.append(values)
    return arrInputs

def prepareAndTrain(inputs, outputs, uid):
    print(inputs, outputs)
    countKeys = len(inputs[0])
    training_data = np.array(inputs, "float32")
    target_data = np.array(outputs, "float32")
    model = Sequential()
    model.add(Dense(20, input_dim=countKeys, activation='relu'))
    model.add(Dense(20, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='mean_squared_error',
                optimizer='adam',
                metrics=['binary_accuracy'])
    t = current_milli_time()
    model.fit(training_data, target_data, nb_epoch=1000, verbose=2)
    print('dt=', (current_milli_time() - t) / 1000)
    result = model.predict(training_data)
    getPercent = lambda x: round(x[0], 4)
    result = [getPercent(x) for x in result]
    print(result)
    return model

for uid in userInputs:
    userInputs[uid] = normalize2(userInputs[uid])
userInputsT = userInputs
tmpKeys = userInputs.keys() 
userInputs = prepareForInputs(userInputs)
for uid in userInputsT:
    print('training user ', uid)
    outputs = [0 for x in range(0, len(userInputs))]
    index = list(tmpKeys).index(uid)
    outputs[index] = 1
    outputs = [[x] for x in outputs]
    nn = prepareAndTrain(userInputs, outputs, uid)
    print(nn)
    break
