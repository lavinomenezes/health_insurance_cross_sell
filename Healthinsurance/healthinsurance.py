import pickle
import numpy  as np
import pandas as pd

class HealthInsurance:
    
    def __init__( self ):
        self.home_path = ''
        self.annual_premium_scaler =            pickle.load( open( self.home_path + 'features/annual_premium_scaler.pkl','rb' ) )
        self.age_scaler =                       pickle.load( open( self.home_path + 'features/age_scaler.pkl','rb' ) ) 
        self.vintage_scaler =                   pickle.load( open( self.home_path + 'features/vintage_scaler.pkl','rb' ) ) 
        
    def data_cleaning( self, df1 ):
        # 1.1. Rename Columns
        cols_new = ['id', 'gender', 'age','region_code', 'previously_insured', 'vehicle_age', 
                    'vehicle_damage', 'annual_premium', 'policy_sales_channel', 'vintage', 'response']

        # rename 
        df1.columns = cols_new
        
        return df1 

    
    def feature_engineering( self, df2 ):
        # Feature Engineering

        # Vehicle Damage Number
        df2['vehicle_damage'] = df2['vehicle_damage'].apply(lambda x: 1 if x =='Yes' else 0)

        # Vehicle Age
        df2['gender'] = df2['gender'].apply(lambda x: 1 if x=='Female' else (0 if x=='Male' else x))

        df2['vehicle_damage'] = df2['vehicle_damage'].apply(lambda x: 1 if x =='Yes' else 0)
        
        return df2
    
    
    def data_preparation( self, df5 ):

        # Min - max sacaler
        df5['age'] = self.annual_premium_scaler.transform(df5[['age']].values)

        df5['vintage'] = self.vintage_scaler.transform(df5[['vintage']].values)

        # StandardScale
        df5['annual_premium'] = self.annual_premium_scaler.transform(df5[['annual_premium']].values)

        # vehicle_age ordinal scale
        vehicle_age_dict = {'> 2 Years':3, '1-2 Year':2, '< 1 Year':1}
        df5['vehicle_age'] = df5['vehicle_age'].map(vehicle_age_dict)

        # Feature Selection
        final_columns = ['id',  'age', 'region_code', 'policy_sales_channel',
              'previously_insured', 'annual_premium', 'vintage', 'vehicle_age',
              'vehicle_damage', 'response']
        
        return df5[ final_columns ]
    
    
    def get_prediction( self, model, original_data, test_data ):
        # model prediction
        pred = model.predict_proba( test_data )
        
        # join prediction into original data
        original_data['prediction'] = pred
        
        return original_data.to_json( orient='records', date_format='iso' )