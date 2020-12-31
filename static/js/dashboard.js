// Hides alert after 5 seconds
window.onload = () => {
    const alertbox = document.querySelector("#alert-header")
    if (alertbox)
        setTimeout(() => alertbox.style.display = "none", 5000)
}