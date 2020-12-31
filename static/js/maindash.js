// Date difference to emit a warning or danger
const urgencies = loadUrgency()

const warningDate = dayjs().subtract(urgencies.warning[0], urgencies.warning[1])
const dangerDate = dayjs().subtract(urgencies.danger[0], urgencies.danger[1])

const rows = document.querySelectorAll("tbody > tr")

// Sets the values of the legend labels
document.querySelector("#warning-label").innerText = `${urgencies.warning[0]} ${urgencies.warning[1]}`
document.querySelector("#danger-label").innerText = `${urgencies.danger[0]} ${urgencies.danger[1]}`

// For each row, compute and set style of the row
for (const row of rows) {
    const state = getRowState(row)

    if (state != null || state != undefined)
        row.classList.add(`table-${state}`)

    // console.log(row.children[2].innerText, state)
}

// Returns if a row must be styled with warning, danger or info
function getRowState(row) {
    // Get the follow up date and time
    let followup = row.children[5].innerText

    // Skip to next row if there is None
    if (followup === "None")
        return null
    // Parses to dayjs object
    else
        followup = dayjs(followup, 'YYYY-MM-DD HH:mm')

    // Returns bootstrap style for the row based on its followup date relative to current date
    if (followup.isBefore(dangerDate))
        return 'danger'
    else if (followup.isBefore(warningDate))
        return 'warning'
    else if (followup.isSame(dayjs(), 'days'))
        return 'info'
    else
        return undefined
}

// Loads urgency intervals for "Most urgent historys" table
function loadUrgency() {
    // If there's no stored time of urgency
    if (!localStorage.getItem("fp_urgency_array")) {
        // Set default urgency
        const urgency = {
            warning: [1, "days"],
            danger: [3, "days"]
        }

        localStorage.setItem("fp_urgency_array", JSON.stringify(urgency))
        return JSON.parse(localStorage.getItem("fp_urgency_array"))
    }
    // Returns urgency array for warning and danger styles
    else {
        return JSON.parse(localStorage.getItem("fp_urgency_array"))
    }
}