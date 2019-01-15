# Обрезка времени перехода более заданного числа
obrubka = 500
# Допуск 
access = 0.85

getPercent = lambda x: round(x[0], 3)

def printResult(result):
    result = [getPercent(x) for x in result]
    print(result)