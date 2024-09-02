import __main__

from os import environ, listdir, path
import json
from pyspark import SparkFiles
from pyspark.sql import SparkSession
from .logging import Log4j

class SparkApp:

    def start_spark(app_name='my_spark_app', master='local[*]', jar_packages=[],
                    files=[], spark_config={}):

        flag_repl = not(hasattr(__main__, '__file__'))
        flag_debug = 'DEBUG' in environ.keys()

        if not (flag_repl or flag_debug):
            spark_builder = (
                SparkSession
                .builder
                .appName(app_name))
        else:
            spark_builder = (
                SparkSession
                .builder
                .master(master)
                .appName(app_name))

            spark_jars_packages = ','.join(list(jar_packages))
            spark_builder.config('spark.jars.packages', spark_jars_packages)

            spark_files = ','.join(list(files))
            spark_builder.config('spark.files', spark_files)

            for key, val in spark_config.items():
                spark_builder.config(key, val)

        spark_session = spark_builder.getOrCreate()
        spark_logger = Log4j(spark_session)
        
        return spark_session, spark_logger