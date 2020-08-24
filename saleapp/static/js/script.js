function addToCart(id, name, price) {
    fetch("/api/cart", {
        body: JSON.stringify({
            "product_id": id,
            "name": name,
            "price": price
        }),
        method: "post",
        headers: {"Content-Type": "application/json"}
    }).then(res => res.json()).then(data => {
        var cart = document.getElementById("cartId");
        var amount = document.getElementById("amount")
        cart.innerText = `${data.quantity}`;
        amount.innerText = `VNĐ ${data.sum}`;
    })
}