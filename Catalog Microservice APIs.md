# Catalog Microservice APIs

## Item in Catalog

Each item is with 6 attributes: `id`, `name`, `description`, `item_price`, `image_url`, `stock`

Example:

```json
{
    "description": "Eggs pack, 12 count",
    "id": 5,
    "image_url": null,
    "item_price": 20.0,
    "name": "Eggs Brown Large Grade A, 12 Count",
    "stock": 4
}
```

## GET

### GET /items

```http
GET /items?page=1&pagesize=10&name=wang
```

GET all the items. Optional query string: `page`, `pagesize` (default=10), `name`

In pagination section `metadata/result_set`:
`count`: number of items in this page
`page`: current page number
`pagesize`: max number of items in a page
`total`: total number of items (in all pages)
`total_page`: total pages available

Example:

```http
GET /items?page=1&pagesize=2
```

```json
{
    "metadata": {
        "result_set": {
            "count": 2,
            "page": 1,
            "pagesize": 2,
            "total": 11,
            "total_page": 6
        }
    },
    "results": [
        {
            "description": "Coke product 500ml from Coca Cola",
            "id": 1,
            "image_url": null,
            "item_price": 2.5,
            "links": [
                {
                    "href": "/items/1/stock",
                    "rel": "stock"
                },
                {
                    "href": "/items/1",
                    "rel": "self"
                }
            ],
            "name": "Coca Cola",
            "stock": 1
        },
        {
            "description": "Coke product 500ml from Pepsi",
            "id": 2,
            "image_url": null,
            "item_price": 45.0,
            "links": [
                {
                    "href": "/items/2/stock",
                    "rel": "stock"
                },
                {
                    "href": "/items/2",
                    "rel": "self"
                }
            ],
            "name": "Pepsi Coke",
            "stock": 2
        }
    ]
}
```

Status code: 200

---

```http
GET /items?page=10&pagesize=2 (empty page)
```

```json
{
    "metadata": {
        "result_set": {
            "count": 0,
            "page": 10,
            "pagesize": 2,
            "total": 11,
            "total_page": 6
        }
    },
    "results": []
}
```

Status code: 200

### GET /items/\<int: item_id\>

```http
GET /items/<int:item_id>
```

GET an item by its `id`

Example:

```http
GET /items/5
```

```json
{
    "description": "Eggs pack, 12 count",
    "id": 5,
    "image_url": null,
    "item_price": 3.39,
    "links": [
        {
            "href": "/items/5/stock",
            "rel": "stock"
        },
        {
            "href": "/items/5",
            "rel": "self"
        }
    ],
    "name": "Eggs Brown Large Grade A, 12 Count",
    "stock": 5
}
```

Status code: 200

---

```http
GET /items/25 (this item doesn't exist)
```

```json
{
    "message": "item not found"
}
```

Status code: 404

### GET /items/\<int: item_id\>/stock

```http
GET /items/<int:item_id>/stock
```

GET an item's stock by its `id`

Example:

```http
GET /items/5/stock
```

```json
{
    "item_id": 5,
    "links": [
        {
            "href": "/items/5",
            "rel": "info"
        },
        {
            "href": "/items/5/stock",
            "rel": "self"
        }
    ],
    "stock": 5
}
```

Status code: 200

---

```http
GET /items/25/stock (this item doesn't exist)
```

```json
{
    "message": "item not found"
}
```

Status code: 404

## POST

### POST /items

```http
POST /items
```

POST an item, with all 5 necessary attributes: `name`, `description`, `item_price`, `image_url`, `stock`

Example:

Request body:

```json
{
    "name": "kirby",
    "description": "a pink ball",
    "item_price": 5,
    "stock": 2,
    "image_url": "https://www.google.com/url?sa=i&url=https%3A%2F%2Ffreepngimg.com%2Fcartoon..."
}
```

Response body (The `id` of the item is returned, other attributes are the same with the request body):

```json
{
    "description": "a pink ball",
    "id": 12,
    "image_url": "https://www.google.com/url?sa=i&url=https%3A%2F%2Ffreepngimg.com%2Fcartoon...",
    "item_price": 5.0,
    "name": "kirby",
    "stock": 2
}
```

Status code: 200

---

Response body (If POST an item that has the same `name` as an item already in the resource):

```json
{
    "message": "item already exist"
}
```

Status code: 400

## DELETE

### DELETE /items/\<int: item_id\>

```http
DELETE /items/<int:item_id>
```

DELETE an item by its `id`

Example:

```http
DELETE /items/6
```

```json
{
    "message": "deletion successful"
}
```

Status code: 200

---

```http
DELETE /items/25 (This item doesn't exist)
```

```json
{
    "message": "item not found"
}
```

Status code: 404

## PUT

### PUT /items/\<int: item_id\>

```http
PUT /items/<int:item_id>
```

PUT/UPDATE an item by its `id`. In the request body, specify the new values of attributes among `name`, `description`, `item_price`, `image_url`, `stock`

Example:

```http
PUT /items/5
```

Request body (specify the new values need to be updated):

```json
{
    "stock": 4,
    "item_price":30
}
```

Response body (return all the attributes of the updated item):

```json
{
    "description": "Eggs pack, 12 count",
    "id": 5,
    "image_url": null,
    "item_price": 30.0,
    "name": "Eggs Brown Large Grade A, 12 Count",
    "stock": 4
}
```

Status code: 200

---

Request body (using the same body to update the item):

```json
{
    "stock": 4,
    "item_price":30
}
```

Response body:

```json
{
    "message": "same update"
}
```

Status code: 400

---

```http
PUT /items/25 (this item doesn't exist)
```

Request body: ...

Response body:

```json
{
    "message": "item not found"
}
```

Status code: 404
