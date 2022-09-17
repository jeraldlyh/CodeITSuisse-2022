from flask import jsonify, request

from routes import app


@app.route("/magiccauldrons", methods=["POST"])
def magic_cauldrons():
    tests = request.get_json()
    ans = []
    for test in tests:
        ans.append(solve(test))
    return jsonify(ans)


def solve(test):
    part1_input = test["part1"]
    # print(part1_input)
    part1_ans = solve_part_1(part1_input)
    part2_input = test["part2"]
    part2_ans = solve_part_2(part2_input)
    part3_input = test["part3"]
    part3_ans = solve_part_3(part3_input)
    part4_input = test["part4"]
    part4_ans = solve_part_4(part4_input)
    return {
        "part1": part1_ans,
        "part2": part2_ans,
        "part3": part3_ans,
        "part4_input": part4_ans,
    }


def get_arithmetic_sum(a, d, n):
    return (n / 2) * (2 * a + (n - 1) * d)


def solve_part_1(flow_rate: int, time: int, row_number: int, col_number: int):
    total_volume = flow_rate * time
    full_volume = 100

    num_of_overflowed = total_volume / full_volume
    num_of_bowls = get_arithmetic_sum(1, 1, row_number)
    count = 1

    # [0] Full
    # [0] Empty
    # Caclulate

    if num_of_bowls <= num_of_overflowed:
        excess_bowls = num_of_bowls - num_of_overflowed

    cauldrons = {}

    while count < num_of_overflowed:

        count += 1

    volForCurrRow = max(0, total_volume - full_volume * (row_number))
    if volForCurrRow > 0:
        pass
