// messages.js

document.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
        document.querySelectorAll(".alert").forEach(alert => {
            alert.classList.add("auto-hide");
            setTimeout(() => {
                alert.remove(); // Elimina el mensaje del DOM después del fade out
            }, 500); // Tiempo extra para que la animación termine
        });
    }, 3000); // 3 segundos antes de que desaparezca
});
