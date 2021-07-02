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

    return (
        e("button", {
            className: "btn",
            style: { backgroundColor: color },
            onClick: () => action()
        }, name)
    )
}

const Direction = ({ content }) => {
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
        e("div", { className: "direction" }, directionKey[content])
    )
}

const CubeOutput = ({ data }) => {
    return (
        e("div", { className: "output-container" },
            data.map((element, idx) => {
                return e(Direction, { key: idx, content: element })
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
        .then((data) => setSolveActions(data))
        .then(() => setSolved(true))
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

    const isSolved = () => {
        if (solved) {
            return e(CubeOutput, { data: solveActions })
        }
        else {
            return null
        }
    }

    return (
        e("div", { className: "cube-input" },
            e(Button, { name: "Solve", action: () => solveCube() }),
            e(Button, { name: "Reset", action: () => onReset() }),
            e("div", { className: "input-output" },
                e(Grid, { cube: cube, changeColor: changeColor }),
                isSolved()),
            e("button", { onClick: () => setCube(setExampleCube()) }, "set example"))
    )
}

ReactDOM.render(
    e(CubeInput, {}),
    document.getElementById("root")
)
