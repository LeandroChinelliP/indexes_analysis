import pandas as pd
import requests
import yfinance as yf
from bcb import sgs 
from app.model.constants import Constants
from app.model.dictionaries import Dictionaries
from app.model.schemas import Spark_Schemas
from app.model.etl.ExtractionModel import ExtractionModel
from pyspark.sql.functions import col

class Extraction:
    def extract(self, spark_session) -> ExtractionModel:
        bovespa_data = yf.download(Constants.STOCK_SYMBOL ,start=Constants.START_DATE,end=Constants.END_DATE)
        columns_bovespa = Constants.COLUMNS_BOVESPA
        bovespa_data = bovespa_data[columns_bovespa]
        selic_data = sgs.get({'selic':432}, start=Constants.START_DATE, end=Constants.END_DATE)
        inflation_data = sgs.get({'ipca':433}, start=Constants.START_DATE, end=Constants.END_DATE        )
        real_exchange_index = sgs.get({'tcr':11753}, start=Constants.START_DATE, end=Constants.END_DATE)
        nominal_exchange_index = sgs.get({'ptax':10813}, start=Constants.START_DATE, end=Constants.END_DATE
                                         )
        df_bovespa = spark_session.createDataFrame(bovespa_data.reset_index(), schema=Spark_Schemas.bovespa_schema)
        df_bovespa = (df_bovespa.withColumnRenamed('Date','date').withColumnRenamed('Close','bovespa'))
        
        df_selic = spark_session.createDataFrame(selic_data.reset_index(), schema=Spark_Schemas.selic_schema)
        df_selic = df_selic.withColumnRenamed('Date','date')
                      
        df_inflation = spark_session.createDataFrame(inflation_data.reset_index(),schema=Spark_Schemas.inflation_schema)
        df_inflation = df_inflation.withColumnRenamed('Date','date')

        df_tcr = spark_session.createDataFrame(real_exchange_index.reset_index(),schema=Spark_Schemas.tcr_schema)
        df_tcr = df_tcr.withColumnRenamed('Date','date') 

        df_ptax = spark_session.createDataFrame(nominal_exchange_index.reset_index(),schema=Spark_Schemas.ptax_schema)
        df_ptax = df_ptax.withColumnRenamed('Date','date') 

        df_fed_interest = self.request_api_df(url=(Constants.FED_URL + Constants.FED_OBSERVATION_ENDPOINT), 
                                            parameters=Dictionaries.EFFECTIVE_FEDERAL_FUNDS_RATE, 
                                            data_array='observations')
        df_fed_interest = df_fed_interest[['date', 'value']]
        df_fed_interest['date'] = pd.to_datetime(df_fed_interest['date'], format='%Y-%m-%d')
        df_fed_interest['value'] = df_fed_interest['value'].replace('.', '0')
        df_fed_interest['value'] = df_fed_interest['value'].astype(float)
        df_fed_interest = spark_session.createDataFrame(df_fed_interest, schema=Spark_Schemas.fed_interest_schema)
        df_fed_interest = df_fed_interest.withColumnRenamed("value", "fed_interest").withColumnRenamed("Date", "date")
        df_fed_interest = df_fed_interest.filter('fed_interest >= 0').dropna()

        return ExtractionModel(bovespa_data=df_bovespa
                               ,inflation_data=df_inflation
                               ,selic_data=df_selic
                               ,tcr_data=df_tcr
                               ,ptax_data=df_ptax
                               ,fed_interest_data=df_fed_interest
        )
    
    @staticmethod
    def request_api_df(url: str, parameters:dict, data_array: str) -> pd.DataFrame:
        response = requests.get(url, params=parameters)

        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data[data_array])
            return df
        else:
            print(f'Error: Unable to fetch data. Status code: {response.status_code}')
            return None

