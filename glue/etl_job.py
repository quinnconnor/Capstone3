import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F

a=getResolvedOptions(sys.argv,["JOB_NAME","SOURCE_DATABASE","SOURCE_TABLE","REDSHIFT_CONNECTION","REDSHIFT_TMP_DIR","REDSHIFT_SCHEMA"])
sc=SparkContext(); gc=GlueContext(sc); job=Job(gc); job.init(a["JOB_NAME"],a)
dyf=gc.create_dynamic_frame.from_catalog(database=a["SOURCE_DATABASE"],table_name=a["SOURCE_TABLE"])
df=dyf.toDF()
if not df.columns: raise ValueError("Schema validation failed: no columns")
for old in df.columns:
    new=old.strip().lower().replace(" ","_").replace("-","_")
    if new!=old: df=df.withColumnRenamed(old,new)
if df.limit(1).count()==0: raise ValueError("Data validation failed: zero rows")
df=df.withColumn("_source_table",F.lit(a["SOURCE_TABLE"])).withColumn("_ingested_at",F.current_timestamp())
dyf=gc.create_dynamic_frame.from_df(df,gc,"normalized")
gc.write_dynamic_frame.from_jdbc_conf(frame=dyf,catalog_connection=a["REDSHIFT_CONNECTION"],
    connection_options={"dbtable":f'{a["REDSHIFT_SCHEMA"]}.{a["SOURCE_TABLE"]}'},
    redshift_tmp_dir=a["REDSHIFT_TMP_DIR"])
job.commit()
