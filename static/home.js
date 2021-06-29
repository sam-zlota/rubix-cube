

const e = React.createElement
const orange = "rgb(255, 165, 0)"
const green = "rgb(0, 128, 0)"
const red = "rgb(255, 0, 0)"
const yellow = "rgb(255, 255, 0)"
const white = "rgb(255, 255, 255)"
const blue = "rgb(0, 0, 255)"




const Button = ({ face, faceCube, color, changeColor }) => {
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
                return e(Button, { key: face + " " + element, face: face, faceCube: element, color: faceData[element], changeColor: change })
            }))
    )
}

const Grid = ({  }) => {
    const [cube, setCube] = React.useState(
        {
            "Left": {"TL": orange, "TT": orange, "TR": orange, "ML": orange, "MM": orange, "MR": orange, "DL": orange, "DD": orange, "DR": orange},
            "Front": {"TL": orange, "TT": orange, "TR": orange, "ML": orange, "MM": blue, "MR": orange, "DL": orange, "DD": orange, "DR": orange}, 
            "Up": {"TL": orange, "TT": orange, "TR": orange, "ML": orange, "MM": yellow, "MR": orange, "DL": orange, "DD": orange, "DR": orange},
            "Down": {"TL": orange, "TT": orange, "TR": orange, "ML": orange, "MM": white, "MR": orange, "DL": orange, "DD": orange, "DR": orange},
            "Right": {"TL": orange, "TT": orange, "TR": orange, "ML": orange, "MM": red, "MR": orange, "DL": orange, "DD": orange, "DR": orange},
            "Back": {"TL": orange, "TT": orange, "TR": orange, "ML": orange, "MM": green, "MR": orange, "DL": orange, "DD": orange, "DR": orange}
        })

    const changeColor = (face, faceCube) => {
        function getNextColor(currentColor) {
            const colors = [orange, green, red, yellow, white, blue];
        
            for (let i = 0; i < colors.length; i++) {
                if (colors[i] === currentColor) {
                    return colors[(i+1) % 6]
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

    return (
        e("div", { className: "input-container" },
            Object.keys(cube).map((element) => {
                return e(Face, { key: element, face: element, faceData: cube[element], change: changeColor })
            }))
    )
}

ReactDOM.render(
    e(Grid, {  }),
    document.getElementById("root")
)