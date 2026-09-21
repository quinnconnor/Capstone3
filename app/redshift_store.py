import time,boto3
from .config import settings
class RedshiftStore:
    def __init__(self): self.client=boto3.client("redshift-data",region_name=settings.region)
    def _args(self):
        x={"Database":settings.redshift_database}
        if settings.redshift_workgroup_name: x["WorkgroupName"]=settings.redshift_workgroup_name
        elif settings.redshift_cluster_id: x["ClusterIdentifier"]=settings.redshift_cluster_id
        else: raise ValueError("Set REDSHIFT_WORKGROUP_NAME or REDSHIFT_CLUSTER_ID")
        if settings.redshift_secret_arn: x["SecretArn"]=settings.redshift_secret_arn
        elif settings.redshift_db_user: x["DbUser"]=settings.redshift_db_user
        else: raise ValueError("Set REDSHIFT_SECRET_ARN or REDSHIFT_DB_USER")
        return x
    def execute(self,sql):
        r=self.client.execute_statement(Sql=sql,**self._args()); sid=r["Id"]; deadline=time.time()+settings.redshift_data_api_timeout
        while time.time()<deadline:
            d=self.client.describe_statement(Id=sid)
            if d["Status"]=="FINISHED": break
            if d["Status"] in {"FAILED","ABORTED"}: raise RuntimeError(d.get("Error",d["Status"]))
            time.sleep(.5)
        else: raise TimeoutError("Redshift Data API timed out")
        r=self.client.get_statement_result(Id=sid); cols=[x["name"] for x in r.get("ColumnMetadata",[])]
        return [{n:(next(iter(c.values())) if c else None) for n,c in zip(cols,row)} for row in r.get("Records",[])]
