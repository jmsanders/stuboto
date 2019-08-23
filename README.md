# Stuboto

Stub `boto3` clients to avoid hitting real AWS endpoints in tests.

# Usage

You can use `Stuboto` instances as if they were `botocore.stub.Stubber`:

```python3
import boto3
from stuboto import Stuboto

def test_create_bucket():
    s3 = boto3.client("s3")
    stubber = Stuboto(s3)
    stubber.activate()

    response = {"Location": "my-bucket"}
    expected_params = {"Bucket": "my-bucket", "ACL": "private"}

    stubber.add_response("create_bucket", response, expected_params)
    service_response = s3.create_bucket(Bucket="my-bucket", ACL="private")
    assert service_response == response
```

`Stuboto` instances are decorated with all the same methods as the original `boto3` client so you can also stub responses with the arguably more readable:

```python3
import boto3
from stuboto import Stuboto

def test_create_bucket():
    s3 = boto3.client("s3")
    stubber = Stuboto(s3)
    stubber.activate()

    response = stubber.create_bucket(Bucket="my-bucket", ACL="private").add_response(
        Location="my-bucket"
    )
    service_response = s3.create_bucket(Bucket="my-bucket", ACL="private")
    assert service_response == response
```

`botocore.stub.Stubber` documentation suggests:

> It should be noted, however, that while missing attributes are often considered correct, your code may not function properly if you leave them out. Therefore you should always fill in every value you see in a typical response for your particular request.

But I won't tell anybody if you leave some values out in favor of writing more readable tests.

## Installation

```bash
pip install stuboto
```
