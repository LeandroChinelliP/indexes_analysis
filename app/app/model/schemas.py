from pyspark.sql.types import StructType, StructField, DateType, IntegerType, FloatType

class Spark_Schemas:
    bovespa_schema = StructType([
                            StructField("Date", DateType(), True),
                            StructField("Close", FloatType(), True)
                            ])
    selic_schema = StructType([
                            StructField("Date", DateType(), True),
                            StructField("selic", FloatType(), True)
                            ])
    inflation_schema = StructType([
                            StructField("Date", DateType(), True),
                            StructField("ipca", FloatType(), True)
                            ])
    tcr_schema = StructType([
                            StructField("Date", DateType(), True),
                            StructField("tcr", FloatType(), True)
                            ])
    ptax_schema = StructType([
                            StructField("Date", DateType(), True),
                            StructField("ptax", FloatType(), True)
                            ])
    fed_interest_schema = StructType([
                            StructField("Date", DateType(), True),
                            StructField("value", FloatType(), True)
                            ])
