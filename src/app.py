from flask import Flask, Response, request, jsonify, url_for, json

from application_services.catalog_item_info_resource import CatalogItemInfoResource

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    context = {
        "get_item_by_id": "/catalog/<int:item_id>",
        "get_item_by_name": "/catalog/<string:name>",
        "get_item_stock_by_id": "/catalog/stock/<int:item_id>",
        "delete_item_by_id": "/catalog/delete/<int:item_id>",
        "add_item_new": "/catalog/add",
        "update_item": "/catalog/update"
    }
    return jsonify(context)


@app.route("/catalog", methods=["GET"])
def get_items():
    result = CatalogItemInfoResource.get_items()
    if result:
        rsp = jsonify(result)
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


@app.route("/catalog/<int:item_id>", methods=["GET"])
def get_item_by_id(item_id):
    result = CatalogItemInfoResource.get_item_by_id(item_id)
    if result:
        rsp = jsonify(result)
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


@app.route("/catalog/<string:name>", methods=["GET"])
def get_item_by_name(name):
    result = CatalogItemInfoResource.get_item_by_name(name)
    if result:
        rsp = jsonify(result)
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


@app.route("/catalog/stock/<int:item_id>", methods=["GET"])
def get_item_stock_by_id(item_id):
    result = CatalogItemInfoResource.get_item_stock_by_id(item_id)
    if result:
        rsp = jsonify(result["stock"])
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


@app.route("/catalog/delete/<int:item_id>", methods=["DELETE"])
def delete_item_by_id(item_id):
    CatalogItemInfoResource.delete_item_by_id(item_id)
    # Don't know how the packet forms yet
    rsp = Response("", status=200, content_type="application/json")
    return rsp


@app.route("/catalog/add", methods=["POST"])
def add_item_new():
    # data = request.form
    # print("data", data)
    data = json.loads(request.data)
    # print(data)
    CatalogItemInfoResource.add_item_new(
        name=data["name"],
        description=data["description"],
        item_price=data["item_price"],
        image_url=data["image_url"],
        stock=data["stock"]
    )
    rsp = Response("", status=201, content_type="application/json")
    return rsp


@app.route("/catalog/update", methods=["PUT"])
def update_item_by_id():
    data = json.loads(request.data)
    # print(data)
    CatalogItemInfoResource.update_item_by_id(
        item_id=data["item_id"],
        update_column=data["update_column"],
        value_update=data["value_update"])
    rsp = Response("", status=200, content_type="application/json")
    return rsp


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5011)
