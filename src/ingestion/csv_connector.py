import pandas as pd
from typing import List, Dict, Any
from .base import BaseConnector

class CSVConnector(BaseConnector):
    """
    Connector to ingest data from CSV files.
    """
    def fetch_data(self, file_path: str, text_column: str = "text", id_column: str = "id") -> List[Dict[str, Any]]:
        df = pd.read_csv(file_path)
        
        # Ensure required columns exist
        if text_column not in df.columns:
            raise ValueError(f"Column '{text_column}' not found in CSV.")
        
        # If id column doesn't exist, create it from index
        if id_column not in df.columns:
            df[id_column] = df.index.astype(str)
            
        data = df[[id_column, text_column]].rename(columns={
            id_column: "id",
            text_column: "text"
        }).to_dict(orient="records")
        
        return data
