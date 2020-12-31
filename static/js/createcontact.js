let contact = {}
const btnAddContact = document.querySelector("#btn-addcontact")
const btnAddHistory = document.querySelector("#btn-addhistory")
const btnCancel = document.querySelectorAll(".btn-dark")
const tbody = document.querySelector("tbody")

btnAddContact.onclick = () => displayModal("#addcontact-form")
btnAddHistory.onclick = () => displayModal("#addhistory-form")

// Open modal
function displayModal(target) {
    const modal = document.querySelector(target)
    modal.parentElement.style.display = "block"
    modal.children[0].children[0].children[1].focus()
}

// Close current modal
btnCancel.forEach(element => {
    element.onclick = el => {
        el.preventDefault()
        el.target.parentElement.reset()
        el.target.parentElement.parentElement.parentElement.style.display = "none"

    }
})


// Select contact info
tbody.onclick = ev => {
    contact["contact_id"] = ev.target.parentElement.children[0].innerText
    contact["name"] = ev.target.parentElement.children[1].innerText
    contact["lastname"] = ev.target.parentElement.children[2].innerText

    document.querySelector('input[name="contact-id"]').value = contact["contact_id"]
    document.querySelector("#selected-contact").innerText = `${contact["name"]} ${contact["lastname"]}`

    activeRow(ev.target.parentElement)
}

// Changes UI selected row that was clicked by the user
function activeRow(target) {
    rows = tbody.children

    // For each row of the table
    for (row of rows) {
        // If there is an option selected already, removes it
        if (row.classList.contains("table-active"))
            row.classList.remove("table-active")
    }

    // Selects the current table row
    target.setAttribute("class", "table-active")
}