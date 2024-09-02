from app.model.etl import TransformationModel

class Load:
    
    def load(self, transformation: TransformationModel):
        df_bovespa = transformation.bovespa_data
        df_inflation_data = transformation.inflation_data
        df_selic_data = transformation.selic_data 
        df_tcr_data = transformation.tcr_data
        df_ptax_data = transformation.ptax_data
        df_fed_interest = transformation.fed_interest_data
        df_indexes = transformation.df_indexes
        df_correlation_matrix = transformation.correlation_matrix 
        
        df_indexes.show()
        print(df_correlation_matrix)

        df_bovespa.write.parquet('./apps/bovespa.parquet', mode='overwrite')
        df_inflation_data.write.parquet('./apps/ipca.parquet', mode='overwrite')
        df_selic_data.write.parquet('./apps/selic.parquet', mode='overwrite') 
        df_tcr_data.write.parquet('./apps/tcr.parquet', mode='overwrite')
        df_ptax_data.write.parquet('./apps/ptax.parquet', mode='overwrite')
        df_fed_interest.write.parquet('./apps/fed_interest.parquet', mode='overwrite')
        df_indexes.write.parquet('./apps/brazilian_indexes.parquet', mode='overwrite')
        df_correlation_matrix.to_parquet('./apps/correlation_matrix_with_labels.parquet')
        print('WRITTEN SUCCESSFULLY')