const e = React.createElement



const Button = ({ name }) => {
    return (
        e("button", 
        { onClick: () => console.log("hello"),
        className: name
     }, "Button")
    )
}

const Grid = ({ classes }) => {
    return (
        e("div", { className: "input-container" }, 
        classes.map((element, idx) => {
            return e(Button, { key: idx, name: element })
        }))
    )
}

ReactDOM.render(
    e(Grid, { classes: ["Left", "Front", "Top", "Down", "Right", "Back"] }),
    document.getElementById("root")
)