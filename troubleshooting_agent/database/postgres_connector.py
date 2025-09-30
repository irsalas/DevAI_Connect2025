import psycopg2
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

def get_customer_services(customer_name: str) -> List[Dict[str, Any]]:
    """
    Connects to a PostgreSQL database and queries for all services related to a specific customer.
    
    Args:
        customer_name: The name of the customer to search for.
    
    Returns:
        A list of dictionaries containing service information.
    """
    conn = None
    try:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is not set.")

        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        query = "SELECT service_id, service_type FROM customer_services WHERE customer_name = %s;"
        cur.execute(query, (customer_name,))
        
        results = cur.fetchall()
        
        service_list = []
        for row in results:
            service_list.append({
                "service_id": row[0],
                "service_type": row[1]
            })
            
        cur.close()
        return service_list

    except (Exception, psycopg2.Error) as error:
        print(f"Error connecting to PostgreSQL or executing query: {error}")
        return []
    finally:
        if conn:
            conn.close()