from pyspark.sql.dataframe import DataFrame

class ExtractionModel:
    bovespa_data: DataFrame
    selic_data: DataFrame
    inflation_data: DataFrame

    def __init__(self,bovespa_data
                    ,inflation_data
                    ,selic_data
                    ,tcr_data
                    ,ptax_data
                    ,fed_interest_data
    ):
        self.bovespa_data = bovespa_data 
        self.inflation_data = inflation_data
        self.selic_data = selic_data 
        self.tcr_data = tcr_data
        self.ptax_data = ptax_data
        self.fed_interest_data = fed_interest_data 