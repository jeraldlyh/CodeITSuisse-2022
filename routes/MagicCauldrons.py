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
    print(part1_input)
    part2_input = test["part2"]
    print(part2_input)
    part3_input = test["part3"]
    print(part3_input)
    part4_input = test["part4"]
    print(part4_input)
    return ({"part1": part1_input, "part2": part2_input, "part3": part3_input, "part4_input": part4_input})
    