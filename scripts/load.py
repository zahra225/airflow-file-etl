import pandas as pd
import logging
import os
from datetime import datetime

def load_data(**context):
    """Load transformed data to CSV file"""
    
    try:
        # Get transformed data
        data = context['ti'].xcom_pull(key='transformed_data', task_ids='transform_task')
        
        if not data:
            raise ValueError("No transformed data received from transform task")
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Create output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = '/opt/airflow/data/output/'
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, f'transformed_customers_{timestamp}.csv')
        
        # Save to CSV
        df.to_csv(output_path, index=False)
        
        logging.info(f"Data loaded successfully to: {output_path}")
        logging.info(f"Saved {len(df)} records, {len(df.columns)} columns")
        
        # Also save a summary
        summary_path = os.path.join(output_dir, f'summary_{timestamp}.txt')
        with open(summary_path, 'w') as f:
            f.write(f"ETL Pipeline Summary\n")
            f.write(f"===================\n")
            f.write(f"Execution Time: {datetime.now()}\n")
            f.write(f"Output File: {output_path}\n")
            f.write(f"Record Count: {len(df)}\n")
            f.write(f"Columns: {list(df.columns)}\n")
        
        return f"Loaded {len(df)} records to {output_path}"
        
    except Exception as e:
        logging.error(f"Error in load: {str(e)}")
        raise