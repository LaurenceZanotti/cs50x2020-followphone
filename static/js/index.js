const menu = document.querySelector(".dropdown-menu")
const getStartedBtn = document.querySelector("#btn-get-started")
const cancelBtn = document.querySelectorAll(".btn-dark")
const modalbg = document.querySelectorAll(".modal-background")

// Menu items handler
menu.onclick = ev => {
    const href = ev.target.getAttribute('href')

    // Display modal
    const modal = document.querySelector(href)
    modal.parentElement.style.display = "block"

    // Focus first form input
    ev.preventDefault()
    modal.children[0].children[0].children[1].focus()
}

// Get started button
getStartedBtn.onclick = ev => {
    const modal = document.querySelector("#register-form")

    // Diplay register modal
    modal.parentElement.style.display = "block"

    // Focus first form input
    ev.preventDefault()
    modal.children[0].children[0].children[1].focus()
}


// Add close modal event to all cancel buttons
cancelBtn.forEach(element => {
    element.onclick = ev => closeModals(ev)
})

// Close index modals
function closeModals(ev) {
    ev.preventDefault() // Prevent form submit

    const modals = document.querySelectorAll(".modal-background")
    const forms = document.querySelectorAll("form")

    for (modal of modals)
        modal.style.display = "none"

    for (form of forms)
        form.reset()
}

// Hides alert after 5 seconds
window.onload = () => {
    const alertbox = document.querySelector("#alert-header")
    if (alertbox)
        setTimeout(() => alertbox.style.display = "none", 5000)
}