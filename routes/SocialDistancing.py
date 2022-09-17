
class State:
    def __init__(self, board, numVisitors, domain, assignment):
        self.board = board
        self.numVisitors = numVisitors
        self.domain = domain
        self.assignment = assignment


def printBoard(board, width, height):
    boardList = []
    for x in range(0, height):
        row = []
        for y in range(0, width):
            row.append(board[(x, y)])
        boardList.append(row)
    for i in boardList:
        print(i)


# Create board
# Input: "width, height, numberOfVisitors, occupiedSeats..."


def getInitialState(input):
    width = input[0]
    height = input[1]
    numVisitors = input[2]
    occupiedCoords = set()
    for i in range(3, len(input) - 1):
        occupiedCoords.add((input[i], input[i + 1]))
        i += 2

    coordTuples = set()
    for x in range(0, height):
        for y in range(0, width):
            coordTuples.add((x, y))
    board = dict.fromkeys(coordTuples, ".")

    for occupied in occupiedCoords:
        board[occupied] = "V"
    printBoard(board, width, height)
    domain = getDomain(coordTuples, occupiedCoords)
    initialState = State(board, numVisitors, domain, board.copy())
    return initialState


def getDomain(coordTuples, occupiedCoords):
    domain = coordTuples - occupiedCoords
    for occupied in occupiedCoords:
        xChange = [-1, -1, -1, 0, 0, 1, 1, 1]
        yChange = [1, 0, -1, 1, -1, 1, 0, -1]
        for i in range(len(xChange)):
            newCoord = (occupied[0] + xChange[i], occupied[1] + yChange[i])
            if (newCoord in domain):
                domain.remove(newCoord)
    return domain


def updateDomain(currDomain, newPos):
    domain = currDomain.copy()
    domain.remove(newPos)
    xChange = [-1, -1, -1, 0, 0, 1, 1, 1]
    yChange = [1, 0, -1, 1, -1, 1, 0, -1]
    if domain == None:
        return None
    for i in range(len(xChange)):
        newCoord = (newPos[0] + xChange[i], newPos[1] + yChange[i])
        if (newCoord in domain):
            domain.remove(newCoord)
    return domain


def backtrack(state):
    for pos in state.domain:
        newDomain = updateDomain(state.domain.copy(), pos)
        newNumVisitors = state.numVisitors - 1
        newAssignment = state.assignment.copy()
        newAssignment[pos] = "V"
        if (newNumVisitors == 0):
            return newAssignment
        if (newDomain == None):
            return False
        newState = State(state.board, newNumVisitors, newDomain, newAssignment)
        result = backtrack(newState)
        if (result is not False):
            return result
    return False


width = 3
height = 4

state = getInitialState([3, 4, 2, 2, 2])
print("newly assigned:")
printBoard(backtrack(state), 3, 4)
