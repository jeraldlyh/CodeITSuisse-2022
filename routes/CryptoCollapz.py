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
    calculatedDict = dict()
    calculatedDict[1] = 4
    output = []
    for data_array in input_data:
        temp_data_array = []
        for data in data_array:
            appeared = False
            if (data in calculatedDict.keys()):
                temp_data_array.append(calculatedDict[data])
                continue
            temp_price = convert_price(data)
            max_price = max(temp_price, data)
            while temp_price >= 1:
                temp_price = convert_price(temp_price)
                if (temp_price in calculatedDict.keys()):
                    temp_data_array.append(
                        max(calculatedDict[temp_price], max_price))
                    appeared = True
                    break
                max_price = max(max_price, temp_price)
            if (not appeared):
                temp_data_array.append(max_price)
                calculatedDict[data] = max_price
        output.append(temp_data_array)
    return jsonify(output)
        

# print(cryptoCollapz([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]))

# [
#   // test case 1
#   [ 4, 4, 16, 4, 16 ],

#   // test case 2
#   [ 16, 52, 8, 52, 16 ],

#   // other test cases
#   ...
# ]
