import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense
import time
import json
import os
from common import *

if not os.path.exists('models'):
    os.makedirs('models')

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

# save model
f = open('models/common.json', 'w')
f.write(json.dumps(arr, indent=2, sort_keys=True))
f.close()

# exit()
# arr = arr[0:5]

userInputs = {}
for uid in jd:
    userInputs[uid] = {}
    for aa in arr:
        userInputs[uid][aa] = jd[uid][aa]
    print(uid, userInputs[uid])

def normalize2(userInputs):
    for k, v in userInputs.items():
        userInputs[k] = v/obrubka
    return userInputs

def prepareForInputs(data):
    arrInputs = []
    for d in data:
        values = list(data[d].values())
        arrInputs.append(values)
    return arrInputs

def trainNN(inputs, outputs, uid):
    print(inputs, outputs)
    countKeys = len(inputs[0])
    training_data = np.array(inputs, "float32")
    target_data = np.array(outputs, "float32")
    model = Sequential()
    model.add(Dense(40, input_dim=countKeys, activation='relu'))
    model.add(Dense(40, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='mean_squared_error',
                optimizer='adam',
                metrics=['binary_accuracy'])
    t = current_milli_time()
    model.fit(training_data, target_data, nb_epoch=3000, verbose=2)
    print('dt=', (current_milli_time() - t) / 1000)
    result = model.predict(training_data)
    printResult(result)
    return model

f = open('log-training.txt', 'w')
f.write('')
f.close()

def log(a):
    f = open('log-training.txt', 'a')
    f.write(a + "\n")
    f.close()

t_common = current_milli_time()
for uid in userInputs:
    userInputs[uid] = normalize2(userInputs[uid])
userInputsT = userInputs
tmpKeys = userInputs.keys() 
userInputs = prepareForInputs(userInputs)
print(userInputs)
for uid in userInputsT:
    print('training user ', uid)
    outputs = [0 for x in range(0, len(userInputs))]
    index = list(tmpKeys).index(uid)
    outputs[index] = 1
    outputs = [[x] for x in outputs]
    t = current_milli_time()
    nn = trainNN(userInputs, outputs, uid)
    log('dt=' + str((current_milli_time() - t) / 1000))
    nn.save('models/' + uid + '.h5')
    # break
log('dt_common=' + str((current_milli_time() - t_common) / 1000))
