from langchain_core.tools import tool
from typing import List, Dict, Any
from database.postgres_connector import get_customer_services

@tool
def get_customer_services_tool(customer_name: str) -> List[Dict[str, Any]]:
    """
    Retrieve all services for a given customer name from the 'customer_services' table.
    
    Args:
        customer_name: The name of the customer.
    
    Returns:
        A list of dictionaries, each representing a service.
    """
    return get_customer_services(customer_name)