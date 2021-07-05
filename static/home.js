const e = React.createElement
const orange = "rgb(255, 165, 0)"
const green = "rgb(0, 128, 0)"
const red = "rgb(255, 0, 0)"
const yellow = "rgb(255, 255, 0)"
const white = "rgb(255, 255, 255)"
const blue = "rgb(0, 0, 255)"

const CubeButton = ({ face, faceCube, color, changeColor }) => {
    return (
        e("button",
            {
                onClick: () => changeColor(face, faceCube),
                className: faceCube + " button",
                style: {
                    backgroundColor: color,
                    margin: "none",
                    border: "none",
                    width: "90%",
                    height: "90%",
                    borderRadius: "2px",
                    cursor: "pointer"
                }
            }, "")
    )
}

const Face = ({ face, faceData, change }) => {
    return (
        e("div", { className: "face-container " + face },
            Object.keys(faceData).map((element) => {
                return e(CubeButton, { key: face + " " + element, face: face, faceCube: element, color: faceData[element], changeColor: change })
            }))
    )
}

const Grid = ({ cube, changeColor }) => {
    return (
        e("div", { className: "input-container" },
            Object.keys(cube).map((element) => {
                return e(Face, { key: element, face: element, faceData: cube[element], change: changeColor })
            }))
    )
}


const Button = ({ name, action }) => {
    var color

    if (name === "Solve") {
        color = "green"
    }
    else if (name === "Reset") {
        color = "red"
    }
    else if (name === "Set Example") {
        color = "blue"
    }

    return (
        e("button", {
            className: "btn",
            style: { backgroundColor: color },
            onClick: () => action()
        }, name)
    )
}

const Direction = ({ content, changeState, idx, buttonState, isPrevActive, setDirectionActive }) => {

    // gets color for current direction state
    const getColor = () => {
        if (buttonState["active"]) {
            return "red"
        }
        else {
            return "green"
        }
    }

    const changeDirectionState = () => {
        // set direction state to active
        setDirectionActive(buttonState["key"])

        // change state of the cube
        changeState(idx)
    }

    // gets onClick function for current direction state
    const getOnClick = () => {

        var isValid = false

        // valid if button is either index 0 or the previous button is already active
        if (buttonState["key"] === 0) {
            isValid = true
        }
        else {
            // check to see if previous button is already active
            if (isPrevActive(buttonState["key"] - 1)) {
                isValid = true
            }
        }

        if (buttonState["active"]) {
            return () => console.log("button already active")
        }
        else if (!buttonState["active"] && isValid) {
            return () => changeDirectionState()
        }
        else {
            return () => console.log("not next button")
        }
        // NOTE: left off here
        // I want to be able to click ahead buttons but not go back
    }
    

    const directionKey = {
        23: "U",
        22: "D",
        3: "L",
        21: "R",
        5: "F",
        6: "B",
        7: "U'",
        20: "D'",
        9: "L'",
        10: "R'",
        11: "F'",
        12: "B'",
        15: "Y Rot",
        19: "Y Rot'",
        17: "X Rot",
        18: "X Rot'"
    }

    return (
        e("div", { 
            className: "direction",
            style: { cursor: "pointer", backgroundColor: getColor() },
            onClick: getOnClick() }, directionKey[content])
    )
}

const CubeOutput = ({ actions, changeState }) => {

    // maps actions into button states
    const setInitialState = () => {
        // convert actions to list of objects [{ key: int, active: boolean }]
        const buttonState = actions.map((element, idx) => {
            return { "key": idx, "active": false }
        })

        return buttonState
    }

    // states for each button
    const [buttonStates, setButtonStates] = React.useState(setInitialState())

    // returns true if given button is active and false if not
    const isPrevActive = (currentKey) => {
        return buttonStates[currentKey]["active"]
    }

    // sets the given button to active
    const setDirectionActive = (currentKey) => {
        setButtonStates(buttonStates.map(element => {
            if (element["key"] === currentKey) {
                return { "key": element["key"], "active": true }
            }
            else {
                return element
            }
        }))
    }

    return (
        e("div", { className: "output-container" },
            actions.map((element, idx) => {
                return e(Direction, { 
                    key: idx, 
                    content: element, 
                    changeState: changeState, 
                    idx: idx,
                    buttonState: buttonStates[idx],
                    isPrevActive: isPrevActive,
                    setDirectionActive: setDirectionActive })
            }))
    )
}

const CubeInput = () => {
    const resetCube = () => {
        return {
            "Left": { "TL": orange, "TT": orange, "TR": orange, "ML": orange, "MM": orange, "MR": orange, "DL": orange, "DD": orange, "DR": orange },
            "Front": { "TL": orange, "TT": orange, "TR": orange, "ML": orange, "MM": blue, "MR": orange, "DL": orange, "DD": orange, "DR": orange },
            "Up": { "TL": orange, "TT": orange, "TR": orange, "ML": orange, "MM": yellow, "MR": orange, "DL": orange, "DD": orange, "DR": orange },
            "Down": { "TL": orange, "TT": orange, "TR": orange, "ML": orange, "MM": white, "MR": orange, "DL": orange, "DD": orange, "DR": orange },
            "Right": { "TL": orange, "TT": orange, "TR": orange, "ML": orange, "MM": red, "MR": orange, "DL": orange, "DD": orange, "DR": orange },
            "Back": { "TL": orange, "TT": orange, "TR": orange, "ML": orange, "MM": green, "MR": orange, "DL": orange, "DD": orange, "DR": orange }
        }
    }

    const [cube, setCube] = React.useState(resetCube())
    const [solveActions, setSolveActions] = React.useState([])
    const [solveStates, setSolveStates] = React.useState([])
    const [solved, setSolved] = React.useState(false)

    const changeColor = (face, faceCube) => {
        function getNextColor(currentColor) {
            const colors = [orange, green, red, yellow, white, blue];

            for (let i = 0; i < colors.length; i++) {
                if (colors[i] === currentColor) {
                    return colors[(i + 1) % 6]
                }
            }
        };

        var newCube = {}

        Object.keys(cube).forEach(element => {
            var newFace = cube[element]

            if (element === face && faceCube !== "MM") {
                const currentColor = cube[face][faceCube]

                newFace[faceCube] = getNextColor(currentColor)
            }

            newCube[element] = newFace
        })
        setCube(newCube)
    }

    const solveCube = () => {
        fetch("http://127.0.0.1:5000/solve", {
            method: "POST",
            body: JSON.stringify(cube),
            headers: new Headers({
                "content-type": "application/json"
            })
        }).then((response) => response.json())
        .then((data) => {
            if (data["actions"] === "none" && data["states"] === "none") {
                 console.log("invalid cube inputed")
                 alert("Invalid cube inputed! Try again!")
            }
            else {
                setSolveActions(data["actions"])
                setSolveStates(data["states"])
                setSolved(true)
            }
        })
    }

    const onReset = () => {
        setSolved(false)

        setCube(resetCube())
    }

    const setExampleCube = () => {
        return {
            "Left": { "TL": red, "TT": blue, "TR": green, "ML": white, "MM": orange, "MR": red, "DL": green, "DD": green, "DR": white },
            "Front": { "TL": white, "TT": green, "TR": orange, "ML": green, "MM": blue, "MR": green, "DL": red, "DD": red, "DR": white },
            "Up": { "TL": green, "TT": red, "TR": yellow, "ML": red, "MM": yellow, "MR": white, "DL": orange, "DD": yellow, "DR": blue },
            "Down": { "TL": green, "TT": white, "TR": red, "ML": white, "MM": white, "MR": blue, "DL": yellow, "DD": blue, "DR": yellow },
            "Right": { "TL": white, "TT": blue, "TR": orange, "ML": orange, "MM": red, "MR": orange, "DL": blue, "DD": orange, "DR": red },
            "Back": { "TL": blue, "TT": yellow, "TR": yellow, "ML": yellow, "MM": green, "MR": orange, "DL": blue, "DD": yellow, "DR": orange }
        }
    }

    // changes cube to cube state of given action index
    const changeState = (idx) => {
        const currentState = solveStates[idx]

        const transformKey = {
            1: yellow,
            2: white,
            4: red,
            8: orange,
            16: green,
            32: blue
        }

        var newState = {}

        Object.keys(currentState).forEach(key => {
            var newFace = {}

            Object.keys(currentState[key]).forEach(faceKey => {
                newFace[faceKey] = transformKey[currentState[key][faceKey]]
            })

            newState[key] = newFace
        })
        console.log(newState)
        setCube(newState)
    }

    const isSolved = () => {
        if (solved) {
            return e(CubeOutput, { actions: solveActions, changeState: changeState })
        }
        else {
            return null
        }
    }

    return (
        e("div", { className: "cube-input" },
            e(Button, { name: "Solve", action: () => solveCube() }),
            e(Button, { name: "Reset", action: () => onReset() }),
            e(Button, { name: "Set Example", action: () => setCube(setExampleCube()) }),
            e("div", { className: "input-output" },
                e(Grid, { cube: cube, changeColor: changeColor }),
                isSolved()))
    )
}

ReactDOM.render(
    e(CubeInput, {}),
    document.getElementById("root")
)
