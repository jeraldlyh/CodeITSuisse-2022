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
    calculatedDict = {}
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


def get_largest_num(num, global_max, memoized_dict):
    if num == 1:
        return 4

    if num in memoized_dict:
        return memoized_dict[num]

    converted_price = convert_price(num)
    max_value = max(
        num,
        converted_price,
        get_largest_num(converted_price, converted_price, memoized_dict),
    )
    memoized_dict[num] = max(num, max_value, global_max)

    global_max = max(global_max, max_value, num)
    return get_largest_num(num, global_max, memoized_dict)


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
