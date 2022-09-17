from collections import defaultdict

from flask import jsonify, request

from routes import app


def convert_price(value):
    if value % 2 == 0:
        value = value // 2
    else:
        value = value * 3 + 1
    return value


@app.route("/cryptocollapz", methods=["POST"])
def cryptoCollapz():
    input_data = request.get_json()
    return jsonify(sol(input_data))


def sol(input_data):
    calculatedDict = defaultdict(int)
    output = []
    for data_array in input_data:
        temp_data_array = []
        for data in data_array:

            if data in calculatedDict:
                temp_data_array.append(calculatedDict[data])
            else:
                temp_data_array.append(get_largest_num(data, data, calculatedDict))
        output.append(temp_data_array)
    print(calculatedDict)
    return output


def get_largest_num(num, currMax, calculatedDict):
    if num == 1:
        return 4

    if num in calculatedDict:
        return calculatedDict[num]

    temp = convert_price(num)
    tempMax = max(num, temp, get_largest_num(temp, temp, calculatedDict))
    calculatedDict[temp] = tempMax
    currMax = max(currMax, tempMax, num)
    return get_largest_num(temp, currMax, calculatedDict)


# calculatedDict = dict()
# print(get_largest_num(7, 1, calculatedDict))

# print(sol([[1, 2, 3, 4, 5],
#            [6, 7, 8, 9, 10]]))


# [
#   // test case 1
#   [ 4, 4, 16, 4, 16 ],

#   // test case 2
#   [ 16, 52, 8, 52, 16 ],

#   // other test cases
#   ...
# ]
