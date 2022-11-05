"""
# GET item info: catalog/<item_id>
# GET item stock: catalog/stock/<item_id>
# DELETE item info: catalog/delete/<item_id>
# POST item info: newitem/
PATCH item info: update/<item_id>
"""
from flask import jsonify, Response

from database_services.rdb_services import RDBService


class CatalogItemInfoResource:
    @classmethod
    def get_item_by_id(cls, item_id):
        """
        :param item_id: id of item
        :return: a dic of the item
        """
        result = RDBService.get_by_value("catalog_db", "item_info", "id", item_id)
        return result

    @classmethod
    def get_item_by_name(cls, name):
        """
        :param name: prefix of item name
        :return: a list of fetched items
        """
        result = RDBService.get_by_prefix("catalog_db", "item_info", "name", name)
        return result

    @classmethod
    def get_item_stock_by_id(cls, item_id):
        """
        :param item_id: id of item
        :return: number of stocking of item
        """
        result = RDBService.get_by_value("catalog_db", "item_stocking", "item_id", item_id)
        return result

    @classmethod
    def delete_item_by_id(cls, item_id):
        RDBService.delete_by_value("catalog_db", "item_stocking", "item_id", item_id)
        RDBService.delete_by_value("catalog_db", "item_info", "id", item_id)

    @classmethod
    def add_item_new(cls, name, description, item_price, image_url, stock):
        RDBService.add_by_prefix(
            db_schema="catalog_db",
            table_name="item_info",
            column_names=("name", "description", "item_price", "image_url"),
            values=(name, description, item_price, image_url)
        )
        RDBService.add_by_prefix(
            db_schema="catalog_db",
            table_name="item_stocking",
            column_names=["stock"],
            values=[stock]
        )

    @classmethod
    def update_item_by_id(cls, item_id, update_column, value_update):
        """
        update an attribute of a item by id
        :param item_id:
        :param update_column:
        :param value_update:
        :return:
        """
        if update_column != "stock":
            RDBService.update_by_template("catalog_db",
                                          "item_info",
                                          "id",
                                          item_id,
                                          update_column,
                                          value_update)
        else:
            RDBService.update_by_template("catalog_db",
                                          "item_stocking",
                                          "item_id",
                                          item_id,
                                          update_column,
                                          value_update)
