let allProducts = [];

async function getProducts() {
    try {
        const response = await fetch('https://dummyjson.com/products');
        const data = await response.json();
        allProducts = data.products;
        displayProducts(allProducts);
    } catch (err) {
        console.error("Failed to fetch products", err);
    }
}

function displayProducts(products) {
    const grid = document.getElementById('products-grid');
    grid.innerHTML = ""; 

    products.forEach(item => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <img src="${item.thumbnail}" alt="${item.title}">
            <h3>${item.title}</h3>
            <p>$${item.price}</p>
        `;
        grid.appendChild(card);
    });
}

document.getElementById('search-bar').addEventListener('input', (event) => {
    const searchTerm = event.target.value.toLowerCase();
    
    const filteredProducts = allProducts.filter(item => 
        item.title.toLowerCase().includes(searchTerm)
    );
    
    displayProducts(filteredProducts); 
});

document.getElementById('sort-select').addEventListener('change', (event) => {
    const sortValue = event.target.value;
    // making copy of list so that the original ones stay intact
    let sortedList = [...allProducts]; 
    if (sortValue === 'high-low') {
        sortedList.sort((a, b) => b.price - a.price); // High to Low logic
    } else if (sortValue === 'low-high') {
        sortedList.sort((a, b) => a.price - b.price); // Low to High logic
    }

    displayProducts(sortedList);
});



getProducts();