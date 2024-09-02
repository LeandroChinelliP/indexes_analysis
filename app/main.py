from app.etl import ETL
from app.config import SparkApp

etl = ETL()
app = SparkApp()
spark_session, spark_logger = app.start_spark()
etl.execute(spark_session)
