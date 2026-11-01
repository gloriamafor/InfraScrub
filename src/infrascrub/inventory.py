"""The only module that talks to AWS.

Every check reads from here instead of calling boto3 itself. Each AWS API is
called once per region and the result is cached, so adding a check never adds
an API call.

Two methods are finished (ebs_volumes, ec2_instances) so you can see the
pattern. The others are yours to write; each stub tells you which boto3 call
to use. Follow the finished ones exactly: paginate, flatten, cache.
"""

from collections.abc import Callable
from typing import Any

import boto3


class Inventory:
    def __init__(self, session: boto3.Session, regions: list[str]):
        self.session = session
        self.regions = regions
        self._cache: dict[tuple, Any] = {}

    # ---- plumbing -------------------------------------------------------

    def client(self, service: str, region: str | None = None):
        return self.session.client(service, region_name=region)

    def _cached(self, key: tuple, fetch: Callable[[], Any]) -> Any:
        """Run fetch() once per key, then serve the stored result."""
        if key not in self._cache:
            self._cache[key] = fetch()
        return self._cache[key]

    # ---- finished examples ---------------------------------------------

    def ebs_volumes(self, region: str) -> list[dict]:
        """All EBS volumes in a region. Each dict is one entry from describe_volumes."""

        def fetch() -> list[dict]:
            ec2 = self.client("ec2", region)
            volumes: list[dict] = []
            for page in ec2.get_paginator("describe_volumes").paginate():
                volumes.extend(page["Volumes"])
            return volumes

        return self._cached(("ebs_volumes", region), fetch)

    def ec2_instances(self, region: str) -> list[dict]:
        """All EC2 instances in a region, flattened out of their Reservations."""

        def fetch() -> list[dict]:
            ec2 = self.client("ec2", region)
            instances: list[dict] = []
            for page in ec2.get_paginator("describe_instances").paginate():
                for reservation in page["Reservations"]:
                    instances.extend(reservation["Instances"])
            return instances

        return self._cached(("ec2_instances", region), fetch)

    # ---- yours to write --------------------------------------------------

    def security_groups(self, region: str) -> list[dict]:
        """All security groups in a region.

        Use: ec2.get_paginator("describe_security_groups"), key "SecurityGroups".
        Same shape as ebs_volumes above.
        """
        raise NotImplementedError("Build guide, step 7")

    def s3_buckets(self) -> list[dict]:
        """All S3 buckets. S3 is global, so no region argument and no paginator.

        Use: s3.list_buckets()["Buckets"]. Cache key: ("s3_buckets",).
        """
        raise NotImplementedError("Build guide, step 8")

    def elastic_ips(self, region: str) -> list[dict]:
        """All Elastic IPs in a region.

        Use: ec2.describe_addresses()["Addresses"]. No paginator for this call.
        """
        raise NotImplementedError("Build guide, step 9")

    def snapshots(self, region: str) -> list[dict]:
        """EBS snapshots owned by this account.

        Use: ec2.get_paginator("describe_snapshots").paginate(OwnerIds=["self"]),
        key "Snapshots". Without OwnerIds you get every public snapshot on AWS.
        """
        raise NotImplementedError("Build guide, step 10")
