from typing import Dict
from pyspark.sql import SparkSession, DataFrame
from Connect_database_config.database.mysql_connect import MySQLConnect
from Connect_database_config.config.spark_config import get_spark_config

class SparkWriteDatabase:
    def __init__(self,spark:SparkSession, db_config:Dict):
        self.spark = spark
        self.db_config = db_config

    def spark_write_mysql(self, df: DataFrame, table_name:str, jdbc_url:str, config:Dict, mode:str = "append"):
        # try:
        #     mysql_client = MySQLConnect(config)
        #     mysql_client.connect()
        #     mysql_client.close()
        # except Exception as e:
        #     raise Exception(f"Failed to connect mysql: {e}")

        df.write \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", table_name) \
            .option("user", config["user"]) \
            .option("password", config["password"]) \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .mode(mode) \
            .save()

        print(f"Wrote data to mysql in table: {table_name}")

    def spark_write_mongodb(self, df: DataFrame, uri: str, database: str, collection: str, mode: str = "append"):
        df.write \
            .format("mongo") \
            .option("uri", uri) \
            .option("database",database) \
            .option("collection",collection) \
            .mode(mode) \
            .save()

        print(f"Wrote data to MongoDB in collection: {collection} (database: {database})")

    def write_all_database(self, df : DataFrame, mode : str = "append"):
        # self.spark_write_mysql(
        #     df,
        #     self.db_config["mysql"]["table"],
        #     self.db_config["mysql"]["jdbc_url"],
        #     self.db_config["mysql"]["config"],
        #     mode
        # )

        self.spark_write_mongodb(
            df,
            self.db_config["mongodb"]["uri"],
            self.db_config["mongodb"]["database"],
            self.db_config["mongodb"]["collection"],
            mode
        )

        print(f"-------- Write success to all database --------")
