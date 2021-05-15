from flask import Flask, redirect, url_for, render_template, request, make_response
import json
from solver import Solver
from model import Cube

app = Flask(__name__)


def transform_data(data):
    '''
    Transforms data from rgb to one letter string format
    '''
    transform_key = {
        "rgb(255, 165, 0)": "o",
        "rgb(0, 128, 0)": "g",
        "rgb(255, 0, 0)": "r",
        "rgb(255, 255, 0)": "y",
        "rgb(255, 255, 255)": "w",
        "rgb(0, 0, 255)": "b"
    }
    new_data = {}

    for key in data.keys():
        current_face = data[key]

        new_colors = []
        for row in current_face:
            current_row = []
            for current in row:
                current_row.append(transform_key[current])

            new_colors.append(current_row)

        new_data[key] = new_colors

    return new_data


def solve_cube(cube_data):
    # transform rgb into single letter strings
    transformed_data = transform_data(cube_data)

    # create cube and set its state
    cube = Cube()
    cube.set_state(transformed_data)

    # create solver and solve cube
    solver = Solver(cube)
    print(cube)
    return ''


@app.route("/")
def home():
    return render_template('index.html')


def double_number(number):
    print('called double')
    return int(number) * 2


@app.route("/double", methods=["POST", "GET"])
def double():
    if request.method == "POST":
        number = request.form["number"]
        n = double_number(number)
        return str(n)
    else:
        return render_template("index.html")


@app.route("/test", methods=["POST"])
def test():
    if request.method == "POST":
        response_data = {"message": "json received"}
        res = request.get_json()
        solved_cube = solve_cube(res)
        return make_response(json.dumps(res), 200)


if __name__ == '__main__':
    # test_data = {"front": [["rgb(255, 165, 0)", "rgb(255, 165, 0)"], ["rgb(255, 165, 0)"]],
    # "left": [["rgb(255, 165, 0)", "rgb(255, 165, 0)"], ["rgb(255, 165, 0)"]]}
    app.run(debug=True)
