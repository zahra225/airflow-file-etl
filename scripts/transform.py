import pandas as pd
import logging
from datetime import datetime

def transform_data(**context):
    """Transform data: Clean and process"""
    
    try:
        # Get data from XCom
        data = context['ti'].xcom_pull(key='data', task_ids='extract_task')
        
        if not data:
            raise ValueError("No data received from extract task")
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        logging.info(f"Starting transformation on {len(df)} records")
        logging.info(f"Original columns: {list(df.columns)}")
        
        # 1. Handle missing emails
        df['email'] = df['email'].fillna('unknown@email.com')
        
        # 2. Handle missing age with median
        if df['age'].isnull().any():
            median_age = df['age'].median()
            df['age'] = df['age'].fillna(median_age)
        df['age'] = df['age'].astype(int)
        
        # 3. Add transformation timestamp
        df['transformed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 4. Customer segment based on age
        df['segment'] = pd.cut(df['age'], 
                               bins=[0, 30, 50, 100],
                               labels=['Young', 'Adult', 'Senior'])
        
        # 5. Clean city names
        df['city'] = df['city'].str.strip().str.title()
        
        # 6. Mark active customers
        df['is_active'] = df['spent_amount'] > 0
        
        logging.info(f"Transformation complete. New columns added: segment, is_active")
        logging.info(f"Active customers: {df['is_active'].sum()}")
        
        # Store transformed data back to XCom
        context['ti'].xcom_push(key='transformed_data', value=df.to_dict('records'))
        
        return f"Transformed {len(df)} records"
        
    except Exception as e:
        logging.error(f"Error in transform: {str(e)}")
        raise