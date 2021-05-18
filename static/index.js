const orange = "rgb(255, 165, 0)"
const green  = "rgb(0, 128, 0)"
const red = "rgb(255, 0, 0)"
const yellow = "rgb(255, 255, 0)"
const white = "rgb(255, 255, 255)"
const blue = "rgb(0, 0, 255)"
const colors = [orange, green, red, yellow, white, blue];

var score = 0;
var doubledScore = 0;
const score_button = document.getElementById("increase-score");
const scoreValue_input = document.getElementById("score-value");
const displayScore_span = document.getElementById("display-score");
const button1_button = document.querySelector("#button1");
const button2_button = document.querySelector("#button2");
const button3_button = document.querySelector("#button3");
const button4_button = document.querySelector("#button4");
const button5_button = document.querySelector("#button5");
const button6_button = document.querySelector("#button6");
const button7_button = document.querySelector("#button7");
const button8_button = document.querySelector("#button8");
const button9_button = document.querySelector("#button9");
const faceText_h3 = document.getElementById("face-text");
const resetCube_button = document.querySelector(".reset-cube")
const solveCube_button = document.querySelector(".solve-cube")
var buttons = [[button1_button, button2_button, button3_button], 
                [button4_button, button5_button, button6_button], 
                [button7_button, button8_button, button9_button]];

const changeFace_button = document.querySelector(".change-face");
var cubeData = {"Front Face": [[orange, orange, orange],[orange, blue, orange],[orange, orange, orange]], 
                "Left Face": [[orange, orange, orange],[orange, orange, orange],[orange, orange, orange]], 
                "Right Face": [[orange, orange, orange],[orange, red, orange],[orange, orange, orange]], 
                "Back Face": [[orange, orange, orange],[orange, green, orange],[orange, orange, orange]], 
                "Up Face": [[orange, orange, orange],[orange, yellow, orange],[orange, orange, orange]], 
                "Down Face": [[orange, orange, orange],[orange, white, orange],[orange, orange, orange]]}

var newData = ""
solveCube_button.addEventListener("click", function(){

    fetch("http://127.0.0.1:5000/test", {
        method: "POST",
        body: JSON.stringify(cubeData),
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(function(response){
        console.log(response.json())
    })
})

resetCube_button.addEventListener("click", function(){
    // resets entire cube
    for (i = 0; i < Object.keys(cubeData).length; i ++) {
        // get data for face
        const currentFaceData = cubeData[Object.keys(cubeData)[i]]
        for (k = 0; k < currentFaceData.length; k++) {
            const currentRow = currentFaceData[k]
            for (j = 0; j < currentRow.length; j++) {
                if (!(k == 1 && j == 1)) {
                    // reset cube to orange
                    cubeData[Object.keys(cubeData)[i]][k][j] = orange
                }
            }
        }
    }
    const currentFace = faceText_h3.innerHTML
    // update UI for current face
    updateCube(currentFace)
})

function updateCube(face) {
    const data = cubeData[face]
    console.log(data)
    for (i = 0; i < data.length; i++) {
        const currentRow = data[i]
        for (k = 0; k < currentRow.length; k++) {
            const currentCube = currentRow[k]
            buttons[i][k].style.backgroundColor = currentCube;
        }
    }
}

function getNextFace(currentFace) {
    faces = Object.keys(cubeData)
    for (i = 0; i < faces.length; i++) {
        if (faces[i] === currentFace) {
            return faces[(i+1) % 6]
        }
    }
}

changeFace_button.addEventListener("click", function(){
    const currentFace = faceText_h3.innerHTML
    const toDisplay = getNextFace(currentFace)
    // updates face text
    faceText_h3.innerHTML = toDisplay
    // updates UI to show data for current face
    updateCube(toDisplay)
})

function getNextColor(currentColor) {
    for (i = 0; i < colors.length; i++) {
        if (colors[i] === currentColor) {
            return colors[(i+1) % 6]
        }
    }
};

score_button.addEventListener("click", function(){
    score++;
    displayScore_span.innerHTML = score;
    scoreValue_input.value = score;
});

button1_button.addEventListener("click", function(){
    const style = getComputedStyle(button1_button);
    var currentColor = style.backgroundColor;

    var nextColor = getNextColor(currentColor);

    // change UI to reflect color change
    button1_button.style.backgroundColor = nextColor;
    // change cubeData to reflect color change
    const currentFace = faceText_h3.innerHTML
    cubeData[currentFace][0][0] = nextColor
});

button2_button.addEventListener("click", function(){
    const style = getComputedStyle(button2_button);
    var currentColor = style.backgroundColor;

    var nextColor = getNextColor(currentColor);
    button2_button.style.backgroundColor = nextColor;

    const currentFace = faceText_h3.innerHTML
    cubeData[currentFace][0][1] = nextColor
});

button3_button.addEventListener("click", function(){
    const style = getComputedStyle(button3_button);
    var currentColor = style.backgroundColor;

    var nextColor = getNextColor(currentColor);
    button3_button.style.backgroundColor = nextColor;

    const currentFace = faceText_h3.innerHTML
    cubeData[currentFace][0][2] = nextColor
});

button4_button.addEventListener("click", function(){
    const style = getComputedStyle(button4_button);
    var currentColor = style.backgroundColor;

    var nextColor = getNextColor(currentColor);
    button4_button.style.backgroundColor = nextColor;

    const currentFace = faceText_h3.innerHTML
    cubeData[currentFace][1][0] = nextColor
});

// button5_button.addEventListener("click", function(){
//     const style = getComputedStyle(button5_button);
//     var currentColor = style.backgroundColor;

//     var nextColor = getNextColor(currentColor);
//     button5_button.style.backgroundColor = nextColor;

//     const currentFace = faceText_h3.innerHTML
//     cubeData[currentFace][1][1] = nextColor
// });

button6_button.addEventListener("click", function(){
    const style = getComputedStyle(button6_button);
    var currentColor = style.backgroundColor;

    var nextColor = getNextColor(currentColor);
    button6_button.style.backgroundColor = nextColor;

    const currentFace = faceText_h3.innerHTML
    cubeData[currentFace][1][2] = nextColor
});

button7_button.addEventListener("click", function(){
    const style = getComputedStyle(button7_button);
    var currentColor = style.backgroundColor;

    var nextColor = getNextColor(currentColor);
    button7_button.style.backgroundColor = nextColor;

    const currentFace = faceText_h3.innerHTML
    cubeData[currentFace][2][0] = nextColor
});

button8_button.addEventListener("click", function(){
    const style = getComputedStyle(button8_button);
    var currentColor = style.backgroundColor;

    var nextColor = getNextColor(currentColor);
    button8_button.style.backgroundColor = nextColor;

    const currentFace = faceText_h3.innerHTML
    cubeData[currentFace][2][1] = nextColor
});

button9_button.addEventListener("click", function(){
    const style = getComputedStyle(button9_button);
    var currentColor = style.backgroundColor;

    var nextColor = getNextColor(currentColor);
    button9_button.style.backgroundColor = nextColor;

    const currentFace = faceText_h3.innerHTML
    cubeData[currentFace][2][2] = nextColor
});

function positionButtons() {
    var startY = 130;
    var startX = 180;

    for (i = 0; i < buttons.length; i++) {
        const currentRow = buttons[i]
        for (k = 0; k < currentRow.length; k++) {
            const currentButton = currentRow[k]
            currentButton.style.top = startX + "px";
            currentButton.style.left = startY + "px";
            startY += 80;
        }
        startY = 130;
        startX += 80;
    }
}

positionButtons()
updateCube("Front Face")