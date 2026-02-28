from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseConnector(ABC):
    """
    Abstract base class for all data ingestion connectors.
    """
    @abstractmethod
    def fetch_data(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Fetch data from the source and return a list of dictionaries.
        Each dictionary should contain at least a 'text' and 'id' field.
        """
        pass
