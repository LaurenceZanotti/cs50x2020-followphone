const btnTalk = document.querySelector("#btn-addtalk")
const btnClose = document.querySelector(".btn-dark")


// Display modal
btnTalk.onclick = ev => {
    const modal = document.querySelector(".modal-background")
    modal.children[0].children[0].children[1].children[0].focus()
    modal.style.display = "block"
}

// Close modal
btnClose.onclick = ev => {
    ev.preventDefault()
    ev.target.parentElement.reset()
    document.querySelector(".modal-background").style.display = "none"
}