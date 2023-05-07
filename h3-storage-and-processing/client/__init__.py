from os import getenv
from io import BytesIO
from typing import Optional, IO

from minio import Minio
from minio.api import ObjectWriteResult
from urllib3.response import HTTPResponse


class Client:
    """
    CRUD client for Minio.

    For `**kwargs` see details for `minio.Minio`.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        bucket: Optional[str] = None,
        secure: bool = True,
        **kwargs,
    ):
        self.minio = Minio(
            endpoint=endpoint or getenv("MINIO_ENDPOINT"),
            access_key=access_key or getenv("MINIO_ACCESS_KEY"),
            secret_key=secret_key or getenv("MINIO_SECRET_KEY"),
            secure=secure,
            **kwargs,
        )
        self.bucket = bucket or "default"

    def create(
        self,
        name: str,
        data: IO,
        content_type: str = "application/octet-stream",
        bucket: Optional[str] = None,
        **kwargs,
    ) -> ObjectWriteResult:
        """
        Create object.

        For `**kwargs` see `minio.Minio.put_object`.
        """
        length = None

        if isinstance(data, str):
            data = data.encode()

        if isinstance(data, bytes):
            length = len(data)
            data = BytesIO(data)

        return self.minio.put_object(
            object_name=name,
            data=data,
            length=kwargs.get("length") or length,
            content_type=content_type,
            bucket_name=bucket or self.bucket,
            **kwargs,
        )

    def read(
        self,
        name: str,
        version: Optional[str] = None,
        bucket: Optional[str] = None,
    ) -> HTTPResponse:
        """
        Read object.

        For `**kwargs` see `minio.Minio.get_object`.
        """
        return self.minio.get_object(
            object_name=name,
            version_id=version,
            bucket_name=bucket or self.bucket,
        )

    def update(
        self,
        name: str,
        data: IO,
        content_type: Optional[str] = None,
        bucket: Optional[str] = None,
        **kwargs,
    ) -> ObjectWriteResult:
        """
        Update object.

        Raises an `ValueError` if object does not exist.

        For `**kwargs` see `minio.Minio.put_object`.
        """
        obj = self.minio.stat_object(object_name=name, bucket_name=bucket or self.bucket)

        return self.create(
            name=name,
            data=data,
            content_type=content_type or obj.content_type,
            bucket=bucket,
            **kwargs,
        )

    def delete(
        self,
        name: Optional[str] = None,
        version: Optional[str] = None,
        bucket: Optional[str] = None,
    ):
        self.minio.remove_object(
            bucket_name=bucket or self.bucket,
            object_name=name,
            version_id=version,
        )
