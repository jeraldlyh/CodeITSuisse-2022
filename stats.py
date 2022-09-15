from collections import OrderedDict

import pandas as pd


def to_cumulative(stream: list):
    df = get_cumulative_db(stream)
    df = df[[
        'timestamp', 'ticker', 'cumulative quantity', 'cumulative nominal'
    ]]
    # list of list of values, where valuesList[0][0] returns the first value of the first column of first row
    ans = format_string_cumulative(df)
    return ans


def format_string_cumulative(df: pd.DataFrame):
    valuesList = df.values.tolist()
    mapT = OrderedDict()

    for row in valuesList:
        newValue = ','.join(str(val) for val in row[1:])
        if (row[0] in mapT.keys()):
            currString = mapT[row[0]]
            mapT[row[0]] = currString + ',' + newValue
        else:
            mapT[row[0]] = newValue

    return [key + "," + value for key, value in mapT.items()]


def get_cumulative_db(stream: list):
    arr = [sub.split(",") for sub in stream]
    df = pd.DataFrame(arr,
                      columns=['timestamp', 'ticker', 'quantity', 'price'])
    df.sort_values(by=['timestamp', 'ticker'], inplace=True)
    df[['quantity', 'price']] = df[['quantity', 'price']].apply(pd.to_numeric)
    df['nominal'] = df['quantity'] * df['price']
    df['cumulative quantity'] = df.groupby('ticker')['quantity'].cumsum()
    df['cumulative nominal'] = df.groupby('ticker')['nominal'].cumsum()
    return df


def to_cumulative_delayed(stream: list, quantity_block: int):
    df = get_cumulative_db(stream)
    df.sort_values(by=['ticker', 'timestamp'], inplace=True)

    values_list = df.values.tolist()
    output = []
    temp_quantity_block = 0  # Keeps track of quantity
    current_ticker = values_list[0][1]
    quotient = 1

    for row in values_list:
        price = row[3]
        timestamp = row[0]
        ticker_name = row[1]
        cumulative_nominal = row[6]
        ticker_quantity = row[2]

        # Dispose previous ticker values and reset quotient
        if ticker_name != current_ticker:
            current_ticker = ticker_name
            quotient = 1
            temp_quantity_block = 0

        temp_quantity_block += ticker_quantity  # Assign cumulative quantity

        while temp_quantity_block >= quantity_block:
            excessive_tickers = temp_quantity_block % quantity_block
            temp_quantity_block = excessive_tickers

            current_quantity = quantity_block * quotient

            output.append(
                timestamp + ',' + ticker_name + ',' + str(current_quantity) +
                ',' +
                str(round(cumulative_nominal -
                          (excessive_tickers * price), 1)))
            quotient += 1
    output.sort(key=lambda o: o[:5])
    return output
