from collections import OrderedDict

import pandas as pd
from flask import jsonify, request

from routes import app


@app.route("/tickerStreamPart1", methods=["POST"])
def ticker_stream_part_one():
    input_data = request.get_json()["stream"]

    return jsonify({"output": to_cumulative(input_data)})


@app.route("/tickerStreamPart2", methods=["POST"])
def ticker_stream_part_two():
    input_data = request.get_json()["stream"]
    quantity_block = request.get_json()["quantityBlock"]

    return jsonify({"output": to_cumulative_delayed(input_data, quantity_block)})


def to_cumulative(stream: list):
    df = get_cumulative_db(stream)
    df = df[["timestamp", "ticker", "cumulative quantity", "cumulative nominal"]]
    output = format_string_cumulative(df)
    return output


def format_string_cumulative(df: pd.DataFrame):
    values_list = df.values.tolist()
    sorted_map = OrderedDict(OrderedDict())

    for row in values_list:
        timestamp = row[0]
        ticker_symbol = row[1]
        cumulative_quantity = str(row[2])
        cumulative_nominal = str(row[3])

        if timestamp not in sorted_map.keys():
            sorted_map[timestamp] = {
                ticker_symbol: [cumulative_quantity, cumulative_nominal]
            }
        else:
            timestamp_tickers = sorted_map[timestamp]
            timestamp_tickers[ticker_symbol] = [cumulative_quantity, cumulative_nominal]

    output = []
    for timestamp, timestamp_values in sorted_map.items():
        temp_ticker_data = []
        for ticker, ticker_info in timestamp_values.items():
            temp_ticker_data.append(f'{ticker},{",".join(ticker_info)}')

        output.append(f'{timestamp},{",".join(temp_ticker_data)}')

    return output


def get_cumulative_db(stream: list):
    arr = [sub.split(",") for sub in stream]
    df = pd.DataFrame(arr, columns=["timestamp", "ticker", "quantity", "price"])
    df.sort_values(by=["timestamp", "ticker"], inplace=True)
    df[["quantity", "price"]] = df[["quantity", "price"]].apply(pd.to_numeric)
    df["nominal"] = df["quantity"] * df["price"]
    df["cumulative quantity"] = df.groupby("ticker")["quantity"].cumsum()
    df["cumulative nominal"] = df.groupby("ticker")["nominal"].cumsum()
    return df


def to_cumulative_delayed(stream: list, quantity_block: int):
    df = get_cumulative_db(stream)
    df.sort_values(by=["ticker", "timestamp"], inplace=True)

    values_list = df.values.tolist()
    output = []
    temp_quantity_block = 0  # Keeps track of quantity
    current_ticker = values_list[0][1]

    for row in values_list:
        timestamp = row[0]
        ticker_name = row[1]
        ticker_quantity = row[2]
        price = row[3]
        cumulative_quantity = row[5]
        cumulative_nominal = row[6]

        # Dispose previous ticker values and reset quotient
        if ticker_name != current_ticker:
            current_ticker = ticker_name
            temp_quantity_block = 0

        temp_quantity_block += ticker_quantity  # Assign cumulative quantity
        multiples = temp_quantity_block // quantity_block

        # Report unique tickers based on the current timestamp instead of iterating over number of multiples
        if multiples != 0:
            excessive_tickers = temp_quantity_block % quantity_block
            current_quantity = cumulative_quantity - excessive_tickers

            output.append(
                timestamp
                + ","
                + ticker_name
                + ","
                + str(current_quantity)
                + ","
                + str(round(cumulative_nominal - (excessive_tickers * price), 1))
            )

        # Assign the remainder value
        temp_quantity_block = temp_quantity_block % quantity_block

    output.sort(key=lambda o: o[:5])
    return output
