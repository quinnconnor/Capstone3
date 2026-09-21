import os,matplotlib.pyplot as plt
from app.redshift_store import RedshiftStore
os.makedirs("charts",exist_ok=True); rs=RedshiftStore()
rows=rs.execute("SELECT source_key AS source, COUNT(*) AS record_count FROM structured_records GROUP BY 1 ORDER BY 2 DESC")
if rows:
    plt.figure(figsize=(10,6)); plt.bar([str(x["source"]) for x in rows],[float(x["record_count"]) for x in rows])
    plt.xticks(rotation=45,ha="right"); plt.ylabel("Count"); plt.title("Redshift records by source")
    plt.tight_layout(); plt.savefig("charts/records_by_source.png",dpi=160); plt.close()
rows=rs.execute("SELECT DATE_TRUNC('month',processed_at) AS month,SUM(row_count) AS rows_processed FROM etl_audit GROUP BY 1 ORDER BY 1")
if rows:
    plt.figure(figsize=(10,6)); plt.plot([x["month"] for x in rows],[float(x["rows_processed"]) for x in rows],marker="o")
    plt.ylabel("Rows processed"); plt.title("Rows processed by month"); plt.xticks(rotation=45,ha="right")
    plt.tight_layout(); plt.savefig("charts/records_over_time.png",dpi=160); plt.close()
print("Charts generated when the warehouse contains data.")
