

### Accounts Endpoints

- http://localhost:3001/accounts/addAccount [POST]
    - {\
        "firstName":"Ishaan",\
        "lastName" : "Sahu",\
        "email": "ishaan.sahu@hestabit.in",\
        "password" : "In HestaBit learning is Great"\
       }
    - Add new account

- http://localhost:3001/accounts/all [GET]
    - Get all accounts 

- http://localhost:3001/accounts/:email [GET]
    - Get account by email

- http://localhost:3001/accounts/updateName [PATCH]
    - {\
        "email":"ishaan@example.com",\
        "firstName":"Ishaan"\
      }
    - These two are necessary to send

- http://localhost:3001/accounts/:email [DELETE]
    - delete accounts based on email


### Orders Endpoints

- http://localhost:3001/orders [POST]
    - {\
    "account":"699f0152f66d254a3a911df4",\
    "items": [{\
        "product": "69a0114c1723b8fbd9c9a55b",\
        "quantity": 12,\
        "priceAtPurchase": 100\
    }]\
    }
    - Add a new order & order price is added at saving time

- http://localhost:3001/orders/:id [GET]
    - Get order by id

- http://localhost:3001/orders/account/:accountID [GET]
    - Get orders by accountID

- http://localhost:3001/orders/:id/status [PATCH]
    - update order status using orderID
    - { \
    "status": "shipped"\
    }

### Product Endpoints

- http://localhost:3001/product [POST]
    - {\
    "name":"new product",\
    "description": "this is desc",\
    "price": 1000,\
    "tags": ["BestProduct", "Worst product"]\
    }
    - Add new product

- http://localhost:3001/product/:productID [GET]
    - Get product by ID

- http://localhost:3001/product/:productID [DELETE]
    - Delete product by ID

- http://localhost:3001/product?minPrice=1000&maxPrice=2000&sortOrder=asc [GET]
    - Get products with complex filters
    - sorting order and minPrice and maxPrice
    - cursorId = 
    - cursorPrice = 


#### For running locally command -> node server.js


## NodeJS LifeCycle

![nodejs lifecycle](images/nodejs%20lifecycle.png)

## Event Loop Phases

![event loop phases](images/event%20loop%20phases.png)

- Between every phase, Node checks for **microtasks** first:

```js
Phase completes
      ↓
process.nextTick() callbacks   ← highest priority
      ↓
Promise .then() callbacks      ← second priority
      ↓
Move to next phase
```

