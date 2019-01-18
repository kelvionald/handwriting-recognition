a = [[1, 2], [3, 4], [5, 6], [7, 8]]

combinations = []

def combine(arr, digits, digit = None):
    def getDigits(hh, d, isFinal = 0):
        gg = [x for x in hh]
        gg.append(d)
        if isFinal == 1:
            combinations.append(gg)
        return gg
    if len(arr[1:]) == 0:
        return [
            {
                'digit': arr[0][0],
                'digits': getDigits(digits, arr[0][0], 1)
            },
            {
                'digit': arr[0][1],
                'digits': getDigits(digits, arr[0][1], 1)
            }
        ]
    return [
        {
            'digit': arr[0][0],
            'arr': combine(arr[1:], getDigits(digits, arr[0][0]), arr[0][0])
        },
        {
            'digit': arr[0][1],
            'arr': combine(arr[1:], getDigits(digits, arr[0][1]), arr[0][1])
        }
    ]

# sample
# combine(a, [])
# print(combinations)
# combinations = []
# combine([[1, 2], [3, 4], [5, 6], [7, 12]], [])
# print(combinations)