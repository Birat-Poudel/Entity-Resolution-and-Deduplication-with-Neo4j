LOAD CSV WITH HEADERS FROM 'https://docs.google.com/spreadsheets/d/1d2aXpsKcTIarqS9LpHv8IXBus1BfgpFZG8J5p7_iMMk/pub?gid=1543451169&single=true&output=csv' AS row

MERGE (p:Person {email: row.email})
SET p.name = row.name,
    p.phone = row.phone

MERGE (loc1:Location {address: row.address_1})

MERGE (p)-[:LIVES_AT]->(loc1)

MATCH (source:Person)
OPTIONAL MATCH (source)-[r:LIVES_AT]->(target:Location)
RETURN gds.graph.project(
  'Graph',
  source,
  target,
  { relationshipProperties: r { strength: coalesce(r.strength, 1.0) } }
)

CALL gds.nodeSimilarity.write.estimate('Graph', {
  writeRelationshipType: 'SIMILAR',
  writeProperty: 'score'
})
YIELD nodeCount, relationshipCount, bytesMin, bytesMax, requiredMemory

CALL gds.nodeSimilarity.stream('Graph')
YIELD node1, node2, similarity
RETURN gds.util.asNode(node1).name AS Person1, gds.util.asNode(node2).name AS Person2, similarity
ORDER BY similarity DESCENDING, Person1, Person2

MATCH (p1:Person)
MATCH (p2:Person)
    WHERE id(p1) < id(p2)
        AND (p1.email = p2.email 
            OR p1.phone = p2.phone 
            OR apoc.text.levenshteinSimilarity(p1.name, p2.name) > 0.9)
        WITH p1, p2, count(*) as matches

CALL apoc.merge.node(['Person'], 
    {email: coalesce(p1.email, p2.email)}, 
    {name: coalesce(p1.name, p2.name), 
     phone: coalesce(p1.phone, p2.phone)}) YIELD node as mergedPerson

CALL apoc.refactor.mergeNodes([p1,p2,mergedPerson],{properties:"overwrite", mergeRels:true}) yield node
RETURN node AS mergedPerson, count(*) AS mergedPersonCount;

// For deleting Graph, Nodes and Relationships

MATCH (n:Person) RETURN n;

MATCH (n) DETACH DELETE n

CALL gds. graph. drop('Graph') YIELD graphName;

// For Debugging Purposes

MATCH (p1:Person)
MATCH (p2:Person)
    WHERE p1 <> p2
        AND (p1.email = p2.email 
            OR p1.phone = p2.phone 
            OR apoc.text.levenshteinSimilarity(p1.name, p2.name) > 0.9)
RETURN p1, p2