from pyspark.sql.dataframe import DataFrame

class TransformationModel:
    df_indexes: DataFrame
    correlation_matrix: DataFrame

    def __init__(self 
                ,bovespa_data 
                ,inflation_data
                ,selic_data 
                ,tcr_data
                ,ptax_data
                ,fed_interest_data
                ,df_indexes
                ,correlation_matrix):
        
        self.bovespa_data = bovespa_data 
        self.inflation_data = inflation_data
        self.selic_data = selic_data 
        self.tcr_data = tcr_data
        self.ptax_data = ptax_data
        self.fed_interest_data = fed_interest_data
        self.df_indexes = df_indexes 
        self.correlation_matrix = correlation_matrix
