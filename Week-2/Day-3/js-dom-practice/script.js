const headers = document.querySelectorAll(".header");

    headers.forEach(header => {
        header.addEventListener("click", () => {
            const currentItem = header.parentElement;

            document.querySelectorAll(".item").forEach(item => {
                if (item !== currentItem) {
                    item.classList.remove("active");
                }
            });

            currentItem.classList.toggle("active");
        
        });
    });