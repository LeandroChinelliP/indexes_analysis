from pyspark.sql.dataframe import DataFrame

class LoadModel:
    data: DataFrame

    def __init__(self, data: list):
        self.data = data
