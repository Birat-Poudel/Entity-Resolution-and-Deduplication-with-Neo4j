# from setup import connect_database
from fetch_csv import fetch_csv_data

# Uncomment the code when required for testing scripts independently
# driver = connect_database()

def load_and_process_data(driver):
    with driver.session() as session:
        csv_data = fetch_csv_data()

        for row in csv_data:
            session.run(
                """
                MERGE (p:Person {email: $email})
                SET p.name = $name, p.phone = $phone
                MERGE (loc1:Location {address: $address})
                MERGE (p)-[:LIVES_AT]->(loc1)
                """,
                email=row['email'],
                name=row['name'],
                phone=row['phone'],
                address=row['address_1']
            )

        session.run(
            """
            CALL gds.graph.project(
              'GraphEmployee3',
              ['Person'],
              ['LIVES_AT'],
              { relationshipProperties: ['strength'] }
            )
            """
        )

        session.run(
            """
            MATCH (p1:Person), (p2:Person)
            WHERE elementid(p1) < elementid(p2) AND (
                p1.email = p2.email OR
                p1.phone = p2.phone OR
                apoc.text.levenshteinSimilarity(p1.name, p2.name) > 0.9
            )
            WITH p1, p2, count(*) as matches
            CALL apoc.merge.node(['Person'], {
                email: coalesce(p1.email, p2.email)
            }, {
                name: coalesce(p1.name, p2.name),
                phone: coalesce(p1.phone, p2.phone)
            }) YIELD node as mergedPerson
            CALL apoc.refactor.mergeNodes([p1, p2, mergedPerson], {properties: "overwrite", mergeRels: true})
            YIELD node
            RETURN node AS mergedPerson, count(*) AS mergedPersonCount
            """
        )

# Uncomment the code when required for testing scripts independently.

# if __name__ == "__main__":
#     try:
#         load_and_process_data(driver)
#     finally:
#         driver.close()