from flask import Flask, Response, request, jsonify, json, url_for
from flask_cors import CORS
from application_services.catalog_item_info_resource import CatalogItemInfoResource
from utils import wrap_pagination, wrap_link
from middleware import notification  # , security

# default settings
PAGESIZE = 10

app = Flask(__name__)
CORS(app)

# trigger_SNS = {"path": "/timeSlot", "method": "GET"}


# @app.after_request
# def after_request(response):
#     print("checking after request")
#     if request.path == trigger_SNS["path"] and request.method == trigger_SNS["method"]:
#         sns = notification.NotificationMiddlewareHandler.get_sns_client()
#         print("Got SNS Client!")
#         tps = notification.NotificationMiddlewareHandler.get_sns_topics()
#         print("SNS Topics = \n", json.dumps(tps, indent=2))
#
#         message = {"test": "event created"}
#         notification.NotificationMiddlewareHandler.send_sns_message(
#             #     #"arn:aws:sns:us-east-1:971820320916:6156project",
#
#             "arn:aws:sns:us-east-1:697047102781:new-user-topic",
#
#             message
#         )
#     return response


@app.route("/", methods=["GET"])
def index():
    context = {
        "GET items": "/items",
        "GET an item by id": "/items/<int:item_id>",
        "GET an item's stock by id": "/items/<int:item_id>/stock",
        "POST an item": "/items",
        "DELETE an item by id": "/items/<int:item_id>",
        "PUT an item by id": "/items/<int:item_id>"
    }
    return jsonify(context)


# TODO: implement pagination
@app.route("/items", methods=["GET"])
def get_items():
    pagesize = request.args.get("pagesize", type=int)
    page = request.args.get("page", type=int)
    name = request.args.get("name", type=str)
    if not pagesize:
        pagesize = PAGESIZE
    if not page:
        page = 1
    limit, offset = pagesize, (page - 1) * pagesize
    results, num_of_rows = CatalogItemInfoResource.get_items(limit=limit, offset=offset, name=name)
    for result in results:
        result["links"] = list()
        result["links"].append(wrap_link(url_for("get_item_stock_by_id", item_id=result["id"]), "stock"))
        result["links"].append(wrap_link(url_for("get_item_by_id", item_id=result["id"]), "self"))
    rsp = jsonify(wrap_pagination(results, pagesize, page, num_of_rows))
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


@app.route("/items", methods=["POST"])
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


@app.route("/items/<int:item_id>", methods=["GET"])
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


@app.route("/items/<int:item_id>/stock", methods=["GET"])
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


@app.route("/items/<int:item_id>", methods=["PUT"])
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


@app.route("/items/<int:item_id>", methods=["DELETE"])
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
