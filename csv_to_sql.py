import csv
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer

engine = create_engine('sqlite:///output.db')

metadata = MetaData()

person_table = Table('person', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('email', String),
    Column('phone', String)
)

metadata.create_all(engine)

with open('output.csv', 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    
    csv_columns = csvreader.fieldnames
    print("CSV Columns:", csv_columns)

    with engine.connect() as connection:
        for row in csvreader:
            print("Inserting:", row['name'])
            connection.execute(person_table.insert().values(
                name=row['name'],
                email=row['email'],
                phone=row['phone']
            ))
        
        connection.commit()
            
print("CSV data has been successfully converted and inserted into the SQL database.")