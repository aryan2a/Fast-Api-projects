from fastapi import FastAPI , Query
from pydantic import BaseModel, Field
from typing import Optional, List , Dict
from fastapi import HTTPException

app = FastAPI()

products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook','price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub','price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set','price':  49, 'category': 'Stationery',  'in_stock': True },
    {'id': 5, 'name': 'Pencil Set','price':  59, 'category': 'Stationery',  'in_stock': True },
    {'id': 6, 'name': 'earphone','price':  350, 'category': 'Electronics',  'in_stock': True },
    {'id': 7, 'name': 'waterbottle','price':  250, 'category': 'Reusable',  'in_stock': True }
]

@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}

@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

@app.get('/products/filter')
def filter_products(
    category:  str  = Query(None),
    max_price: int  = Query(None),
    in_stock:  bool = Query(None),
    min_price: int  = Query(None)
):
    result = products
 
    if category:
        result = [p for p in result if p['category'] == category]
 
    if max_price is not None:
        result = [p for p in result if p['price'] <= max_price]
 
    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
    
    if min_price is not None:
        result =[p for p in result if p['price'] >= min_price]
 
    return {'filtered_products': result, 'count': len(result)}

@app.get('/products/deals')
def get_search():
    best_deal = min(products,key=lambda p:p["price"])
    premium_pick = max(products,key = lambda p:p["price"])
    return { "best_deal": best_deal, "premium_pick": premium_pick}

@app.get('/products/instock')
def get_instock():
    instock_products = [p for p in products if p["in_stock"]]
    return {"in_stock_products": instock_products}

@app.get("/products/summary")
def summary():
    instock_count = len([p for p in products if p["in_stock"] == True ])
    prices = [p["price"] for p in products]
    most_expensive = max(prices)
    name_most_expensive = [p["name"] for p in products if p["price"] == most_expensive]
    cheapest = min(prices)
    cheapest_name = [p["name"] for p in products if p["price"] == cheapest]
    most_expensive_product = max(products, key=lambda p: p["price"])
    cheapest_product = min(products, key=lambda p: p["price"])

    categories = [
        most_expensive_product["category"],
        cheapest_product["category"]
    ]
    
    return {
        "total products":len(products),
        "in_stock_count":instock_count,
        "out_of_stock":len(products)-instock_count,
        "most_expensive":{"name":name_most_expensive,"price":most_expensive},
        "cheapest":{"name":cheapest_name,"price":cheapest},
        "categories":categories
    }

@app.get('/products/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}

@app.get('/products/category/{category_name}')
def get_category(category_name: str):
    category_products = []

    for product in products:
        if product["category"] == category_name:
            category_products.append(product)

    if category_products:
        return {"products": category_products}

    return {"error": "no products found in this category"}

@app.get('/store/summary')
def get_store_summary():
    in_stock_count = len([p for p in products if p["in_stock"] == True])
    out_stock_count = len(products) - in_stock_count
    categories = set([p["category"] for p in products])
    return {
        "store_name": "My E-commerce Store",
        "total_products":len(products),
        "in_stock":in_stock_count,
        "out_of_stock":out_stock_count,
        "categories":list(categories)
    }

@app.get('/products/search/{keyword}')
def get_search_key(keyword:str):
    count = 0
    product_list = []
    for product in products:
        if keyword.lower() in product["name"].lower():
            count += 1
            product_list.append(product["name"])
    
    if count != 0:
        return {
            "matched_products": product_list,
            "total_matches": count
        }
    
    return {"message": "No products matched your search"}
    
# DAY 2 

@app.get('/products/{product_id}/price')
def get_price(product_id:int):
    for product in products:
        if(product["id"] == product_id):
            return {"name":product["name"],"price":product["price"]}
    return {"error":"product not found"}
        
feedback_db = []

class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)

@app.post("/feedback")
def submit_feedback(feedback: CustomerFeedback):
    feedback_db.append(feedback.model_dump())
    return {
        "message": "Feedback submitted successfully",
        "feedback": feedback,
        "total_feedback": len(feedback_db)
    }  

class orderitem(BaseModel):
    product_id: int
    quantity:int

class Bulkorder(BaseModel):
    company_name:str
    contact_email:str
    items:List[orderitem]

def find_products(product_id:int):
    for product in products:
        if product["id"] == product_id:
            return product
    return None   # ✅ FIX

@app.post("/orders/bulk")
def place_order(order: Bulkorder):
    total_price = 0   # ✅ FIX
    success = []
    failed = []

    for item in order.items:
        product = find_products(item.product_id)

        if not product:   # ✅ FIX
            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })
            continue

        if not product["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": "Out of stock"
            })
            continue

        item_total = product["price"] * item.quantity
        total_price += item_total   # ✅ FIX

        success.append({
            "product_id": item.product_id,
            "name": product["name"],
            "quantity": item.quantity,
            "item_total": item_total
        })

    return {   # ✅ FIX (moved outside loop)
        "company": order.company_name,
        "email": order.contact_email,
        "successful_orders": success,
        "failed_orders": failed,
        "total_bill": total_price
    }

orders: Dict[int, dict] = {}
order_counter = 1

class Order(BaseModel):
    product: str
    price: float

@app.post("/orders")
def create_order(order: Order):
    global order_counter

    order_data = order.model_dump()
    order_data["status"] = "pending"

    orders[order_counter] = order_data

    response = {
        "order_id": order_counter,
        "order": order_data
    }

    order_counter += 1
    return response

@app.get("/orders/{order_id}")
def get_order(order_id:int):
    if order_id not in orders:   # ✅ FIX
        return {"error":"order not found"}
        
    return orders[order_id]      # ✅ FIX

@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id:int):
    if order_id not in orders:
        return {"errors":"order not found"}
    
    orders[order_id]["status"] = "confirmed"
    return {"message":"order confirmed","order": orders[order_id]}

# DAY 3
        
@app.post("/products/add")
def add(name:str,price:int,category:str,in_stock:bool):
    count = len(products)
    count = count + 1
    products.append({"id":count,"name":name,"category":category,"in_stock":in_stock})
    print("product added successfully")

    return {"id":count,"name":name,"category":category,"in_stock":in_stock}

@app.put("/products/update/{product_id}")
def update_product(product_id:int, in_stock:bool = Query(None), price:int = Query(None)):
    
    for product in products:
        if product["id"] == product_id:
            if in_stock is not None:
                product["in_stock"] = in_stock
            if price is not None:
                product["price"] = price

            return {
                "message": "Product updated successfully",
                "product": product
            }

    # ✅ runs ONLY if loop completes with no match
    return {"error": "Product not found"}

@app.delete("/products/{product_id}")
def delete_products(product_id:int):
    for i in range(len(products)):
        if products[i]["id"] == product_id:
            deleted_product = products.pop(i) 
        
            for product in products:
                product["id"] = product["id"] - 1
             
            return{
                 "message":"product deleted successfully"
             }
            
    return {"error": "Product not found"}

@app.get("/products/day/audit")
def audit():

    in_stock_products = [p for p in products if p["in_stock"]]

    if in_stock_products:
        max_price = max(p["price"] for p in in_stock_products)

        most_expensive_names = [
            p["name"] for p in in_stock_products if p["price"] == max_price
        ]
    else:
        max_price = None
        most_expensive_names = []

    day_summary = {
        "total_products": len(products),

        "in_stock_count": len(in_stock_products),

        "out_of_stock_names": [
            p["name"] for p in products if not p["in_stock"]
        ],

        "total_stock_value": sum(
            p["price"] for p in in_stock_products
        ),

        "most_expensive": {
            "price": max_price,
            "name": most_expensive_names
        }
    }

    return day_summary

@app.put("/products/price/discount")
def discount(category: str = Query(..., description='Category to discount'), discount_percent: int = Query(..., ge=1, le=99, description='% off')):
    updated = [p['category'] for p in products if p['category'] == category]
    for i,product in enumerate(products):
        if products[i]["category"] == category:
            new_price = int(product["price"]*(1-discount_percent/100))
            product["price"] = new_price
    
    if updated:
        return {f"total {len(updated)} products are updated and available at a discounted price"}
    else:
        return {"sorry nothing has been updated"}
    
