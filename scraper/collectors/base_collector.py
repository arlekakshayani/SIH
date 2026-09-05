import os
import sys

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseFlightCollector(ABC):
    """
    Abstract blueprint for all flight collectors.
    Every new portal or API collector must inherit from this class.
    """

    def __init__(self, source_name: str):
        self.source_name = source_name

    @abstractmethod
    def search_flights(
        self, 
        origin: str, 
        destination: str, 
        departure_date: str, 
        advance_days: int
    ) -> List[Dict[str, Any]]:
        """
        Queries the source for flight fares on a given route and date.
        Must return a list of normalized flight dictionaries.
        """
        pass
