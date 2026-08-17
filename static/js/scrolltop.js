const btnArriba = document.getElementById("btn-arriba");

const toggleBtnArriba = () => {
    if (window.scrollY > 400) {
        btnArriba.classList.add("visible");
    } else {
        btnArriba.classList.remove("visible");
    }
};

window.addEventListener("scroll", toggleBtnArriba, { passive: true });
toggleBtnArriba();

btnArriba.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
});
