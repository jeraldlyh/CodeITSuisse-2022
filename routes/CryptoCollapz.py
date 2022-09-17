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

    output = []
    for data_array in input_data:
        temp_data_array = []

        for data in data_array:
            temp_price = convert_price(data)
            max_price = max(data, temp_price)
            counter = 0
            while temp_price not in [0, 1] and temp_price > 0 and counter < 1000:
                temp_price = convert_price(temp_price)
                max_price = max(max_price, temp_price)
                counter += 1

            temp_data_array.append(max_price)
        output.append(temp_data_array)

    return jsonify(output)