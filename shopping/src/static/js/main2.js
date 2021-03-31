function addToCart(id,name,price,image,discription,catagory_id){
    fetch('/api/cart',{
        'method': 'post',
        'body': JSON.stringify({
            'id': id,
            'name': name,
            'price': price,
            'image': image,
            'discription': discription,
            'catagory_id': catagory_id
        }),
        'headers': {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
        var stats = document.getElementById("cart-amunt")
        stats.innerText = `${data.total_quantity} Items - ${data.total_amount} VND`;
    })
}
function pay(){
    if (confirm("Bạn chắc chắn muốn thanh toán?") == true)
        fetch('/api/pay',{
            'method': 'post',
            'headers': {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            alert(data.message);
            location.reload();
        }).catch(err => console.log(err));
}

function del_item(item_id){
    if (confirm("bạn có chắc xóa sản phẩm ?") == true){
        fetch(`/api/cart/${item_id}`,{
            'method': 'delete',
            'headers': {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data.code == 200){
                var x = document.getElementById(`item${data.item_id}`)
                x.style.display = 'none';
            }else{
                alert("xóa thất bại!");
            }
        }).catch(err => alert("Xóa thất bại!"))
    }
}
function update_item(obj, item_id){
    fetch(`/api/cart/${item_id}`,{
        'method': 'post',
        'body': JSON.stringify({
            'quantity': obj.value
        }),
        'headers': {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.code != 200){
            alert("cập nhật thất bại !");
        }else{
            document.getElementById("update").innerText = data.total_quantity
            document.getElementById("update").innerText = data.total_amount
            location.reload();
        }
    }).catch(err => console.log("thất bại !"));
}