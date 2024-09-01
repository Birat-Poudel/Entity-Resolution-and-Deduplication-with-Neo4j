from setup import connect_database

driver = connect_database()

def cql_tests(driver):
    query = """
    MATCH (p:Person)
    RETURN p.name AS name, p.email AS email, p.phone AS phone
    """
    
    with driver.session() as session:
        session.run(query)
        
if __name__ == "__main__":
    try:
        cql_tests(driver)
    finally:
        driver.close()