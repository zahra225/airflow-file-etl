import pandas as pd
import logging

def extract_data(**context):
    """Extract data from CSV file"""
    input_path = '/opt/airflow/data/input/customers.csv'
    
    logging.info(f"Extracting data from: {input_path}")
    
    try:
        df = pd.read_csv(input_path)
        logging.info(f"Extracted {len(df)} records")
        logging.info(f"Columns: {list(df.columns)}")
        
        # Convert DataFrame to dict and store in XCom
        context['ti'].xcom_push(key='data', value=df.to_dict('records'))
        context['ti'].xcom_push(key='columns', value=list(df.columns))
        
        return f"Extracted {len(df)} records"
    except Exception as e:
        logging.error(f"Error in extract: {str(e)}")
        raise