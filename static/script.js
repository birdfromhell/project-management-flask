function toggleActive(elementId) {
    var statusElement = document.getElementById(elementId);

    if (statusElement.innerHTML === "Activo") {
        statusElement.innerHTML = "Inactivo";
        statusElement.classList.remove("active");
        statusElement.classList.add("inactive");
    } else {
        statusElement.innerHTML = "Activo";
        statusElement.classList.remove("inactive");
        statusElement.classList.add("active");
    }
}
