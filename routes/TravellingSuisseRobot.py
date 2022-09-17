from flask import jsonify, request

from routes import app


# def get_plus_matrix(row, col, formatted_matrix):
#     vertical = []
#     horizontal = []

#     for row, _ in enumerate(formatted_matrix):
#         vertical.append(formatted_matrix[row][col])

#     for col, _ in enumerate(formatted_matrix[row]):
#         horizontal.append(formatted_matrix[row][col])

#     return (horizontal, vertical)


# def get_direction(
#     horizontal, vertical, target_char, row_index, col_index, current_direction
# ):
#     direction = ""
#     # print(horizontal, vertical, target_char)

#     if target_char in vertical:
#         target_index = vertical.index(target_char)

#         if target_index < row_index:
#             if current_direction in ["E", "W", "N"]:
#                 direction = "N"
#             else:
#                 direction = "S"
#         else:
#             direction = "S"

#     else:
#         target_index = horizontal.index(target_char)

#         if target_index > col_index:
#             if current_direction == ["N", "E", "S"]:
#                 direction = "R"
#             else:
#                 direction = "L"
#         else:
#             # raise Exception("impossble to be behind me")
#             pass
#     return direction


@app.route("/travelling-suisse-robot", methods=["POST"])
def travellingSuisseRobot():
    input_data = request.data.decode("UTF-8").replace("\\n", "")
    pattern = "CODEITSUISSE"
    matrix = input_data.splitlines()

    start_position = (0, 0)
    for index, row in enumerate(matrix):
        col = row.index("X") if "X" in row else -1

        if col != -1:
            start_position = (index, col)

    direction = ""
    plus_matrix = get_plus_matrix(
        start_position[0], start_position[1], matrix
    )
    visited_matrix = [
        [False for j in range(len(matrix[0]))]
        for i in range(len(matrix))
    ]
    horizontal = plus_matrix[0]
    vertical = plus_matrix[1]

    # Determine starting direction to find first letter 'C'
    if pattern[0] in vertical:
        s_index = vertical.index(pattern[0])
        x_index = vertical.index("X")

        if s_index > x_index:
            pass
        else:
            direction = "N"
    else:
        s_index = horizontal.index(pattern[0])
        x_index = horizontal.index("X")

        if s_index > x_index:
            direction = "R"
        else:
            direction = "L"

    print(f'sizeof matrix {len(matrix)} | {len(matrix[0])}')
    print(f'sizeof visited matrix {len(visited_matrix)} | {len(visited_matrix[0])}')

    moves = []

    traverse(
        start_position[0],
        start_position[1],
        pattern,
        "",
        0,
        matrix,
        moves,
        direction,
        visited_matrix,
    )

    print(moves)
    return jsonify("ok")


def traverse(
    row, col, pattern, temp_pattern, index, matrix, moves, direction, visited_matrix
):
    if (
        row < 0
        or col < 0
        or col == len(matrix[0])
        or row == len(matrix)
        or visited_matrix[row][col]
    ):
        return

    current_char = matrix[row][col]
    visited_matrix[row][col] = True
    print(f'currently at {row} | {col} | {current_char} | {temp_pattern}| {visited_matrix[row][col]}')

    if current_char == pattern[index]:
        print(f"yes - {current_char} | {pattern[index]}")
        temp_pattern += current_char
        moves.append("P")
        index += 1

    if pattern == temp_pattern:
        return

    if direction == "N":
        traverse(row - 1, col, pattern, temp_pattern, index, matrix, moves + ["S"], "N", visited_matrix)
        traverse(row, col + 1, pattern, temp_pattern, index, matrix, moves + ["R"], "E", visited_matrix)
        traverse(row, col - 1, pattern, temp_pattern, index, matrix, moves + ["L"], "W", visited_matrix)
    if direction == "E":
        traverse(row, col + 1, pattern, temp_pattern, index, matrix, moves + ["S"], "E", visited_matrix)
        traverse(row + 1, col, pattern, temp_pattern, index, matrix, moves + ["R"], "S", visited_matrix)
        traverse(row - 1, col, pattern, temp_pattern, index, matrix, moves + ["L"], "N", visited_matrix)
    if direction == "W":
        traverse(row, col - 1, pattern, temp_pattern, index, matrix, moves + ["S"], "W", visited_matrix)
        traverse(row + 1, col, pattern, temp_pattern, index, matrix, moves + ["L"], "S", visited_matrix)
        traverse(row - 1, col, pattern, temp_pattern, index, matrix, moves + ["R"], "N", visited_matrix)
    if direction == "S":
        traverse(row - 1, col, pattern, temp_pattern, index, matrix, moves + ["S"], "S", visited_matrix)
        traverse(row, col + 1, pattern, temp_pattern, index, matrix, moves + ["L"], "E", visited_matrix)
        traverse(row, col - 1, pattern, temp_pattern, index, matrix, moves + ["R"], "W", visited_matrix)
    
    visited_matrix[row][col] = False


    # plus_matrix = get_plus_matrix(row, col, matrix)
    # horizontal = plus_matrix[0]
    # vertical = plus_matrix[1]

    # print(f"current {direction} - [{row}, {col}]")
    # next_direction = get_direction(
    #     horizontal, vertical, pattern[index], row, col, direction
    # )

    # if next_direction == "N":
    #     # STRAIGHT
    #     if row - 1 >= 0:
    #         traverse(
    #             row - 1,
    #             col,
    #             pattern,
    #             temp_pattern,
    #             index,
    #             matrix,
    #             [moves] + ["S"],
    #             next_direction,
    #         )
    #     # TURN LEFT
    #     if col - 1 >= 0:
    #         traverse(
    #             row - 1,
    #             col,
    #             pattern,
    #             temp_pattern,
    #             index,
    #             matrix,
    #             [moves] + ["L"],
    #             next_direction,
    #         )
    #     # TURN RIGHT
    #     if col + 1 < len(pattern[0]):
    #         traverse(
    #             row,
    #             col + 1,
    #             pattern,
    #             temp_pattern,
    #             index,
    #             matrix,
    #             [moves] + ["R"],
    #             next_direction,
    #         )
    # elif next_direction == "E":
    #     # STRAIGHT
    #     if col + 1 < len(pattern[0]):
    #         traverse(
    #             row,
    #             col + 1,
    #             pattern,
    #             temp_pattern,
    #             index,
    #             matrix,
    #             [moves] + ["S"],
    #             next_direction,
    #         )
    #     # TURN LEFT
    #     if row - 1 >= 0:
    #         traverse(
    #             row - 1,
    #             col,
    #             pattern,
    #             temp_pattern,
    #             index,
    #             matrix,
    #             [moves] + ["L"],
    #             next_direction,
    #         )
    #     # TURN RIGHT
    #     if row + 1 < len(pattern):
    #         traverse(
    #             row + 1,
    #             col,
    #             pattern,
    #             temp_pattern,
    #             index,
    #             matrix,
    #             [moves] + ["R"],
    #             next_direction,
    #         )
    # elif next_direction == "S":
    #     # STRAIGHT
    #     if row + 1 < len(pattern):
    #         traverse(
    #             row + 1,
    #             col,
    #             pattern,
    #             temp_pattern,
    #             index,
    #             matrix,
    #             [moves] + ["S"],
    #             next_direction,
    #         )
    #     # TURN RIGHT
    #     if col - 1 >= 0:
    #         traverse(
    #             row,
    #             col - 1,
    #             pattern,
    #             temp_pattern,
    #             index,
    #             matrix,
    #             [moves] + ["R"],
    #             next_direction,
    #         )
    #     # TURN LEFT
    #     if col + 1 < len(pattern[0]):
    #         traverse(
    #             row,
    #             col + 1,
    #             pattern,
    #             temp_pattern,
    #             index,
    #             matrix,
    #             [moves] + ["L"],
    #             next_direction,
    #         )
    # else:
    #     # TURN STRAIGHT
    #     if col - 1 >= 0:
    #         traverse(
    #             row,
    #             col - 1,
    #             pattern,
    #             temp_pattern,
    #             index,
    #             matrix,
    #             [moves] + ["S"],
    #             next_direction,
    #         )
    #     # TURN LEFT
    #     if row + 1 < len(pattern):
    #         traverse(
    #             row + 1,
    #             col,
    #             pattern,
    #             temp_pattern,
    #             index,
    #             matrix,
    #             [moves] + ["L"],
    #             next_direction,
    #         )
    #     # TURN RIGHT
    #     if col + 1 < len(pattern[0]):
    #         traverse(
    #             row,
    #             col + 1,
    #             pattern,
    #             temp_pattern,
    #             index,
    #             matrix,
    #             [moves] + ["R"],
    #             next_direction,
    #         )
