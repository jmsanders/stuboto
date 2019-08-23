import datetime

import boto3

import pytest
from stuboto import stub


def test_classic_stubber():
    s3 = boto3.client("s3")
    stubber = stub(s3)

    response = {"Location": "my-bucket"}
    expected_params = {"Bucket": "my-bucket", "ACL": "private"}

    stubber.add_response("create_bucket", response, expected_params)
    service_response = s3.create_bucket(Bucket="my-bucket", ACL="private")
    assert service_response == response


def test_stuboto_stubber():
    s3 = boto3.client("s3")
    stubber = stub(s3)

    response = stubber.create_bucket(Bucket="my-bucket", ACL="private").with_response(
        Location="my-bucket"
    )
    service_response = s3.create_bucket(Bucket="my-bucket", ACL="private")
    assert service_response == response


def test_stuboto_stubber_with_any_param():
    s3 = boto3.client("s3")
    stubber = stub(s3)

    response = stubber.create_bucket().with_response(Location="my-bucket")
    service_response = s3.create_bucket(Bucket="my-bucket", ACL="private")
    assert service_response == response


def test_stuboto_complex_responses():
    s3 = boto3.client("s3")
    stubber = stub(s3)

    stubber.list_objects_v2(Bucket="my-bucket").with_response(
        IsTruncated=True,
        ContinuationToken="page 1",
        NextContinuationToken="page 2",
        Contents=[dict(Key="Key 1"), dict(Key="Key 2")],
    )

    stubber.list_objects_v2(
        Bucket="my-bucket", ContinuationToken="page 2"
    ).with_response(
        IsTruncated=False, ContinuationToken="page 2", Contents=[dict(Key="Key 3")]
    )

    paginator = s3.get_paginator("list_objects_v2")
    keys = []
    for page in paginator.paginate(Bucket="my-bucket"):
        keys += [key["Key"] for key in page["Contents"]]

    assert len(keys) == 3
    assert set(keys) == set(["Key 1", "Key 2", "Key 3"])
    stubber.assert_no_pending_responses()


def test_stubber_has_all_stubbable_methods():
    s3 = boto3.client("s3")
    stubber = stub(s3)
    methods = [attr for attr in dir(stubber) if callable(getattr(stubber, attr))]

    assert set(s3.meta.method_to_api_mapping.keys()).issubset(methods)
    assert "get_paginator" not in methods
    assert "get_waiter" not in methods


def test_multiple_services_can_be_stubbed():
    s3_stubber = stub(boto3.client("s3"))
    ec2_stubber = stub(boto3.client("ec2"))

    s3_methods = [
        attr for attr in dir(s3_stubber) if callable(getattr(s3_stubber, attr))
    ]
    ec2_methods = [
        attr for attr in dir(ec2_stubber) if callable(getattr(ec2_stubber, attr))
    ]

    assert set(s3_methods) != set(ec2_methods)
