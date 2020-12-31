const urgencies = loadUrgency()

// Load urgency data on profile page
for (const type in urgencies) {
    // Sets radio button accordingly to loaded urgencies
    if (urgencies[type][1] == 'hours')
        document.querySelector(`#${type}-hours-check`).checked = true

    // Loads values to inputs
    document.querySelector(`#${type}-input`).value = urgencies[type][0]

}

const btnSetUrgency = document.querySelector("[name='change-urgency']")

// Issues setUrgency with form data
btnSetUrgency.onclick = function(ev) {
    const warningNum = document.querySelector("#warning-input").value
    const warningDatetime = getRadioValue(document.getElementsByName("warning-radio"))

    const dangerNum = document.querySelector("#danger-input").value
    const dangerDatetime = getRadioValue(document.getElementsByName("danger-radio"))

    const urgency = {
        warning: [warningNum, warningDatetime],
        danger: [dangerNum, dangerDatetime]
    }

    setUrgency(urgency)
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

// Returns the value of a radio group
function getRadioValue(radioGroup) {
    for (const radio of radioGroup) {
        if (radio.checked)
            return radio.value
    }
}

// Changes the time of urgency based on form values
function setUrgency(urgency) {
    try {
        localStorage.setItem("fp_urgency_array", JSON.stringify(urgency))
        return true
    } catch (error) {
        console.log(error)
        return false
    }
}