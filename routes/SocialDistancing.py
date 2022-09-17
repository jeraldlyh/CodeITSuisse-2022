from flask import jsonify, request
from math import comb
from routes import app

@app.route("/social-distancing", methods=["POST"])
def social_distancing():
    venues_string = request.get_json()
    venues_list = parse_venues_strings(venues_string)
    output = []
    for venue in venues_list:
        numSolns = branch_and_prune(venue)
        if numSolns == 0:
            output.append("No Solution")
        else:
            output.append(numSolns)
    return jsonify(output)

def branch_and_prune(venue):
    height, width, numPeople = venue[1], venue[0], venue[2]

    possible_pos = {}
    for i in range(height):
        for j in range(width):
            possible_pos[(i, j)] = 0

    for coord in venue[3]:
        row = coord[0]
        col = coord[1]
        possible_pos[(row, col)] = 1
        possible_pos = fill_surrounding_squares(possible_pos, height, width, row, col)
        numPeople-=1

    numPosAvailable = 0
    for _,val in possible_pos.items():
        if val == 0:
            numPosAvailable+=1
    if (numPeople == 1):
        return numPosAvailable

    # return comb(numPosAvailable, numPeople)

    return recursive_assign(possible_pos, height, width, numPeople)

def recursive_assign(possible_pos, height, width, numPeople):
    if numPeople == 0:
        return 1 # possible assignment found

    if 0 not in possible_pos.values(): # no more possible assignments 
        return 0

    output = 0
    for pos, val in possible_pos:
        if val == 0: # if able to assign; assign it
            possible_pos[pos] = 1
            numPeople-=1
            possible_pos = fill_surrounding_squares(possible_pos, height, width, pos[0], pos[1])
            output += recursive_assign(possible_pos, height, width, numPeople)
            possible_pos[pos] = 0
            numPeople+=1
    return output

def fill_surrounding_squares(possible_pos, height, width, row, col):
    if row-1 >= 0 and col-1 >= 0: # top left
        possible_pos[(row-1, col-1)] = 1
    if row-1 >= 0 and col+1 < width: # top right
        possible_pos[(row-1,col+1)] = 1
    if row-1 >= 0: # top
        possible_pos[(row-1, col)] = 1 
    if col-1 >= 0: # left
        possible_pos[(row, col-1)] = 1 
    if col+1 < width: # right
        possible_pos[(row, col+1)] = 1
    if row+1 < height and col-1 >= 0: # bottom left
        possible_pos[(row+1, col-1)] = 1
    if row+1 < height and col+1 < width: # bottom right
        possible_pos[(row+1, col+1)] = 1
    if row+1 < height: # bottom
        possible_pos[(row+1, col)] = 1
    return possible_pos

def parse_venues_strings(venues_string):
    output = []
    for str in venues_string:
        strList = str.split(",")
        width = int(strList[0])
        height = int(strList[1])
        numVisitors = int(strList[2])
        occupiedList = strList[3:]
        ptr = 0
        occupied = []
        while ptr < len(occupiedList)-1:
            row = int(occupiedList[ptr])
            col = int(occupiedList[ptr+1])
            ptr+=2
            occupied.append((row, col))
        output.append([width, height, numVisitors, occupied])
    return output


# class State:
#     def __init__(self, board, numVisitors, domain, assignment):
#         self.board = board
#         self.numVisitors = numVisitors
#         self.domain = domain
#         self.assignment = assignment


# def printBoard(board, width, height):
#     boardList = []
#     for x in range(0, height):
#         row = []
#         for y in range(0, width):
#             row.append(board[(x, y)])
#         boardList.append(row)
#     for i in boardList:
#         print(i)


# # Create board
# # Input: "width, height, numberOfVisitors, occupiedSeats..."


# def getInitialState(input):
#     width = input[0]
#     height = input[1]
#     numVisitors = input[2]
#     occupiedCoords = set()
#     for i in range(3, len(input) - 1):
#         occupiedCoords.add((input[i], input[i + 1]))
#         i += 2

#     coordTuples = set()
#     for x in range(0, height):
#         for y in range(0, width):
#             coordTuples.add((x, y))
#     board = dict.fromkeys(coordTuples, ".")

#     for occupied in occupiedCoords:
#         board[occupied] = "V"
#     printBoard(board, width, height)
#     domain = getDomain(coordTuples, occupiedCoords)
#     initialState = State(board, numVisitors, domain, board.copy())
#     return initialState


# def getDomain(coordTuples, occupiedCoords):
#     domain = coordTuples - occupiedCoords
#     for occupied in occupiedCoords:
#         xChange = [-1, -1, -1, 0, 0, 1, 1, 1]
#         yChange = [1, 0, -1, 1, -1, 1, 0, -1]
#         for i in range(len(xChange)):
#             newCoord = (occupied[0] + xChange[i], occupied[1] + yChange[i])
#             if (newCoord in domain):
#                 domain.remove(newCoord)
#     return domain


# def updateDomain(currDomain, newPos):
#     domain = currDomain.copy()
#     domain.remove(newPos)
#     xChange = [-1, -1, -1, 0, 0, 1, 1, 1]
#     yChange = [1, 0, -1, 1, -1, 1, 0, -1]
#     if domain == None:
#         return None
#     for i in range(len(xChange)):
#         newCoord = (newPos[0] + xChange[i], newPos[1] + yChange[i])
#         if (newCoord in domain):
#             domain.remove(newCoord)
#     return domain


# def backtrack(state):
#     for pos in state.domain:
#         newDomain = updateDomain(state.domain.copy(), pos)
#         newNumVisitors = state.numVisitors - 1
#         newAssignment = state.assignment.copy()
#         newAssignment[pos] = "V"
#         if (newNumVisitors == 0):
#             return newAssignment
#         if (newDomain == None):
#             return False
#         newState = State(state.board, newNumVisitors, newDomain, newAssignment)
#         result = backtrack(newState)
#         if (result is not False):
#             return result
#     return False


# width = 3
# height = 4

# state = getInitialState([3, 4, 2, 2, 2])
# print("newly assigned:")
# printBoard(backtrack(state), 3, 4)

