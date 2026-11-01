"""Shared test setup.

moto fakes AWS in memory. Anything you create through the `aws` session here
exists only for the duration of one test and costs nothing. No real
credentials are used; the fake keys below stop boto3 from looking for real ones.
"""

import os

import boto3
import pytest
from moto import mock_aws

REGION = "us-east-1"


@pytest.fixture
def aws():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = REGION
    with mock_aws():
        yield boto3.Session(region_name=REGION)
