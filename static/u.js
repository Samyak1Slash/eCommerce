document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const name = this.getAttribute('data-name');
            const price = parseFloat(this.getAttribute('data-price'));
            
            addToCart(name, price);
        });
    });
});

function addToCart(name, price) {
    fetch('/add_to_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            price: price
        })
    })
    .then(response => {
        if (response.ok) {
            alert('Item added to cart successfully!');
        } else {
            throw new Error('Failed to add item to cart');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
