getPercent = lambda x: round(x[0], 3)

def printResult(result):
    result = [getPercent(x) for x in result]
    print(result)