# Infrastructure setup

Course sandboxes often pre-create some resources, so this repository intentionally keeps deployment resource-agnostic rather than hard-coding account-specific IDs.

Create/configure:
1. S3 bucket with Block Public Access, encryption and versioning.
2. ECR repository and the Lambda image from `lambda_ingest/Dockerfile`.
3. Lambda with S3 ObjectCreated trigger on `raw/`.
4. RDS PostgreSQL reachable by the Lambda.
5. Amazon OpenSearch Service domain with k-NN enabled.
6. Glue Catalog database and S3 crawler over `raw/`.
7. Glue Spark job and a Redshift Glue connection.
8. Redshift cluster or Serverless workgroup.
9. IAM roles with least privilege.

Recommended network:
* RDS/OpenSearch/Redshift/Lambda in private subnets.
* VPC endpoints or NAT for required AWS APIs.
* Glue connection configured for the same VPC/subnet/security group needed to reach Redshift.

Lambda IAM should minimally cover:
* s3:GetObject on the raw prefix
* textract:DetectDocumentText
* es:ESHttpGet/Post/Put for the index
* CloudWatch Logs

AI query runtime:
* bedrock:InvokeModel for the exact allowed inference profile
* redshift-data:ExecuteStatement/DescribeStatement/GetStatementResult
* OpenSearch read access

Use Secrets Manager for database credentials instead of hard-coding passwords.

## ECR commands

```bash
AWS_REGION=us-east-1
REPO=unit3-ingest
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

aws ecr create-repository --repository-name "$REPO" --region "$AWS_REGION" || true
aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

docker build -t "$REPO" lambda_ingest/
docker tag "$REPO:latest" "$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO:latest"
docker push "$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO:latest"
```

Then set the Lambda package type to Image.

## OpenSearch

After the Lambda role can access OpenSearch:

```bash
python -c "from app.opensearch_store import OpenSearchStore; OpenSearchStore().ensure_index()"
```

The index is a 384-dimensional `knn_vector` using cosine similarity.
