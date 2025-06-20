// Funcion para confirmar el gaurdado de un dato
function confirmarGuardado() {
    return confirm("¿Estas seguro de que deseas guardar?");
}

// Funcion para confirmar si quiere el usuario cerrar sesion
function confirmarLogout() {
    if (confirm("¿Estas seguro de que deseas cerrar sesion?")) {
        window.location.href = logoutUrl;
    }
}
// Funcion para animacion de boton de carga
function mostrarCarga(form) {
    const boton = form.querySelector("button");
    const spinner = boton.querySelector(".spinner-border");
    const texto = boton.querySelector(".texto-boton");
    if (spinner && texto) {
        spinner.classList.remove("d-none");
        texto.textContent = "Cargando...";
    }
}