operation = "tba"
query = """tba
"""

def get_system_status_query(system_id):
    return {
        "operationName": operation,
        "variables": {
            #tba
        },
        "query": query,
    }