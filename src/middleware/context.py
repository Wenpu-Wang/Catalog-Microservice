import os
# This is a bad place for this import
import pymysql

SUBSCRIPTIONS = {"/items"}
SLACK_URL = os.environ.get("SLACK_URL", None)
SNS_ARN = "arn:aws:sns:us-east-1:381693958687:catalog_item_request"


class Context:
    def __init__(self):
        pass

    @staticmethod
    def get_db_info():
        """
        :return: A dictionary with connect info for MySQL
        """
        h = os.environ.get("DBHOST", None)
        usr = os.environ.get("DBUSER", None)
        pw = os.environ.get("DBPW", None)

        if h is not None:
            db_info = {
                "host": h,
                "user": usr,
                "password": pw,
                "cursorclass": pymysql.cursors.DictCursor,
                # auto commit
            }
        else:
            # If no environment variables set go local
            db_info = {
                "host": "localhost",
                "user": "root",
                "password": "dbuserdbuser",
                "cursorclass": pymysql.cursors.DictCursor
            }
        return db_info

    @staticmethod
    def get_context(method):
        if method == "SUBSCRIPTIONS":
            return SUBSCRIPTIONS
        elif method == "SLACK_URL":
            return SLACK_URL
        elif method == "SNS_ARN":
            return SNS_ARN
        return None
