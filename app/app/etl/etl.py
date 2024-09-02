from .extract import Extraction
from .transform import Transformation
from .load import Load

class ETL:
    
    def __init__(self):
        self.extracter = Extraction()
        self.transformer = Transformation()
        self.loader = Load()
    
    def execute(self, spark_session):
        extraction = self.extracter.extract(spark_session)
        transformed = self.transformer.transform(extraction, spark_session)
        df_indexes = self.loader.load(transformed)
        return df_indexes