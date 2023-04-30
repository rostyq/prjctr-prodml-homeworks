# H3 Storage and Processing

## Deploy Minio on K8s

1. Create persistent volume claim.

```
kubectl create -f minio-pvc.yml
```

2. Create Minio deployment.

```
kubectl create -f minio-deploy.yml
```

3. Create Minio service.

```
kubectl create -f minio-service.yml
```

Port forward:

```
kubectl port-forward svc/minio-service 9090:9090 9000:9000
```