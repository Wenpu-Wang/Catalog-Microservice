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
              column_name + " like " + "%s"
        value_prefix = value_prefix + "%"
        print(value_prefix)
        print("SQL Statement = " + cur.mogrify(sql, value_prefix))

        cur.execute(sql, args=value_prefix)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def get_by_value(cls, db_schema, table_name, column_name, value):
        conn = cls._get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + db_schema + "." + table_name + " where " + \
              column_name + " = %s"
        print("SQL Statement = " + cur.mogrify(sql, value))

        cur.execute(sql, args=value)
        res = cur.fetchone()

        conn.close()

        return res

    @classmethod
    def delete_by_value(cls, db_schema, table_name1, table_name2,
                        column_name1, column_name2, value):
        """
        :return: successful or not
        """
        conn = cls._get_db_connection()
        sql1 = "delete from " + db_schema + "." + table_name1 + " where " + \
               column_name1 + " = " + "%s"
        sql2 = "delete from " + db_schema + "." + table_name2 + " where " + \
               column_name2 + " = " + "%s"

        try:
            cur = conn.cursor()
            print("SQL Statement = " + cur.mogrify(sql1, value))
            print("SQL Statement = " + cur.mogrify(sql2, value))
            cur.execute(sql1, args=value)
            cur.execute(sql2, args=value)
        except UserWarning:
            conn.rollback()
            conn.close()
            return False
        else:
            conn.commit()
            conn.close()
            return True

    @classmethod
    def add_by_prefix(cls, db_schema, table_name1, table_name2, column_names1, column_names2,
                      values1, values2):
        conn = cls._get_db_connection()

        sql1 = " INSERT INTO " + db_schema + "." + table_name1 + " (" + ",".join(column_names1) + ")"
        sql1 += (" values (" + ",".join(len(column_names1) * ["%s"]) + ")")

        sql2 = " INSERT INTO " + db_schema + "." + table_name2 + " (" + ",".join(column_names2) + ")"
        sql2 += (" values (" + ",".join(len(column_names2) * ["%s"]) + ")")

        try:
            cur = conn.cursor()
            print("SQL Statement = " + cur.mogrify(sql1, values1))
            print("SQL Statement = " + cur.mogrify(sql2, values2))
            cur.execute(sql1, args=values1)
            cur.execute(sql2, args=values2)
        except UserWarning:
            conn.rollback()
            conn.close()
            return False
        else:
            conn.commit()
            conn.close()
            return True

    @classmethod
    def update_by_value(cls, db_schema, table_name, column_name, value, update_columns: list):
        """
        :param column_name:
        :param db_schema:
        :param table_name:
        :param value: the matched attribute's value
        :param update_columns: the [(k,v)...] list
        :return:
        """
        conn = cls._get_db_connection()
        cur = conn.cursor()

        li = []
        for k, v in update_columns:
            li.append(f"{k}='{v}'")

        sql = " UPDATE " + db_schema + "." + table_name + " SET " + ", ".join(li) + " WHERE " + column_name + "=%s"
        print("SQL Statement = " + cur.mogrify(sql, value))

        cur.execute(sql, args=value)
        conn.commit()
        row_affected = cur.rowcount
        print("row_affected:", row_affected)
        conn.close()

        return row_affected

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

    @classmethod
    def find_by_template(cls, db_schema, table_name, column_name, template):
        wc, args = cls._get_where_clause_args(template)

        conn = cls._get_db_connection()
        cur = conn.cursor()

        sql = "select " + ", ".join(column_name) + "from " + db_schema + "." + table_name + " " + wc
        cur.execute(sql, args=args)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def find_by_template_join(cls, db_schema, table_name1, table_name2, column_names1, column_names2, template,
                              join_column1, join_column2):
        wc, args = cls._get_where_clause_args(template)

        conn = cls._get_db_connection()
        cur = conn.cursor()

        for i in range(len(column_names1)):
            column_names1[i] = table_name1 + "." + column_names1[i]

        for i in range(len(column_names2)):
            column_names2[i] = table_name2 + "." + column_names2[i]

        print(column_names1)
        print(column_names2)
        column_names1.extend(column_names2)

        sql = "select " + ", ".join(column_names1) + " from " + \
              db_schema + "." + table_name1 + " join " + db_schema + "." + table_name2 + " on " + \
              table_name1 + "." + join_column1 + " = " + table_name2 + "." + join_column2 + " " + wc
        print("SQL Statement = " + cur.mogrify(sql, None))

        cur.execute(sql, args=args)
        res = cur.fetchall()

        conn.close()

        return res
