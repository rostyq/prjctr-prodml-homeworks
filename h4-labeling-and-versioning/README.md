# H4 Labeling & Versioning

### DVC

Setup Minio and its keys:

```ps1
$env:AWS_ACCESS_KEY_ID="minioadmin"
$env:AWS_SECRET_ACCESS_KEY="minioadmin"
```

Create bucket and add it to dvc:

```
aws s3 create-bucket --bucket dvc-store --endpoint-url http://localhost:9000
dvc remote add --default minio s3://dvc-store
```

Push commited data:

```
dvc push
```
