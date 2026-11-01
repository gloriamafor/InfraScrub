"""Worked example test. Copy this shape for every check you write.

Pattern:
    1. create the AWS state you want (one good resource, one bad one)
    2. run the check
    3. assert it flagged the bad one and only the bad one
"""

from infrascrub.checks.unattached_ebs import UnattachedEbs
from infrascrub.inventory import Inventory
from infrascrub.models import Category
from tests.conftest import REGION


def test_flags_only_the_unattached_volume(aws):
    ec2 = aws.client("ec2", region_name=REGION)

    # a running instance comes with an attached root volume (the "good" one)
    ec2.run_instances(ImageId="ami-12345678", MinCount=1, MaxCount=1, InstanceType="t3.micro")

    # a volume nobody attached (the "bad" one)
    orphan = ec2.create_volume(AvailabilityZone=f"{REGION}a", Size=100, VolumeType="gp3")["VolumeId"]

    findings = UnattachedEbs().run(Inventory(aws, [REGION]), REGION)

    assert len(findings) == 1
    finding = findings[0]
    assert finding.resource_id == orphan
    assert finding.category == Category.COST
    assert finding.monthly_cost_usd == 8.0  # 100 GB * $0.08
    assert orphan in finding.remediation
    assert "delete-volume" in finding.remediation


def test_clean_region_returns_nothing(aws):
    findings = UnattachedEbs().run(Inventory(aws, [REGION]), REGION)
    assert findings == []
