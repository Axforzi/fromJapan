const itemsCarrusel = document.querySelectorAll(".carrusel .item-carrusel");
const dotsContenedor = document.querySelector(".carrusel-dots");

let indiceActual = 0;
let intervalo = null;
const TIEMPO_AUTOPLAY = 10000;

const crearDots = () => {
    if (!dotsContenedor) return;
    itemsCarrusel.forEach((_, i) => {
        const dot = document.createElement("button");
        dot.className = "dot";
        dot.setAttribute("aria-label", `Ir al carrusel ${i + 1}`);
        dot.addEventListener("click", () => irA(i));
        dotsContenedor.appendChild(dot);
    });
};

const actualizarDots = () => {
    if (!dotsContenedor) return;
    const dots = dotsContenedor.querySelectorAll(".dot");
    dots.forEach((dot, i) => dot.classList.toggle("active", i === indiceActual));
};

const activarItem = (nuevo) => {
    itemsCarrusel.forEach((item, i) => item.classList.toggle("item-active", i === nuevo));
    indiceActual = nuevo;
    actualizarDots();
};

const siguiente = () => {
    activarItem((indiceActual + 1) % itemsCarrusel.length);
};

const anterior = () => {
    activarItem((indiceActual - 1 + itemsCarrusel.length) % itemsCarrusel.length);
};

const irA = (i) => {
    activarItem(i);
    reiniciarAutoplay();
};

const iniciarAutoplay = () => {
    if (intervalo) clearInterval(intervalo);
    intervalo = setInterval(siguiente, TIEMPO_AUTOPLAY);
};

const detenerAutoplay = () => {
    if (intervalo) clearInterval(intervalo);
    intervalo = null;
};

const reiniciarAutoplay = () => {
    detenerAutoplay();
    iniciarAutoplay();
};

const carrusel = document.querySelector(".carrusel");
if (carrusel) {
    carrusel.addEventListener("mouseenter", detenerAutoplay);
    carrusel.addEventListener("mouseleave", iniciarAutoplay);
}

crearDots();
activarItem(0);
iniciarAutoplay();