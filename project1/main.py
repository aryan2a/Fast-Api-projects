import fastapi
 
app = fastapi.FastAPI()
 
# ── Temporary data — acting as our database for now ──────────
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook','price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub','price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set','price':  49, 'category': 'Stationery',  'in_stock': True },
    {'id': 5, 'name': 'Pencil Set','price':  59, 'category': 'Stationery',  'in_stock': True },
    {'id': 6, 'name': 'earphone','price':  350, 'category': 'Electronics',  'in_stock': True },
    {'id': 7, 'name': 'waterbottle','price':  250, 'category': 'Reusable',  'in_stock': True }
]
 
# ── Endpoint 0 — Home ────────────────────────────────────────
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}
 
# ── Endpoint 1 — Return all products ──────────────────────────
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

@app.get('/products/filter')
def filter_products(
    category:  str  = fastapi.Query(None, description='Electronics or Stationery'),
    max_price: int  = fastapi.Query(None, description='Maximum price'),
    in_stock:  bool = fastapi.Query(None, description='True = in stock only')
):
    result = products          # start with all products
 
    if category:
        result = [p for p in result if p['category'] == category]
 
    if max_price:
        result = [p for p in result if p['price'] <= max_price]
 
    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
 
    return {'filtered_products': result, 'count': len(result)}

@app.get('/products/deals')
def get_search():
    best_deal = min(products,key=lambda p:p["price"])
    # here key expects a function
    # key is used for comparison
    premium_pick = max(products,key = lambda p:p["price"])
    return { "best_deal": best_deal, "premium_pick": premium_pick}

@app.get('/products/instock')
def get_instock():
    instock_products = [p for p in products if p["in_stock"]]
    return {"in_stock_products": instock_products}
 
# ── Endpoint 2 — Return one product by its ID ──────────────────
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
    return {"store_name": "My E-commerce Store", "total_products":len(products),"in_stock":in_stock_count,"out_of_stock":out_stock_count,"categories":categories}

@app.get('/products/search/{keyword}')
def get_search(keyword:str):
    count = 0
    product_list = []
    for product in products:
        if keyword.lower() in product["name"].lower():
            count += 1
            product_list.append(product["name"])
    
    if(count != 0):
        return f"matched products: {product_list} , total matches: {count}"
    
    elif(count == 0):
        return {"message": "No products matched your search"}
    


    


        

            
        






    
        


