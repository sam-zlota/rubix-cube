from flask import Flask, redirect, url_for, render_template, request, make_response
import json
from solver import Solver
from model import Cube
import multiprocessing

app = Flask(__name__)

def do_solve(s):
    actions, states = s.solve()

    return actions, states

def transform_data(data):
    '''
    Transforms data from rgb to one letter string format
    '''
    transform_key = {
        "rgb(255, 165, 0)": 8,
        "rgb(0, 128, 0)": 16,
        "rgb(255, 0, 0)": 4,
        "rgb(255, 255, 0)": 1,
        "rgb(255, 255, 255)": 2,
        "rgb(0, 0, 255)": 32
    }
    face_key = {
        "Left": "Left Face",
        "Front": "Front Face",
        "Up": "Up Face",
        "Down": "Down Face",
        "Right": "Right Face",
        "Back": "Back Face"
    }

    # to contain mapped cube data
    new_data = {}

    for key in data.keys():
        # gets current cube face
        current_face = data[key]

        # to contain list of list of color number identifiers
        new_colors = []

        # to contain one row in face
        current_row = []

        for row_key in current_face.keys():

            current_row.append(transform_key[current_face[row_key]])

            if len(current_row) == 3:
                new_colors.append(current_row)
                current_row = []

        new_data[face_key[key]] = new_colors

    return new_data


def solve_cube(cube_data):
    # transform rgb into single letter strings
    transformed_data = transform_data(cube_data)
    print(f"Transformed data: {transformed_data}")

    # create cube and set its state
    cube = Cube()
    cube.set_state(transformed_data)

    # create solver and solve cube
    solver = Solver(cube)

    # actions, states = solver.solve()
    # print(f"Actions: {actions}")
    # return actions, states

    p = multiprocessing.Process(target=do_solve, args=(solver,))
    p.start()

    # Wait for 10 seconds or until process finishes
    p.join(2)

    # If thread is still active
    if p.is_alive():
        print("timeout after 3 seconds")

        # Terminate - may not work if process is stuck for good
        #p.terminate()
        # OR Kill - will work for sure, no chance for process to finish nicely however
        p.kill()

        p.join()

        return None, None
    else:
        return do_solve(solver)



@app.route("/")
def home():
    return render_template('home.html')

@app.route("/directions")
def direction():
    return render_template("directions.html")


@app.route("/solve", methods=["POST"])
def test():
    if request.method == "POST":
        # get inputed cube data from front end
        res = request.get_json()
        print(f"Original data: {res}")

        # gets actions and states from solving algorithm
        cube_actions, cube_states = solve_cube(res)

        if cube_actions is None and cube_states is None:
            print("return none")
            return json.dumps({"actions": "none", "states": "none"})
        else:
            cube_data = {"actions": cube_actions, "states": cube_states}

            return json.dumps(cube_data)


if __name__ == '__main__':
    # test_data = {"front": [["rgb(255, 165, 0)", "rgb(255, 165, 0)"], ["rgb(255, 165, 0)"]],
    # "left": [["rgb(255, 165, 0)", "rgb(255, 165, 0)"], ["rgb(255, 165, 0)"]]}
    app.run(debug=True)
