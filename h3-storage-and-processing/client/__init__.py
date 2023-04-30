from os import environ
from typing import Optional, IO

from minio import Minio


class Client:
    """
    CRUD client for Minio.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        bucket: Optional[str] = None,
        secure: bool = True,
    ):
        self.client = Minio(
            endpoint=endpoint or environ.get("MINIO_ENDPOINT"),
            access_key=access_key or environ.get("MINIO_ACCESS_KEY"),
            secret_key=secret_key or environ.get("MINIO_SECRET_KEY"),
            secure=secure,
        )
        self.bucket = bucket or "default"

    def create(self,
        name: str,
        data: IO,
        content_type: str = "application/octet-stream",
        bucket: Optional[str] = None,
    ):
        return self.client.put_object(
            object_name=name,
            data=data,
            content_type=content_type,
            bucket_name=bucket or self.bucket,
        )
    
    def read(
        self,
        name: str,
        version: Optional[str] = None,
        bucket: Optional[str] = None,
    ):
        return self.client.get_object(
            object_name=name,
            version_id=version,
            bucket_name=bucket or self.bucket,
        )
        # TODO

    def update(self,
        name: str,
        data: IO,
        content_type: str = "application/octet-stream",
        bucket: Optional[str] = None,
    ):
        return self.create(name=name, data=data, content_type=content_type, bucket=bucket)

    def delete(
        self,
        name: Optional[str] = None,
        version: Optional[str] = None,
        bucket: Optional[str] = None,
    ):
        self.client.remove_object(
            bucket_name=bucket or self.bucket,
            object_name=name,
            version_id=version,
        )