from os import getenv
from io import BytesIO

import pytest
from minio import Minio
from minio.error import S3Error

from client import Client

ENDPOINT = getenv("MINIO_ENDPOINT", "localhost:9000")
ACCESS_KEY = getenv("MINIO_ACCESS_KEY", "minioadmin")
SECRET_KEY = getenv("MINIO_SECRET_KEY", "minioadmin")


@pytest.fixture()
def minio():
    return Minio(
        endpoint=ENDPOINT,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=False,
    )


@pytest.fixture()
def bucket(minio: Minio):
    """
    Fixture that creates a test bucket before tests are run and deletes it after tests are run.
    """
    bucket_name = "test-bucket"
    try:
        minio.make_bucket(bucket_name)
        yield bucket_name
    finally:
        for obj in minio.list_objects(bucket_name, recursive=True):
            minio.remove_object(bucket_name, obj.object_name)
        minio.remove_bucket(bucket_name)


@pytest.fixture()
def client(bucket: str):
    return Client(
        endpoint=ENDPOINT,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=False,
        bucket=bucket,
    )


def test_create(client: Client, minio: Minio):
    # Arrange
    data = b"hello, world"
    object_name = "test-object"
    content_type = "text/plain"

    # Act
    client.create(object_name, data, content_type=content_type)

    # Assert
    assert minio.stat_object(client.bucket, object_name).content_type == content_type
    with minio.get_object(client.bucket, object_name) as response:
        assert response.read() == data


def test_read(client: Client, minio: Minio):
    # Arrange
    data = b"hello, world"
    object_name = "test-object"
    content_type = "text/plain"
    minio.put_object(client.bucket, object_name, BytesIO(data), len(data), content_type)

    # Act
    with client.read(object_name) as response:
        # Assert
        assert response.read() == data


def test_update(client: Client, minio: Minio):
    # Arrange
    data = b"hello, world"
    object_name = "test-object"
    content_type = "text/plain"
    new_data = b"hello, new world"
    minio.put_object(client.bucket, object_name, BytesIO(data), len(data), content_type)

    # Act
    client.update(object_name, new_data)

    # Assert
    with minio.get_object(client.bucket, object_name) as response:
        assert response.data == new_data


def test_delete(client: Client, minio: Minio):
    # Arrange
    data = b"hello, world"
    object_name = "test-object"
    content_type = "text/plain"
    minio.put_object(client.bucket, object_name, BytesIO(data), len(data), content_type)

    # Act
    client.delete(object_name)

    # Assert
    with pytest.raises(S3Error):
        with minio.get_object(client.bucket, object_name):
            pass
