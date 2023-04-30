# H3 Storage and Processing

## Deploy Minio on K8s

1. Create persistent volume claim.

```
kubectl create -f k8s/minio-pvc.yml
```

2. Create Minio deployment.

```
kubectl create -f k8s/minio-deploy.yml
```

3. Create Minio service.

```
kubectl create -f k8s/minio-service.yml
```

Port forward:

```
kubectl port-forward svc/minio-service 9090:9090 9000:9000
```