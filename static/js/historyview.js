const editbtns = document.querySelectorAll(".btn-sm")

editbtns.forEach(element => {
    element.onclick = ev => sendData(ev)
})

function sendData(ev) {
    const rowNode = ev.target.parentElement.parentElement.children

    const row = {
        historyid: rowNode[0].innerText,
        contactid: rowNode[1].innerText,
        name: rowNode[2].innerText,
        lastname: rowNode[3].innerText,
        subject: rowNode[4].innerText,
        followdate: rowNode[5].innerText
    }

    const xhr = new XMLHttpRequest()

    xhr.open("POST", "/historys", true)
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8")

    xhr.onload = function() {
        if (this.status == 200) {
            window.location.href = "/historys/viewtalks"
        }
    }

    xhr.send(JSON.stringify(row))
}