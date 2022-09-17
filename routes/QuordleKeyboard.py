from flask import jsonify, request

from routes import app

@app.route("/quordleKeyboard", methods=["POST"])
def quordle_keyboard():
    answers = request.get_json()["answers"]
    attempts = request.get_json()["attempts"]
    numbers = request.get_json()["numbers"]

    part1_ans, leftover = solve_part_1(answers, attempts)
    part2_ans = solve_part_2(part1_ans, leftover, numbers)

    return jsonify({"part1": part1_ans, "part2": part2_ans})

def get_char_index(c):
    return ord(c) - 65

def solve_part_1(answers, attempts):
    isGuessed = [False] * 26
    cToAns = {}
    isCompleted = {} # map each answer to whether its completed or not
    greyCount = {} # map each number to its grey count; update only once number is pressed AND both conds satisfied 

    for ans in answers:
        isCompleted[ans] = False
        for c in ans:
            if c in cToAns:
                cToAns[c].append(ans)
            else:
                cToAns[c] = [ans]
    
    for attempt in attempts:
        for c in attempt: # update isGuessed
            isGuessed[get_char_index(c)] = True
        for c in attempt:
            if c not in cToAns:
                if c not in greyCount:
                    greyCount[c] = 0
            # if c in cToAns => check if all answers that contain c are complete 
            # => if all complete set greyCount = 0 
            else:
                # update isCompleted 
                for ans in cToAns[c]:
                    if all_characters_guessed(ans, isGuessed):
                        isCompleted[ans] = True
                allAnsCompleted = True
                for ans in cToAns[c]:
                    if isCompleted[ans] == False:
                        allAnsCompleted = False
                if allAnsCompleted and c not in greyCount:
                    greyCount[c] = 0
        # update all greyCount at the end of each attempt
        for key,_ in greyCount.items():
            greyCount[key] += 1

    count = [0] * 26
    for key, value in greyCount.items():
        count[get_char_index(key)] += value
    
    ans = ""
    leftover = ""
    for i in range(26):
        if count[i] == 0:
            leftover+=(chr(i+65))
        else:
            ans += str(count[i])

    return ans, leftover

def all_characters_guessed(ans, isGuessed):
    output = True
    for c in ans:
        if isGuessed[get_char_index(c)] == False:
            output = False
    return output

def solve_part_2(part1_ans, leftover, numbers):
    output = ""
    fiveNumList = get_five_num_list(numbers)
    for listOfNums in fiveNumList:
        binRepr = []
        for num in listOfNums:
            if str(num) in part1_ans:
                binRepr.append(1)
            else:
                binRepr.append(0)
        val = get_value(binRepr)
        output+=chr(val+64)

    return output+leftover

def get_five_num_list(numbers):
    output = []
    count = 0
    tmp = []
    for num in numbers:
        tmp.append(num)
        count+=1
        if count == 5:
            output.append(tmp)
            count = 0
            tmp = []
    return output

def get_value(binRepr):
    return (2**4)*binRepr[0] + (2**3)*binRepr[1] + (2**2)*binRepr[2] + (2**1)*binRepr[3] + (2**0)*binRepr[4]