from setup import connect_database
from app import load_and_process_data
from export_nodes_to_csv import export_nodes_to_csv
from csv_to_sql import csv_to_sql

driver = connect_database()

if __name__ == "__main__":
    try:
        result = load_and_process_data(driver)
        export_nodes_to_csv(result, 'exported_nodes.csv')
        csv_to_sql()
    finally:
        driver.close()