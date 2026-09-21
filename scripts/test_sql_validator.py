from app.sql_validator import validate_sql
CASES=[
("SELECT 1",True),("SELECT customer_id FROM customer_metrics",True),
("DROP TABLE customer_metrics",False),
("SELECT * FROM customer_metrics; DROP TABLE customer_metrics;",False),
("UPDATE customer_metrics SET churned=1",False),
("SELECT * FROM customer_metrics; DELETE FROM customer_metrics;",False),
("SELECT * FROM customer_metrics -- DROP TABLE x",True),
("SELECT * FROM customer_metrics /* DELETE FROM x */",True)]
for q,e in CASES:
    r=validate_sql(q); print(e,r,q); assert r["valid"]==e
print("All SQL validator tests passed.")
