const itemsCarrusel = document.querySelectorAll(".carrusel .item-carrusel");
itemsCarrusel[0].classList.toggle("item-active");

const siguiente = () => {
    try {
        let encontrado = false;
        itemsCarrusel.forEach((item) => {

            //ACTIVAR PRIMERO EN CASO DE ESTAR EN EL ULTIMO | BUCLE
            if(itemsCarrusel[itemsCarrusel.length -1].classList.contains("item-active") && item.classList.contains("item-active")){
                    itemsCarrusel[itemsCarrusel.length - 1].classList.toggle("item-active");
                    itemsCarrusel[0].classList.toggle("item-active");
            }

            //ACTIVAR SIGUIENTE
            if (encontrado){
                    item.classList.toggle("item-active");
                    throw BreakException;
            }

            //ENCONTRAR PREVIAMENTE ACTIVADO
            else if(item.classList.contains("item-active")){
                item.classList.toggle("item-active");
                encontrado = true;
            } 
        });   
    } catch (err) {
    }
};

const anterior = () => {
    try {
        let encontrado = false;
        let number = -1;
        itemsCarrusel.forEach((item) => {
            //ACTIVAR PRIMERO EN CASO DE ESTAR EN EL ULTIMO | BUCLE
            if(itemsCarrusel[0].classList.contains("item-active") && item.classList.contains("item-active")){
                    itemsCarrusel[0].classList.toggle("item-active");
                    itemsCarrusel[itemsCarrusel.length - 1].classList.toggle("item-active");
                    throw BreakException;
            }

            //ENCONTRAR ELEMENTO ACTIVADO
            if(item.classList.contains("item-active")){
                item.classList.toggle("item-active");
                encontrado = true;
            } 
            
            number = number + 1;
        });  

        //ACTIVAR SIGUIENTE
        if (encontrado){
            itemsCarrusel[number - 1].classList.toggle("item-active");
            throw BreakException;
        } 
    } catch (err) {
    }
};

setInterval(() => {
    siguiente()
}, 10000)