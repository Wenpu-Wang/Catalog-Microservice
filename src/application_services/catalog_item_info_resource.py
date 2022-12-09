from database_services.rdb_services import RDBService

LIMIT = 25
OFFSET = 0


class CatalogItemInfoResource:
    @classmethod
    def get_items(cls, limit=LIMIT, offset=OFFSET, name=None):
        if not name:
            template = None
        else:
            template = {"name": name}
        result, num_of_rows = RDBService.find_by_template_join(
            db_schema="catalog_db",
            table_name1="item_info",
            table_name2="item_stocking",
            column_names1=["id", "name", "description", "item_price", "image_url"],
            column_names2=["stock"],
            template=template,
            join_column1="id",
            join_column2="item_id",
            limit=limit,
            offset=offset,
        )
        return result, num_of_rows

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
        :param name: name of item
        :return: a dic of an item
        """
        result = RDBService.get_by_value("catalog_db", "item_info", "name", name)
        return result

    @classmethod
    def get_items_by_name(cls, name):
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
        """
        :param item_id: id of item
        :return: Delete item successful or not
        """
        success = RDBService.delete_by_value(db_schema="catalog_db",
                                             table_name1="item_stocking",
                                             table_name2="item_info",
                                             column_name1="item_id",
                                             column_name2="id",
                                             value=item_id
                                             )
        return success

    @classmethod
    def add_item_new(cls, name, description, item_price, image_url, stock):
        """
        :return: Add id of new item, or False (not successful)
        """
        new_item_id = RDBService.add_by_prefix(
            db_schema="catalog_db",
            table_name1="item_info",
            table_name2="item_stocking",
            column_names1=["name", "description", "item_price", "image_url"],
            column_names2=["stock"],
            values1=[name, description, item_price, image_url],
            values2=[stock]
        )
        return new_item_id

    @classmethod
    def update_item_by_id(cls, item_id, new_data: dict):
        set_info_list = []
        set_stock_list = []
        for k, v in new_data.items():
            if k != "stock":
                set_info_list.append((k, v))
            else:
                set_stock_list.append((k, v))

        row_affected1, row_affected2 = 0, 0
        if set_info_list:
            row_affected1 = RDBService.update_by_value(db_schema="catalog_db",
                                                       table_name="item_info",
                                                       column_name="id",
                                                       value=item_id,
                                                       update_columns=set_info_list)
        if set_stock_list:
            row_affected2 = RDBService.update_by_value(db_schema="catalog_db",
                                                       table_name="item_stocking",
                                                       column_name="item_id",
                                                       value=item_id,
                                                       update_columns=set_stock_list)
        if row_affected1 + row_affected2 == 0:
            return False
        else:
            return True
