from flask import jsonify, request

from routes import app


@app.route("/rubiks", methods=["POST"])
def rubiks():
    ops = request.get_json()["ops"] # string of operations to parse
    state = request.get_json()["state"] # dict of configuration of rubiks cube
    # print(type(ops), ops)
    #print(type(state), state)
    opsArr = parse_ops(ops)
    for op in opsArr:
        if op == "U":
            state = op_up_clockwise(state)
        elif op == "Ui":
            state = op_up_anticlockwise(state)
        elif op == "D":
            state = op_down_clockwise(state)
        elif op == "Di":
            state = op_down_anticlockwise(state)
        elif op == "F":
            state = op_front_clockwise(state)
        elif op == "Fi":
            state = op_front_anticlockwise(state)
        elif op == "B":
            state = op_back_clockwise(state)
        elif op == "Bi":
            state = op_back_anticlockwise(state)
        elif op == "R":
            state = op_right_clockwise(state)
        elif op == "Ri":
            state = op_right_anticlockwise(state)
        elif op == "L":
            state = op_left_clockwise(state)
        elif op == "Li":
            state = op_left_anticlockwise(state)
        else:
            pass

    return jsonify(state)

def parse_ops(ops): # parse string of operations passed in
    opsArr = []
    n = len(ops)
    start = 0
    next = 0
    while start < n:
        next = start+1
        if next < n and ops[next] == 'i':
            opsArr.append(ops[start:next+1])
            start+=2
        else:
            opsArr.append(ops[start])
            start+=1
    
    return opsArr

def rotate_anticlockwise(side):
    # return list(reversed(list(zip(*side))))
    new_matrix = []
    for i in range(len(side[0]), 0, -1):
        new_matrix.append(list(map(lambda x: x[i-1], side)))

    return new_matrix

def rotate_clockwise(side):
    # return list(zip(*side[::-1]))
    new_matrix = []
    for i in range(len(side[0])):
        li = list(map(lambda x: x[i], side))
        li.reverse()
        new_matrix.append(li)

    return new_matrix

# up
def op_up_clockwise(state):
    state["u"] = rotate_clockwise(state["u"])
    tfront = state["f"][0]
    tleft = state["l"][0]
    tback = state["b"][0]
    tright = state["r"][0]
    state["l"][0] = tfront
    state["b"][0] = tleft
    state["r"][0] = tback
    state["f"][0] = tright
    return state

def op_up_anticlockwise(state):
    state["u"] = rotate_anticlockwise(state["u"])
    tfront = state["f"][0]
    tleft = state["l"][0]
    tback = state["b"][0]
    tright = state["r"][0]
    state["l"][0] = tback
    state["b"][0] = tright
    state["r"][0] = tfront
    state["f"][0] = tleft
    return state

# bottom
def op_down_clockwise(state):
    state["d"] = rotate_clockwise(state["d"])
    tfront = state["f"][2]
    tleft = state["l"][2]
    tback = state["b"][2]
    tright = state["r"][2]
    state["l"][2] = tback
    state["b"][2] = tright
    state["r"][2] = tfront
    state["f"][2] = tleft
    return state

def op_down_anticlockwise(state):
    state["d"] = rotate_anticlockwise(state["d"])
    tfront = state["f"][2]
    tleft = state["l"][2]
    tback = state["b"][2]
    tright = state["r"][2]
    state["l"][2] = tfront
    state["b"][2] = tleft
    state["r"][2] = tback
    state["f"][2] = tright
    return state

# front 
def op_front_clockwise(state):
    state["f"] = rotate_clockwise(state["f"])
    tup = state["u"][2]
    tdown = state["d"][0]
    tright = [state["r"][2][0], state["r"][1][0], state["r"][0][0]]
    tleft = [state["l"][2][2], state["l"][1][2], state["l"][0][2]]
    state["u"][2] = tleft
    state["r"][0][0], state["r"][1][0], state["r"][2][0] = tup[0], tup[1], tup[2]
    state["d"][0] = tright
    state["l"][0][2], state["l"][1][2], state["l"][2][2] = tdown[0], tdown[1], tdown[2]
    return state

def op_front_anticlockwise(state):
    state["f"] = rotate_anticlockwise(state["f"])
    tup = state["u"][2]
    tdown = state["d"][0]
    tright = [state["r"][0][0], state["r"][1][0], state["r"][2][0]]
    tleft = [state["l"][0][2], state["l"][1][2], state["l"][2][2]]
    state["u"][2] = tright
    state["r"][0][0], state["r"][1][0], state["r"][2][0] = tdown[2], tdown[1], tdown[0]
    state["d"][0] = tleft
    state["l"][0][2], state["l"][1][2], state["l"][2][2] = tup[2], tup[1], tup[0]
    return state

# back
def op_back_clockwise(state):
    state["b"] = rotate_clockwise(state["b"])
    tup = state["u"][0]
    tdown = state["d"][2]
    tright = [state["r"][0][2], state["r"][1][2], state["r"][2][2]]
    tleft = [state["l"][0][0], state["l"][1][0], state["l"][2][0]]
    state["u"][0] = tright
    state["r"][0][2], state["r"][1][2], state["r"][2][2] = tdown[2], tdown[1], tdown[0]
    state["d"][2] = tleft
    state["l"][0][0], state["l"][1][0], state["l"][2][0] = tup[2], tup[1], tup[0]
    return state

def op_back_anticlockwise(state):
    state["b"] = rotate_anticlockwise(state["b"])
    tup = state["u"][0]
    tdown = state["d"][2]
    tright = [state["r"][2][2], state["r"][1][2], state["r"][0][2]]
    tleft = [state["l"][2][0], state["l"][1][0], state["l"][0][0]]
    state["u"][0] = tleft
    state["r"][0][2], state["r"][1][2], state["r"][2][2] = tup[0], tup[1], tup[2]
    state["d"][2] = tright
    state["l"][0][0], state["l"][1][0], state["l"][2][0] = tdown[0], tdown[1], tdown[2]
    return state

# right
def op_right_clockwise(state):
    state["r"] = rotate_clockwise(state["r"])
    tup = [state["u"][0][2], state["u"][1][2], state["u"][2][2]]
    tfront = [state["f"][0][2], state["f"][1][2], state["f"][2][2]]
    tdown = [state["d"][0][2], state["d"][1][2], state["d"][2][2]]
    tback = [state["b"][0][0], state["b"][1][0], state["b"][2][0]]
    state["u"][0][2], state["u"][1][2], state["u"][2][2] = tfront[0], tfront[1], tfront[2]
    state["f"][0][2], state["f"][1][2], state["f"][2][2] = tdown[0], tdown[1], tdown[2]
    state["d"][0][2], state["d"][1][2], state["d"][2][2] = tback[2], tback[1], tback[0]
    state["b"][0][0], state["b"][1][0], state["b"][2][0] = tup[2], tup[1], tup[0]
    return state

def op_right_anticlockwise(state):
    state["r"] = rotate_anticlockwise(state["r"])
    tup = [state["u"][0][2], state["u"][1][2], state["u"][2][2]]
    tfront = [state["f"][0][2], state["f"][1][2], state["f"][2][2]]
    tdown = [state["d"][0][2], state["d"][1][2], state["d"][2][2]]
    tback = [state["b"][0][0], state["b"][1][0], state["b"][2][0]]
    state["u"][0][2], state["u"][1][2], state["u"][2][2] = tback[2], tback[1], tback[0]
    state["f"][0][2], state["f"][1][2], state["f"][2][2] = tup[0], tup[1], tup[2]
    state["d"][0][2], state["d"][1][2], state["d"][2][2] = tfront[0], tfront[1], tfront[2]
    state["b"][0][0], state["b"][1][0], state["b"][2][0] = tdown[2], tdown[1], tdown[0]
    return state

# left
def op_left_anticlockwise(state):
    state["l"] = rotate_anticlockwise(state["l"])
    tup = [state["u"][0][0], state["u"][1][0], state["u"][2][0]]
    tfront = [state["f"][0][0], state["f"][1][0], state["f"][2][0]]
    tdown = [state["d"][0][0], state["d"][1][0], state["d"][2][0]]
    tback = [state["b"][0][2], state["b"][1][2], state["b"][2][2]]
    state["u"][0][0], state["u"][1][0], state["u"][2][0] = tfront[0], tfront[1], tfront[2]
    state["f"][0][0], state["f"][1][0], state["f"][2][0] = tdown[0], tdown[1], tdown[2]
    state["d"][0][0], state["d"][1][0], state["d"][2][0] = tback[2], tback[1], tback[0]
    state["b"][0][2], state["b"][1][2], state["b"][2][2] = tup[2], tup[1], tup[0]
    return state


def op_left_clockwise(state):
    state["l"] = rotate_clockwise(state["l"])
    tup = [state["u"][0][0], state["u"][1][0], state["u"][2][0]]
    tfront = [state["f"][0][0], state["f"][1][0], state["f"][2][0]]
    tdown = [state["d"][0][0], state["d"][1][0], state["d"][2][0]]
    tback = [state["b"][0][2], state["b"][1][2], state["b"][2][2]]
    state["u"][0][0], state["u"][1][0], state["u"][2][0] = tback[2], tback[1], tback[0]
    state["f"][0][0], state["f"][1][0], state["f"][2][0] = tup[0], tup[1], tup[2]
    state["d"][0][0], state["d"][1][0], state["d"][2][0] = tfront[0], tfront[1], tfront[2]
    state["b"][0][2], state["b"][1][2], state["b"][2][2] = tdown[2], tdown[1], tdown[0]
    return state