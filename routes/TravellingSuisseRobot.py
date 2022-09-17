from flask import request

from routes import app


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
    plus_matrix = get_plus_matrix(start_position[0], start_position[1], matrix)
    visited_matrix = [
        [False for j in range(len(matrix[0]))] for i in range(len(matrix))
    ]
    horizontal = plus_matrix[0]
    vertical = plus_matrix[1]

    # Determine starting direction to find first letter 'C'
    if pattern[0] in vertical:
        c_index = vertical.index(pattern[0])
        x_index = vertical.index("X")

        if c_index > x_index:
            pass
        else:
            direction = "N"
    else:
        c_index = horizontal.index(pattern[0])
        x_index = horizontal.index("X")

        if c_index > x_index:
            direction = "E"
        else:
            direction = "W"

    # print(f"sizeof matrix {len(matrix)} | {len(matrix[0])}")
    # print(f"sizeof visited matrix {len(visited_matrix)} | {len(visited_matrix[0])}")

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

    return "".join(moves), 200, {"Content-Type": "text/plain;"}


def traverse(
    row, col, pattern, temp_pattern, index, matrix, moves, direction, visited_matrix
):
    if row < 0 or col < 0 or col == len(matrix[0]) or row == len(matrix):
        return

    current_char = matrix[row][col]

    if current_char == pattern[index]:
        temp_pattern += current_char
        moves.append("P")
        index += 1

    if pattern == temp_pattern:
        return

    plus_matrix = get_plus_matrix(row, col, matrix)
    horizontal = plus_matrix[0]
    vertical = plus_matrix[1]

    # print(horizontal)
    # print(vertical)
    # print(f"currently facing {direction} at {row} | {col} at {matrix[row][col]}")

    visited_matrix[row][col] = True
    next_coordinates = find_next_position(
        row, col, horizontal, vertical, pattern[index], visited_matrix, direction
    )
    next_row = next_coordinates[0]
    next_col = next_coordinates[1]
    # print(f"going to {next_row} | {next_col} with {matrix[next_row][next_col]} {moves}")
    next_direction = find_next_direction(direction, row, col, next_row, next_col)
    is_direction_changed = direction != next_direction

    # Need to traverse vertically
    if next_row != row:
        diff = abs(next_row - row)
        print(f"going vertically {diff} steps to {pattern[index]}")

        if is_direction_changed:
            moves.append("R" if next_direction == "S" else next_direction)
        for _ in range(diff):
            moves.append("S")

        traverse(
            next_row,
            col,
            pattern,
            temp_pattern,
            index,
            matrix,
            moves,
            next_direction,
            visited_matrix,
        )
    else:
        diff = abs(next_col - col)
        print(f"going horiztonally {diff} steps")
        if is_direction_changed:
            moves.append(map_direction(next_direction, direction))
        for _ in range(diff):
            moves.append("S")

        traverse(
            row,
            next_col,
            pattern,
            temp_pattern,
            index,
            matrix,
            moves,
            next_direction,
            visited_matrix,
        )


def map_direction(value, direction):
    if direction == "S":
        if value == "E":
            return "L"
        elif value == "W":
            return "R"
    elif direction == "N":
        if value == "E":
            return "R"
        elif value == "W":
            return "L"
    raise Exception("Something went wrong with map_direction()")


def find_next_direction(direction, row, col, next_row, next_col):
    if direction == "N":
        # Traverse vertically
        if next_row != row:
            if next_row < row:
                return "N"
            else:
                raise Exception("weird")
        if next_col != col:
            if next_col < col:
                return "W"
            else:
                return "E"
    elif direction == "S":
        if next_row != row:
            if next_row < row:
                raise Exception("weird")
            else:
                return "S"
        if next_col != col:
            if next_col < col:
                return "W"
            else:
                return "E"
    elif direction == "E":
        if next_row != row:
            if next_row < row:
                return "N"
            else:
                return "S"
        if next_col != col:
            if next_col < col:
                raise Exception("weird")
            else:
                return "E"
    else:
        if next_row != row:
            if next_row < row:
                return "N"
            else:
                return "S"
        if next_col != col:
            if next_col < col:
                return "W"
            else:
                raise Exception("weird")
    raise Exception(
        f"nothing returned at {row} | {col} going to {next_row} | {next_col} facing {direction}"
    )


def find_next_position(
    row, col, horizontal, vertical, target_char, visited_matrix, direction
):
    if target_char in horizontal:
        possible_indices = [i for i, x in enumerate(horizontal) if x == target_char]

        if direction == "W":
            possible_indices = possible_indices[::-1]

        first_possible_index = 0
        for index in possible_indices:
            if not visited_matrix[row][index]:
                first_possible_index = index
                break
        return row, first_possible_index

    possible_indices = [i for i, x in enumerate(vertical) if x == target_char]
    if direction == "S":
        possible_indices = possible_indices[::-1]

    first_possible_index = 0
    for index in possible_indices:
        if not visited_matrix[index][col]:
            first_possible_index = index
            break
    return first_possible_index, col


def get_plus_matrix(row, col, formatted_matrix):
    vertical = []
    horizontal = []

    for i in range(len(formatted_matrix)):
        vertical.append(formatted_matrix[i][col])

    for j in range(len(formatted_matrix[0])):
        horizontal.append(formatted_matrix[row][j])

    return (horizontal, vertical)
