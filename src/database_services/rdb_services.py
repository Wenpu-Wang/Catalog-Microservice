import pymysql
import logging

from middleware.context import Context as Context

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class RDBService:
    @classmethod
    def _get_db_connection(cls) -> object:
        db_connect_info = Context.get_db_info()

        logger.info("RDBService._get_db_connection:")
        logger.info("\t HOST = " + db_connect_info['host'])

        db_info = Context.get_db_info()
        db_connection = pymysql.connect(
            **db_info
        )
        return db_connection

    @classmethod
    def get_by_prefix(cls, db_schema, table_name, column_name, value_prefix):
        conn = cls._get_db_connection()
        cur = conn.cursor()

        # sql = f"select * from {db_schema}.{table_name} where {column_name} like '{value_prefix}%'"
        sql = "select * from " + db_schema + "." + table_name + " where " + \
              column_name + " like " + "'" + value_prefix + "%'"
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def get_by_value(cls, db_schema, table_name, column_name, value):
        conn = cls._get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + db_schema + "." + table_name + " where " + \
              column_name + " = " + str(value)
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        res = cur.fetchone()

        conn.close()

        return res

    @classmethod
    def delete_by_value(cls, db_schema, table_name, column_name, value):
        conn = cls._get_db_connection()
        cur = conn.cursor()

        sql = "delete from " + db_schema + "." + table_name + " where " + \
              column_name + " = " + str(value)
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        print(res)
        res = cur.fetchall()
        conn.commit()

    @classmethod
    def add_by_prefix(cls, db_schema, table_name, column_names, values):
        conn = cls._get_db_connection()
        cur = conn.cursor()

        sql = " INSERT INTO " + db_schema + "." + table_name + " ("
        for i in range(len(column_names) - 1):
            sql += (column_names[i] + ", ")
        sql += (column_names[-1] + ")")

        sql += " values ("
        for i in range(len(values) - 1):
            sql += ("'" + str(values[i]) + "'" + ", ")
        sql += ("'" + str(values[-1]) + "'" + ");")

        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        res = cur.fetchall()
        conn.commit()
        print(res)
        conn.close()

        return res

    @classmethod
    def update_by_template(cls, db_schema, table_name, column_name, value_prefix, update_column, value_update):
        conn = cls._get_db_connection()
        cur = conn.cursor()
        print("update_by_template")

        sql = "update " + db_schema + "." + table_name + \
              " set " + str(update_column) + " = '" + str(value_update) + "' where " + column_name + ' = ' \
              + str(value_prefix)
        print("SQL Statement = " + cur.mogrify(sql, None))
        res = cur.execute(sql)
        res = cur.fetchall()
        conn.commit()

    @staticmethod
    def _get_where_clause_args(template):
        terms = []
        args = []

        if template is None or template == {}:
            clause = ""
            args = None
        else:
            for k, v in template.items():
                terms.append(k + "=%s")
                args.append(v)

            clause = " where " + " AND ".join(terms)

        return clause, args

    """
    # def put_by_template(db_schema, table_name, template, id, name, field_list):
    #     print(id, name)
    #     wc, args = _get_where_clause_args(template)
    #
    #     conn = _get_db_connection()
    #     cur = conn.cursor()
    #
    #     table = db_schema + "." + table_name
    #     # sql = "update " + table + " set Name=" + name + " " + "where idPlayer=" + id + " " + wc
    #     sql = f"UPDATE {table} SET Name='{name}' WHERE idPlayer={id}" + " " + wc
    #     print(sql)
    #     res = cur.execute(sql, args=args)
    #     res = cur.fetchall()
    #
    #     conn.commit()
    #     conn.close()
    #
    #     return res

    @classmethod
    def select_attribute2_by_attribute1(cls, db_schema, table1, table2, attribute1, attribute2, reference1, reference2,
                                        value):
        conn = cls._get_db_connection()
        cur = conn.cursor()

        sql = "select " + attribute2 + " from " + db_schema + "." + table2 + " where " + reference2 + " = (" \
              + " select " + reference1 + " from " + db_schema + "." + table1 + " where " + attribute1 + " = " + value \
              + ")"
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        print(res)
        res = cur.fetchall()

        conn.close()
        return res
        """
