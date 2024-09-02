from app.model.etl import ExtractionModel, TransformationModel
from pyspark.sql import DataFrame
from pyspark.sql.functions import year, month, col, rank, trunc, mean, stddev, avg
from pyspark.sql.window import Window
from pyspark.ml.stat import Correlation
from pyspark.ml.feature import VectorAssembler
from scipy.ndimage import gaussian_filter1d
import pandas as pd
import numpy as np

class Transformation:
    def __init__(self) -> None:
        pass

    def transform(self, extraction: ExtractionModel, spark_session) -> TransformationModel:
        self.df_bovespa = extraction.bovespa_data
        self.df_inflation = extraction.inflation_data
        self.df_selic = extraction.selic_data 
        self.df_tcr = extraction.tcr_data
        self.df_ptax = extraction.ptax_data
        self.df_fed_interest = extraction.fed_interest_data
        self.spark = spark_session

        df_bovespa_join = self.trunc_date(df=self.df_bovespa,
                                            partition_column='year_month',
                                            trunc_column='date',
                                            trunc_mode='month')

        df_selic_join = self.trunc_date(df=self.df_selic,
                                        partition_column='year_month',
                                        trunc_column='date',
                                        trunc_mode='month')

        df_fed_join = self.trunc_date(df=self.df_fed_interest,
                                        partition_column='year_month',
                                        trunc_column='date',
                                        trunc_mode='month')

        df_fed_join.show()
        df_bovespa_smooth = self.gaussian_smooth(spark_df=df_bovespa_join, column='bovespa', sigma_number=3)
        df_selic_join_smooth = self.gaussian_smooth(spark_df=df_selic_join, column='selic', sigma_number=3)
        df_ipca_smooth = self.gaussian_smooth(spark_df=self.df_inflation, column='ipca', sigma_number=3)
        df_tcr_smooth = self.gaussian_smooth(spark_df=self.df_tcr, column='tcr', sigma_number=10)
        df_ptax_smooth = self.gaussian_smooth(spark_df=self.df_ptax, column='ptax', sigma_number=3)
        df_fed_int_smooth = self.gaussian_smooth(spark_df=df_fed_join, column='fed_interest', sigma_number=2)

        df_indexes = (df_bovespa_smooth
                            .join(df_selic_join_smooth, 'date', how='inner')
                            .join(df_ipca_smooth, 'date', how='inner')
                            .join(df_tcr_smooth, 'date', how='inner')
                            .join(df_ptax_smooth, 'date', how='inner')
                            .join(df_fed_int_smooth, 'date', how='inner')
        )
        df_indexes = self.zscored_data(df_indexes)
        columns_input = ['bovespa', 'selic', 'ipca', 'tcr', 'ptax', 'fed_interest']
        pandas_df_correlation = self.correlation(df=df_indexes, columns_array=columns_input)

        return TransformationModel(bovespa_data=self.df_bovespa
                                    ,inflation_data=self.df_inflation
                                    ,selic_data=self.df_selic
                                    ,tcr_data=self.df_tcr
                                    ,ptax_data=self.df_ptax
                                    ,fed_interest_data=self.df_fed_interest
                                    ,df_indexes=df_indexes
                                    ,correlation_matrix=pandas_df_correlation)

    def gaussian_smooth(self, spark_df: DataFrame, column:str, sigma_number=int) -> DataFrame:
        pandas_df = spark_df.toPandas()
        pandas_df[f'smoothed_{column}'] = gaussian_filter1d(pandas_df[column], sigma=sigma_number)
        df_smooth = self.spark.createDataFrame(pandas_df)
        df_smooth = df_smooth.drop(column).withColumnRenamed(f'smoothed_{column}', f'{column}')
        return df_smooth

    def trunc_date(self, df: DataFrame, partition_column:str, trunc_column: str, trunc_mode: str) -> DataFrame:
        df_year_month = self.add_year_month(df=df)
        window_date = Window.partitionBy(partition_column).orderBy(col(trunc_column).desc())
        df_year_month = df_year_month.withColumn('r', rank().over(window_date)).filter('r=1').drop('r')
        df_year_month = df_year_month.withColumn('trunc_column', trunc(trunc_column, trunc_mode))
        df_year_month = df_year_month.drop(col(trunc_column), col(partition_column)).withColumnRenamed('trunc_column', trunc_column)
        return df_year_month

    @staticmethod
    def add_year_month(df: DataFrame, column_name: str=None) -> DataFrame:
        column = 'year_month' if column_name is None else column_name
        return df.withColumn(column, year(df.date)*100 + month(df.date))

    @staticmethod
    def correlation(df: DataFrame, columns_array: list) -> pd.DataFrame:
        columns_input = columns_array
        vector_assembler = VectorAssembler(inputCols=columns_input,
                                           outputCol='features')
        data_vector = vector_assembler.transform(df).select('features')
        correlation_matrix = Correlation.corr(data_vector, 'features').head()[0]
        correlation_array = np.array(correlation_matrix.toArray())
        df_correlation = pd.DataFrame(correlation_array, index=columns_input, columns=columns_input)
        return df_correlation
        
    @staticmethod
    def moving_average(df: DataFrame, aggregation_interval: int, column: str):
        window_mov_avg = Window.orderBy(col('date')).rowsBetween(aggregation_interval,0)
        df_mov_avg = df.withColumn(f'{column}_mv_avg', avg(col(f'{column}')).over(window_mov_avg))
        df_mov_avg = df_mov_avg.drop(f'{column}').withColumnRenamed(f'{column}_mv_avg', f'{column}')
        return df_mov_avg

    @staticmethod
    def zscored_data(df) -> DataFrame:
        for column in df.columns:
            if column == 'date':
                continue
            mean_val = df.select(mean(col(column))).first()[0]
            stddev_val = df.select(stddev(col(column))).first()[0]
            df = df.withColumn(column, (col(column) - mean_val) / stddev_val)
        return df