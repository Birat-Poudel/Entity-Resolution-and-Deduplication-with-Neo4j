# from setup import connect_database
import csv

# Uncomment the code when required for testing scripts independently.
# driver = connect_database()

def export_nodes_to_csv(driver, filename):
    query = """
    MATCH (p:Person)
    RETURN p.name AS name, p.email AS email, p.phone AS phone
    """
    
    with driver.session() as session:
        result = session.run(query)
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'email', 'phone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for record in result:
                row = {field: record[field] for field in fieldnames}
                writer.writerow(row)

# Uncomment the code when required for testing scripts independently.

# if __name__ == "__main__":
#     try:
#         export_nodes_to_csv(driver, 'exported_nodes.csv')
#     finally:
#         driver.close()