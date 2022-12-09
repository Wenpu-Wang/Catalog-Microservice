from flask import Flask, Response, request, jsonify, json, url_for

from application_services.catalog_item_info_resource import CatalogItemInfoResource
from utils import wrap_func, wrap_link

# default settings
LIMIT = 10
OFFSET = 0

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    context = {
        "GET items": "/items",
        "GET items by name": "/items/<string:name>",
        "POST an item": "/item",
        "GET an item by id": "/item/<int:item_id>",
        "GET an item's stock by id": "/item/<int:item_id>/stock",
        "PUT an item by id": "/item/<int:item_id>",
        "DELETE an item by id": "/item/<int:item_id>"
    }
    return jsonify(context)


# TODO: implement pagination
@app.route("/items", methods=["GET"])
def get_items():
    limit = request.args.get("limit", type=int)
    offset = request.args.get("offset", type=int)
    name = request.args.get("name", type=str)
    if not limit:
        limit = LIMIT
    if not offset:
        offset = OFFSET
    results, num_of_rows = CatalogItemInfoResource.get_items(limit, offset, name)
    for result in results:
        result["links"] = list()
        result["links"].append(wrap_link(url_for("get_item_stock_by_id", item_id=result["id"]), "stock"))
        result["links"].append(wrap_link(url_for("get_item_by_id", item_id=result["id"]), "self"))
    rsp = jsonify(wrap_func(results, limit, offset, num_of_rows))
    return rsp


@app.route("/items/<string:name>", methods=["GET"])
def get_items_by_name(name):
    # search for matched prefix names
    result = CatalogItemInfoResource.get_items_by_name(name)
    if result:
        for item in result:
            item["stock"] = CatalogItemInfoResource.get_item_stock_by_id(item["id"])["stock"]
        rsp = jsonify(result)
    else:
        rsp = Response(json.dumps({"message": "item not found"}), status=404, content_type="application/json")
    return rsp


@app.route("/item", methods=["POST"])
def post_item():
    data = json.loads(request.data)
    exist = CatalogItemInfoResource.get_item_by_name(data["name"])
    if exist:
        return Response(json.dumps({"message": "item already exist"}), status=400, content_type="application/json")
    new_item_id = CatalogItemInfoResource.add_item_new(
        name=data["name"],
        description=data["description"],
        item_price=data["item_price"],
        image_url=data["image_url"],
        stock=data["stock"]
    )
    if new_item_id:
        item = CatalogItemInfoResource.get_item_by_id(new_item_id)
        item["stock"] = CatalogItemInfoResource.get_item_stock_by_id(new_item_id)["stock"]
        rsp = jsonify(item)
        # rsp = Response(json.dumps({"message": "new item added"}), status=200, content_type="application/json")
    else:
        rsp = Response(json.dumps({"message": "item creation failed"}), status=500, content_type="application/json")
    return rsp


@app.route("/item/<int:item_id>", methods=["GET"])
def get_item_by_id(item_id):
    result = CatalogItemInfoResource.get_item_by_id(item_id)
    if result:
        result["stock"] = CatalogItemInfoResource.get_item_stock_by_id(item_id)["stock"]
        result["links"] = list()
        result["links"].append(wrap_link(url_for("get_item_stock_by_id", item_id=item_id), "stock"))
        result["links"].append(wrap_link(url_for("get_item_by_id", item_id=item_id), "self"))
        rsp = jsonify(result)
    else:
        rsp = Response(json.dumps({"message": "item not found"}), status=404, content_type="application/json")
    return rsp


@app.route("/item/<int:item_id>/stock", methods=["GET"])
def get_item_stock_by_id(item_id):
    result = CatalogItemInfoResource.get_item_stock_by_id(item_id)
    if result:
        result["links"] = list()
        result["links"].append(wrap_link(url_for("get_item_by_id", item_id=item_id), "info"))
        result["links"].append(wrap_link(url_for("get_item_stock_by_id", item_id=item_id), "self"))
        rsp = jsonify(result)
    else:
        rsp = Response(json.dumps({"message": "item not found"}), status=404, content_type="application/json")
    return rsp


@app.route("/item/<int:item_id>", methods=["PUT"])
def update_item_by_id(item_id):
    new_data = json.loads(request.data)
    exist = CatalogItemInfoResource.get_item_by_id(item_id)
    if not exist:
        return Response(json.dumps({"message": "item not found"}), status=404, content_type="application/json")
    else:
        success = CatalogItemInfoResource.update_item_by_id(item_id, new_data)
        if success:
            # rsp = Response(json.dumps({"message": "update successful"}), status=200, content_type="application/json")
            rsp = CatalogItemInfoResource.get_item_by_id(item_id)
            rsp["stock"] = CatalogItemInfoResource.get_item_stock_by_id(item_id)["stock"]
        else:
            # if there's no change in the update
            rsp = Response(json.dumps({"message": "same update"}), status=400, content_type="application/json")
    return rsp


@app.route("/item/<int:item_id>", methods=["DELETE"])
def delete_item_by_id(item_id):
    exist = CatalogItemInfoResource.get_item_by_id(item_id)
    if not exist:
        return Response(json.dumps({"message": "item not found"}), status=404, content_type="application/json")
    success = CatalogItemInfoResource.delete_item_by_id(item_id)
    if success:
        rsp = Response(json.dumps({"message": "deletion successful"}), status=200, content_type="application/json")
    else:
        rsp = Response(json.dumps({"message": "deletion failed"}), status=500, content_type="application/json")
    return rsp


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5011)
